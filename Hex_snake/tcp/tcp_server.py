import socket
from threading import Thread
import time
import numpy as np
import utils.snake_utilities as snake_utilities


BOARD_HEIGHT = 10
BOARD_WIDTH = 14


# ==================== Wątek serwera do gry online ====================
class SnakeServerThread(Thread):
    # Wątek serwera jest tworzony przez osobę hostującą grę. Oprócz tego tworzy ona również swój własny wątek klienta
    # SnakeClientThread. Serwer służy do odbierania informacji od klientów, odpowiedniego przetwarzania ich oraz
    # wysyłania klientom informacji o obecnym stanie gry.
    # Komunikacja odbywa się w nastepujący sposób:
    # 1. Serwer oczekuje na połączenie z graczem 1 oraz graczem 2(obaj gracze muszą się połączyć aby gra się zaczęła).
    # 2. Serwer oczekuje, aż obaj graczej klikną przycisk Ready, informując o swojej gotowości do gry.
    # 3. Serwer wysyła do graczy ramkę z informacją o obecnym stanie gry.
    # 4. Serwer oczekuje na otrzymanie od klientów informacji o kierunku ich agenta.
    # 5. Serwer porusza agentami graczy i sprawdza warunek końca gry. Jeśli nie jest on spełniony to cofa się do
    # kroku 3, w przeciwnym wypadku przechodzi do kroku 6.
    # 6. Przesłanie informacji o okńcu gry do obu graczy. Oczekiwanie aż oboje zapoznają się z końcowym wynikiem gry
    # i klikną przycisk Ready.
    # 7. Wysłanie do graczy żądania resetu gry. Przejście do kroku 2.
    # Rozwiązanie takie - przetwarzanie mechaniki gry na serwerze i wysyłanie wyłącznie stanu gry do klientów ma
    # swoje zdecydowane zalety - nie powinna wystąpic sytuacja, w której gracze w inny sposób przetworzą daną turę
    # gry, co dopradzić mogłoby do tego, że widzieliby oni na ekranie różne plansze.

    # ==================== Konstruktor ====================
    def __init__(self, ip, port):
        Thread.__init__(self)
        # Inicjalizacja serwera na określonym przez użytkownika adresie ip i porcie
        self.server_ip = ip
        self.server_port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_threads = []
        self.is_running = True
        self.game_board = snake_utilities.Board(BOARD_HEIGHT, BOARD_WIDTH, 2)
        self.game_board.restart_game(2)
        self.p1_connected = False
        self.p2_connected = False
        self.p1_move_dir = -1
        self.p2_move_dir = -1
        self.game_paused = True
        self.p1_ready = False
        self.p2_ready = False
        self.game_end = False

    # ==================== Funkcja run ====================
    def run(self):
        try:
            # Próba stworzenia serwera
            self.server.bind((self.server_ip, self.server_port))
        except socket.error:
            self.is_running = False

        while self.is_running:
            new_threads = []
            for thread in self.client_threads:
                # Usuwanie nieaktywnych klientów
                if thread.connection_error is True:
                    if thread.player_id == 1:
                        self.p1_connected = False
                    elif thread.player_id == 2:
                        self.p2_connected = False
                else:
                    new_threads.append(thread)
                self.client_threads = new_threads
            if self.p2_connected is False or self.p1_connected is False:
                # Nasłuchiwanie za klientami (kiedy albo gracz 1, albo gracz 2 nie są połączeni)
                self.server.listen(1)
                try:
                    # Dodawanie wątku dla nowego klienta
                    (connection, (ip, port)) = self.server.accept()
                    new_thread = ServerClientThread(self, ip, port, connection)
                    new_thread.start()
                    self.client_threads.append(new_thread)
                    time.sleep(0.1)
                    self.send_board_frame()
                except socket.error:
                    self.is_running = False
                time.sleep(1)
            elif self.p1_connected is True and self.p2_connected is True:
                # Wysyłanie informacji do klientów i odświeżanie stanu gry
                    if self.game_end is True:
                        # Koniec gry(oboje z agentów umarli)
                        if self.p1_ready is True and self.p2_ready is True:
                            # Czekanie na potwierdzenie gotowości przez obu graczy
                            self.game_end = False
                            self.restart_game()
                    elif self.game_paused is False:
                        # Gra jest w toku - odświeżenie stanu gry i wysłanie go do graczy
                        self.update_and_resend_board()
                    else:
                        # Początek gry - oczekiwanie na potwierdzenie gotowości przez obu graczy
                        if self.p1_ready is True:
                            p1_str = 'RDY{}/{}/'.format(1, 1)
                        else:
                            p1_str = 'RDY{}/{}/'.format(1, 0)
                        if self.p2_ready is True:
                            p2_str = 'RDY{}/{}/'.format(2, 1)
                        else:
                            p2_str = 'RDY{}/{}/'.format(2, 0)
                        msg = '$' + p1_str + '$' + p2_str + '$'
                        for thread in self.client_threads:
                            thread.send_data(msg)
                        if self.p1_ready is True and self.p2_ready is True:
                            # Kiedy obaj gracze potwierdzili gotowość wysyłamy do nich stan gry
                            # (żeby mogli nam odesłać kierunek swoich agentów)
                            self.game_paused = False
                            self.send_board_frame()
            time.sleep(0.01)

    # ==================== Funkcje odświeżania i rozsyłania stanu gry ====================
    def update_and_resend_board(self):
        # Funkcja odświeżająca stan gry
        if self.p1_move_dir > -1 and self.p2_move_dir > -1:
            # Przed odświeżeniem czekamy na informacje o kierunku agenta od obu graczy
            if self.game_paused is False:
                if self.game_board.p1_alive is True:
                    # Jeśli gracz 1 jest żywy to ruszamy go
                    self.game_board.agents[0].direction = self.p1_move_dir
                    self.game_board.move_snake(0, True)
                    self.p1_move_dir = -1
                if self.game_board.p2_alive is True:
                    # Jeśli gracz 2 jest żywy to ruszamy go
                    self.game_board.agents[1].direction = self.p2_move_dir
                    self.game_board.move_snake(1, True)
                    self.p2_move_dir = -1
                self.send_board_frame()
                if self.game_board.p1_alive is False and self.game_board.p2_alive is False:
                    # Jeśli oboje z graczy umarli to wywołujemy funkcję końca gry
                    self.game_over()

    def send_board_frame(self):
        # Funkcja wysyłająca do klientów ramkę informującą o stanie gry
        # Informacje o zawartości pól planszy oraz typie(obrazku) owoców
        board_array = self.game_board.board_to_array()
        board_str = 'BOARD'
        fruit_str = 'FRUIT'
        for i in range(len(board_array)):
            for j in range(len(board_array[0])):
                board_str += '{}/'.format(board_array[i][j])
                if self.game_board.board[i][j].type == 2:
                    fruit_str += '{}/{}/{}/'.format(j, i, self.game_board.board[i][j].fruit_type)
        # Informacje o graczu 1
        p1_str = 'P1'
        if self.game_board.p1_alive is True:
            p1_str += '1/'
            head = self.game_board.agents[0].snake_array[0]
            p1_str += '{}/{}/'.format(head[0], head[1])
            p1_str += '{}/'.format(self.game_board.agents[0].direction)
        else:
            p1_str += '0/'
            p1_str += '-1/-1/-1/'
        p1_str += '{}/'.format(self.game_board.agents[0].points)
        # Informacje o graczu 2
        p2_str = 'P2'
        if self.game_board.p2_alive is True:
            p2_str += '1/'
            head = self.game_board.agents[1].snake_array[0]
            p2_str += '{}/{}/'.format(head[0], head[1])
            p2_str += '{}/'.format(self.game_board.agents[1].direction)
        else:
            p2_str += '0/'
            p2_str += '-1/-1/-1/'
        p2_str += '{}/'.format(self.game_board.agents[1].points)
        # Zebranie informacji w całość i stworzenie ramki. Oddzielenie poszczególnych części wiadomości separatorem '$'
        msg = '$FRAME_START$' + board_str + '$' + fruit_str + '$' + p1_str + '$' + p2_str + '$FRAME_END$'
        for thread in self.client_threads:
            if thread.is_running is True:
                thread.send_data(msg)

    def game_over(self):
        # Funkcja odpowiadająca za obsługę końca gry i rozsyłania tej informacji do klientów
        for thread in self.client_threads:
            msg = '$END$'
            if thread.is_running is True:
                thread.send_data(msg)
        time.sleep(0.1)
        self.game_end = True
        self.p1_ready = False
        self.p2_ready = False

    def restart_game(self):
        # Funkcja odpowiadająca za obsługę restartu gry i rozsyłania informacji do klientów
        for thread in self.client_threads:
            msg = '$RDY1/0/$'
            msg += 'RDY1/0/$'
            msg += 'RST$'
            if thread.is_running is True:
                thread.send_data(msg)
        time.sleep(0.1)
        self.p1_ready = False
        self.p2_ready = False
        self.game_paused = True
        self.game_board.restart_game(2)
        self.send_board_frame()

    # ==================== Funkcje serwera ====================
    def stop_server(self):
        # Zatrzymanie serwera oraz wszystkich wątków klientów
        self.is_running = False
        for thread in self.client_threads:
            if thread.is_running is True:
                thread.close_connection()
        self.server.close()


# ==================== Wątek do obsługi klienta przez serwer ====================
class ServerClientThread(Thread):
    # Wątek ten jest tworzony przez serwer za każdym razem, jak połączy się z nowym klientem. Słuzy on do obsługi
    # komunikacji z tym klientem.

    # ==================== Konstruktor ====================
    def __init__(self, server_thread, ip, port, connection):
        Thread.__init__(self)
        self.server_thread = server_thread
        self.ip = ip
        self.port = port
        self.connection = connection
        self.is_running = False
        self.connection_error = False
        self.player_id = 0
        self.new_data_received = False

    # ==================== Funkcja run ====================
    def run(self):
        try:
            # Próba nawiązania połączenia z klientem. Odebranie informacji o jego indeksie(gracz 1 albo 2)
            self.send_data('Welcome to server! Send your player ID.')
            data_in = self.connection.recv(100)
            msg = data_in.decode()
            if msg.find('P1') != -1:
                self.player_id = 1
                self.server_thread.p1_connected = True
                self.send_data('ID correct. Connection established!')
                self.is_running = True
            elif msg.find('P2') != -1:
                self.player_id = 2
                self.server_thread.p2_connected = True
                self.send_data('ID correct. Connection established!')
                self.is_running = True
            else:
                self.connection_error = True
                self.connection.close()
        except (socket.error, UnicodeDecodeError):
            self.close_connection()

        # Wysyłanie do klienta żądanie resetu gry(konieczne w celu uniknięcia błędów)
        self.send_data('$RST$')

        while self.is_running is True:
            # Odbieranie wiadomości od klientów
            data_in = b''
            while self.is_running is True:
                try:
                    data_t = self.connection.recv(25000)
                    data_in += data_t
                    if len(data_t) < 25000:
                        break
                except socket.error:
                    self.is_running = False
                    self.connection_error = True
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
                if msg[0:3] == 'DIR':
                    # Informacja o kierunku agenta danego klienta
                    data = msg[3:].split('/')
                    try:
                        dir = int(data[0])
                        if self.player_id == 1:
                            self.server_thread.p1_move_dir = dir
                        elif self.player_id == 2:
                            self.server_thread.p2_move_dir = dir
                    except (IndexError, ValueError):
                        pass
                if msg[0:5] == 'READY':
                    # Informacja o gotowości klienta do gry
                    if self.player_id == 1:
                        self.server_thread.p1_ready = True
                    elif self.player_id == 2:
                        self.server_thread.p2_ready = True

    # ==================== Funkcje klienta ====================
    def send_data(self, msg_out):
        # Funkcja wysyłająca wiadomość do klienta
        data_out = bytes(msg_out + '\n', 'utf-8')
        try:
            self.connection.sendall(data_out)
        except socket.error:
            self.close_connection()

    def close_connection(self):
        # Funkcja zamykająca socket klienta i informująca o tym serwer
        self.is_running = False
        self.connection_error = True
        self.connection.close()
        if self.player_id == 1:
            self.server_thread.p1_connected = False
        elif self.player_id == 2:
            self.server_thread.p2_connected = False
        self.server_thread.restart_game()





