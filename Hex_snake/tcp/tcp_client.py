import socket
from threading import Thread
import time
import numpy as np


BOARD_HEIGHT = 10
BOARD_WIDTH = 14


# ==================== Wątek klienta do gry online ====================
class SnakeClientThread(Thread):
    # Wątek klienta włączany jest przez każdego gracza grającego online(zarówno osobę hostującą grę, jak i tą
    # przyłączającą się do gry. Służy on do komunikacji z serwerew.

    # ==================== Konstruktor ====================
    def __init__(self, main_thread, ip, port, player_id):
        Thread.__init__(self)
        self.MAIN_THREAD = main_thread
        self.server_ip = ip
        self.server_port = port
        self.is_running = False
        self.player_id = player_id
        self.board_array = []
        self.fruit_array = []
        self.p1_state = []
        self.p2_state = []
        self.p1_ready = False
        self.p2_ready = False
        self.reset = False
        self.game_over = False
        self.game_over_waiting = False
        self.new_data_received = False
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ==================== Funkcja run ====================
    def run(self):
        try:
            # Próba nawiązania połączanie z serwerem, poinformowanie serwera o tym, jakie jest nasze ID gracza
            server_address = (self.server_ip, self.server_port)
            self.connection.connect(server_address)
            self.connection.recv(100)
            self.send_data('P{}'.format(self.player_id))
            self.connection.recv(100)
            self.is_running = True
            print('Player {}: connected'.format(self.player_id))
            self.MAIN_THREAD.client_thread_event.set()
        except socket.error:
            self.is_running = False
            self.MAIN_THREAD.client_thread_event.set()
            self.close_connection()
            print("client error")

        while self.is_running is True:
            # Odbieranie wiadomości od serwera
            data_in = b''
            while self.is_running is True:
                try:
                    data_t = self.connection.recv(25000)
                    data_in += data_t
                    if len(data_t) < 25000:
                        break
                except socket.error:
                    self.close_connection()
                    break
            if len(data_in) == 0:
                self.close_connection()

            try:
                # Próba rozdzielanie wiadomości oddzielonych separatorem(przyjęty separator to znak '$')
                msg = data_in.decode()
                msgs = msg.split('$')
            except UnicodeDecodeError:
                msgs = ['']

            for msg in msgs:
                # Iterowanie po wszystkich wiadomościach rozdzielonych separatorem
                if msg[0:3] == 'RST':
                    # Serwer żąda od klienta zrestartowania gry
                    self.reset = True
                    self.game_over = False
                    self.game_over_waiting = False
                    self.new_data_received = False
                elif msg[0:3] == 'END':
                    # Serwer informuje klienta o końcu gry(oba agenty graczy zginęły)
                    self.game_over = True
                    self.game_over_waiting = False
                    self.new_data_received = False
                elif msg[0:11] == 'FRAME_START':
                    # Informacja o początku przesyłu ramki
                    pass
                elif msg[0:9] == 'FRAME_END':
                    # Informacja o końcu przesyłu ramki
                    self.new_data_received = True
                elif msg[0:5] == 'BOARD':
                    # Tablica zawierająca informacje o polach planszy
                    self.board_array = msg[5:].split('/')
                elif msg[0:5] == 'FRUIT':
                    # Tablica zawierająca informacje o owocahc obecnych na planszy
                    self.fruit_array = msg[5:].split('/')
                elif msg[0:2] == 'P1':
                    # Tablica zawierająca informacje o graczu 1
                    self.p1_state = msg[2:].split('/')
                elif msg[0:2] == 'P2':
                    # Tablica zawierająca informacje o graczu 2
                    self.p2_state = msg[2:].split('/')
                elif msg[0:3] == 'RDY':
                    # Informacja o gotowości danego klienta do gry(tylko na początku gry)
                    data = msg[3:].split('/')
                    try:
                        player = int(data[0])
                        ready = int(data[1])
                        if player == 1:
                            if ready == 1:
                                self.p1_ready = True
                            else:
                                self.p1_ready = False
                        elif player == 2:
                            if ready == 1:
                                self.p2_ready = True
                            else:
                                self.p2_ready = False
                        self.MAIN_THREAD.multi_update = True
                    except (IndexError, ValueError):
                        pass
                if self.new_data_received is True:
                    # Przesłanie do GUI informacji o otrzymaniu nowej ramki
                    self.new_data_received = False
                    self.MAIN_THREAD.change_online_game_state()

    # ==================== Funkcja klienta ====================
    def send_status(self, ready):
        # Wysyłanie do serwera statusu gotowości do gry
        msg = '$READY{}$'.format(ready)
        self.send_data(msg)

    def send_dir(self, dir):
        # Wysyłanie do serwera kierunku naszego agenta
        msg = '$DIR{}$'.format(dir)
        self.send_data(msg)

    def send_data(self, msg_out):
        # Wysyłanie do serwera wiadomości
        data_out = bytes(msg_out + '\n', 'utf-8')
        try:
            self.connection.sendall(data_out)
        except socket.error:
            self.close_connection()

    def close_connection(self):
        # Zamknięcie socketa i skończenie działania wątku
        self.is_running = False
        self.MAIN_THREAD.multiplayer_connection_error = True
        self.connection.close()

