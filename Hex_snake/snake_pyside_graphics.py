from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import time
import threading
import json
import numpy as np
import utils.snake_utilities as snake_utilities
import utils.keyboard_listener as keyboard_listener
import res.resources as resources
import utils.replay as replay
import utils.bot as bot
import gui.snake_gui_graphics as snake_gui
from tcp.tcp_client import SnakeClientThread
from tcp.tcp_server import SnakeServerThread


FPS = 3
BOARD_HEIGHT = 10
BOARD_WIDTH = 14
TILE_IMG_SIZE = 64


# ==================== Klasa głownego okna gry ====================
class MainWindow(QMainWindow):
    # ==================== Konstruktor ====================
    def __init__(self):
        super(MainWindow, self).__init__()
        # inicjalizacja UI
        self.ui = snake_gui.Ui_SnakeGame()
        self.ui.setupUi(self)
        # inicjalizacja zmiennych
        self.game_board = snake_utilities.Board(BOARD_HEIGHT, BOARD_WIDTH, 2)
        self.game_paused = True
        self.game_is_running = True
        self.first_round = True
        self.replay = False
        self.game_with_bot = False
        self.multiplayer = False
        self.multiplayer_connection_error = False
        self.host = True
        self.connected = False
        self.server_ip = 'localhost'
        self.server_port = 6000
        # inicjalizacja dodatkowych klas
        self.key_listener = keyboard_listener.KeyboardListenerThread()
        self.multiplayer_server = SnakeServerThread(self.server_ip, self.server_port)
        self.multiplayer_client = SnakeClientThread(self, self.server_ip, self.server_port, 1)
        self.replay_player = replay.Replay()
        self.snake_bot = bot.Bot()
        # Event używany do sprawdzania, czy połączenie z serwerem zostało nawiązane
        self.client_thread_event = threading.Event()
        # wczytywanie obrazów
        self.pixmap_empty = QPixmap(":/images/empty_tile.png")
        self.pixmap_empty = self.pixmap_empty.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
        self.pixmap_list_fruits = []
        pixmap = QPixmap(":/images/fruits/apple_tile.png")
        pixmap = pixmap.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
        self.pixmap_list_fruits.append(pixmap)
        pixmap = QPixmap(":/images/fruits/pear_tile.png")
        pixmap = pixmap.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
        self.pixmap_list_fruits.append(pixmap)
        pixmap = QPixmap(":/images/fruits/cherry_tile.png")
        pixmap = pixmap.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
        self.pixmap_list_fruits.append(pixmap)
        self.pixmap_snake_blue = QPixmap(":/images/snake_blue/snake_blue_tile.png")
        self.pixmap_snake_blue = self.pixmap_snake_blue.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
        self.pixmap_snake_pink = QPixmap(":/images/snake_pink/snake_pink_tile.png")
        self.pixmap_snake_pink = self.pixmap_snake_pink.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
        self.pixmap_list_blue_head = []
        self.pixmap_list_pink_head = []
        for i in range(6):
            pixmap = QPixmap(":/images/snake_blue/snake_blue_head_dir{}.png".format(i))
            pixmap = pixmap.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
            self.pixmap_list_blue_head.append(pixmap)
            pixmap = QPixmap(":/images/snake_pink/snake_pink_head_dir{}.png".format(i))
            pixmap = pixmap.scaled(TILE_IMG_SIZE, TILE_IMG_SIZE, Qt.KeepAspectRatio)
            self.pixmap_list_pink_head.append(pixmap)
        self.board_scene = QGraphicsScene()
        # inicjalizacja elementów UI
        self.ui.btn_pause.clicked.connect(self.click_btn_pause)
        self.ui.btn_restart.clicked.connect(self.click_btn_restart)
        self.ui.btn_exit.clicked.connect(self.click_btn_exit)
        self.ui.btn_connect.clicked.connect(self.change_online_connection)
        self.ui.load_replay_btn.clicked.connect(self.load_replay)
        self.ui.save_replay_btn.clicked.connect(self.save_replay)
        self.ui.ip_textbox.textChanged.connect(self.textbox_ip_changed)
        self.ui.port_textbox.textChanged.connect(self.textbox_port_changed)
        self.ui.combo_game_type.currentIndexChanged.connect(self.combo_game_mode_changed)
        self.ui.combo_online.currentIndexChanged.connect(self.combo_conn_mode_changed)
        self.ui.p1_gBox.setStyleSheet('QGroupBox:title {color: rgb(0, 0, 255);}')
        self.ui.p2_gBox.setStyleSheet('QGroupBox:title {color: rgb(255, 0, 255);}')
        self.ui.conn_status_textbox.setStyleSheet("color: yellow; background-color: red")
        bold_font = QFont()
        bold_font.setBold(True)
        self.ui.conn_status_textbox.setFont(bold_font)
        self.only_int_val = QIntValidator()
        self.ui.port_textbox.setValidator(self.only_int_val)
        # wczytanie zapisanych opcji z pliku
        self.load_options_file()
        # timer odpowiadający za odświeżanie planszy i wykonywanie ruchu
        self.multi_new_frame = False
        self.multi_update = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer_multi = QTimer(self)
        self.timer_multi.timeout.connect(self.multi_check_new_frame)
        self.start_game()

    # ==================== Funkcje gry ====================
    def start_game(self):
        # Funkcja restartująca grę (w tym planszę, agentów itd.)
        self.game_paused = True
        self.game_is_running = True
        self.first_round = True
        self.replay_player.curr_frame_id = 0
        self.game_board.restart_game(2)
        if self.replay is False:
            self.replay_player.temp_replay_array = []
            self.replay_player.add_board_frame(self.game_board)
        if self.replay is True and len(self.replay_player.replay_array) > 0:
            frame = self.replay_player.get_curr_frame()
            self.change_replay_game_state(frame)
        self.update_board_scene()

    def run(self):
        # Funkcja wywoływana przez QTimer(w przypadku lokalnej gry,).
        # Odpowiada ona za zmianę stanu gry oraz odświeżanie planszy.
        if self.multiplayer is False:
            if self.game_board.game_over is True:
                if self.replay is False:
                    self.ui.btn_pause.setText('New game')
                else:
                    self.ui.btn_pause.setText('Restart replay')
                if self.replay is False:
                    self.replay_player.replay_array = self.replay_player.temp_replay_array
                self.update_board_scene()
            elif self.game_paused is False:
                if self.replay is True:
                    if self.replay_player.curr_frame_id < len(self.replay_player.replay_array):
                        replay_frame = self.replay_player.get_curr_frame()
                        self.change_replay_game_state(replay_frame)
                    else:
                        self.game_board.p1_alive = False
                        self.game_board.p2_alive = False
                        self.game_board.remove_snake(0)
                        self.game_board.remove_snake(1)
                        self.game_board.game_over = True
                if self.game_board.p1_alive is True:
                    if self.replay is False:
                        self.change_dir_player1()
                        self.game_board.move_snake(0, True)
                    else:

                        self.game_board.move_snake(0, False)
                if self.game_board.p2_alive is True:
                    if self.replay is False:
                        if self.game_with_bot is False:
                            self.change_dir_player2()
                            self.game_board.move_snake(1, True)
                        else:
                            self.get_bot_move_route()
                            self.move_bot()
                    else:
                        self.game_board.move_snake(1, False)
                if self.replay is False:
                    self.replay_player.add_board_frame(self.game_board)
                self.update_board_scene()
                if self.game_board.p1_alive is False and self.game_board.p2_alive is False:
                    self.update_board_scene()
                    self.game_board.game_over = True
                    if self.replay is False:
                        self.ui.btn_pause.setText('New game')
                    else:
                        self.ui.btn_pause.setText('Restart replay')
                    self.game_is_running = False
                    self.game_paused = True

    # ==================== Funkcje bota ====================
    def get_bot_move_route(self):
        board_array = self.game_board.board_to_array()
        head = self.game_board.agents[1].snake_array[0]
        fruits = np.where(board_array == 2)
        route = []
        for f_id in range(0, len(fruits[0]), 1):
            fruit = [int(fruits[1][f_id]), int(fruits[0][f_id])]
            route_valid, new_route = self.snake_bot.get_route_A_algorithm(board_array, head, fruit)
            if route_valid is True and (len(route) == 0 or len(new_route) < len(route)):
                route = new_route
        if len(route) > 0:
            self.snake_bot.move_route = route
        else:
            self.snake_bot.random_move(self.game_board.board, self.game_board.agents[1].snake_array[0])

    def move_bot(self):
        neigh = self.snake_bot.get_next_move(self.game_board.agents[1].snake_array[0])
        if neigh[0] != -1:
            self.game_board.move_snake_pos(1, neigh, True)
        else:
            self.game_board.move_snake(1, True)

    # ==================== Funkcje online multiplayer ====================
    def multi_check_new_frame(self):
        # Funkcja sprawdzająca, czy przyszły nowe inforlacje z serwera i odpowiednio odświeżająca GUI
        if self.host is True:
            if self.multiplayer_server.p2_connected is True:
                self.ui.conn_status_textbox.setStyleSheet("color: black; background-color: rgb(0, 255, 0);")
                self.ui.conn_status_textbox.setText("Connected")
            else:
                self.ui.conn_status_textbox.setStyleSheet("color: yellow; background-color: red")
                self.ui.conn_status_textbox.setText("Not connected")
        if self.multiplayer_connection_error is True:
            self.end_multi_connection()
        elif self.multiplayer_client.game_over is True:
            self.multiplayer_client.game_over = False
            self.game_board.game_over = True
            self.ui.btn_pause.setText('New game')
            self.update_board_scene()
        elif self.multiplayer_client.reset is True:
            self.multiplayer_client.reset = False
            self.ui.btn_pause.setText('Ready')
            self.start_game()
        elif self.multi_new_frame is True:
            self.multi_new_frame = False
            self.timer.singleShot(int(1000 / FPS) + self.timer.remainingTime(), self.run_multiplayer)
        elif self.multi_update is True:
            self.multi_update = False
            self.update_board_scene()
        elif self.host is True and self.multiplayer_server.p2_connected is False:
            self.update_board_scene()

    def change_online_game_state(self):
        # Funkcja, wywoływana przez klienta gry, która powoduje przekazanie informacji o nowym stanie gry, gdy dostaniemy
        # taki od serwera (nowa plansza, informacje o agentach i owocach)
        # Zamienia ona ramkę otrzymaną od serwera na odpowiednie wartości na planszy oraz w kontrolkach GUI.
        try:
            self.game_paused = False
            board_array = self.multiplayer_client.board_array
            fruits = self.multiplayer_client.fruit_array
            p1_state = self.multiplayer_client.p1_state
            p2_state = self.multiplayer_client.p2_state
            # Zmiana wartości planszy
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    self.game_board.board[i][j].type = int(board_array[i*BOARD_WIDTH + j])
            fruit1 = [int(fruits[0]), int(fruits[1]), int(fruits[2])]
            fruit2 = [int(fruits[3]), int(fruits[4]), int(fruits[5])]
            self.game_board.board[fruit1[1]][fruit1[0]].fruit_type = fruit1[2]
            self.game_board.board[fruit2[1]][fruit2[0]].fruit_type = fruit2[2]
            # Zmiana wartości graczy
            if int(p1_state[0]) == 1:  # P1
                self.game_board.p1_alive = True
            elif int(p1_state[0]) == 0:
                self.game_board.p1_alive = False
            if self.game_board.p1_alive is True:
                self.game_board.agents[0].snake_array[0] = [int(p1_state[1]), int(p1_state[2])]
                if self.host is False:
                    self.game_board.agents[0].direction = int(p1_state[3])
            self.game_board.agents[0].points = int(p1_state[4])
            if int(p2_state[0]) == 1:  # P2
                self.game_board.p2_alive = True
            elif int(p2_state[0]) == 0:
                self.game_board.p2_alive = False
            if self.game_board.p2_alive is True:
                self.game_board.agents[1].snake_array[0] = [int(p2_state[1]), int(p2_state[2])]
                if self.host is True:
                    self.game_board.agents[1].direction = int(p2_state[3])
            self.game_board.agents[1].points = int(p2_state[4])
            self.multi_new_frame = True
        except (IndexError, ValueError):
            pass

    def run_multiplayer(self):
        # Funkcja wysyłająca do serwera informację o kierunku węża gracza(w przypadku otrzymania od serwera nowej klatki)
        self.update_board_scene()
        self.update_game_state_text()
        if self.game_paused is False:
            self.change_dir_player1()
            if self.host is True:
                self.multiplayer_client.send_dir(self.game_board.agents[0].direction)
            else:
                self.multiplayer_client.send_dir(self.game_board.agents[1].direction)

    def end_multi_connection(self):
        # Zakończenie połączenia w grze online, zamknięcie socketa klienta(oraz serwera w przypadku hosta)
        self.timer_multi.stop()
        self.connected = False
        if self.host is True:
            self.ui.btn_connect.setText('Start server')
            self.multiplayer_server.stop_server()
        else:
            self.ui.btn_connect.setText('Join server')
        self.multiplayer_client.close_connection()
        self.multiplayer_connection_error = False
        if self.replay is False:
            self.ui.btn_pause.setText('Unpause game')
            self.ui.btn_restart.setText('Restart game')
        else:
            self.ui.btn_pause.setText('Unpause replay')
            self.ui.btn_restart.setText('Restart replay')
        self.ui.conn_status_textbox.setStyleSheet("color: yellow; background-color: red")
        self.ui.conn_status_textbox.setText("Not connected")
        self.start_game()

    # ==================== Funkcje replay playera ====================
    def change_replay_game_state(self, frame):
        try:
            fruits = frame[0]
            p1_state = frame[1]
            p2_state = frame[2]
            # Zmiana wartości planszy
            self.game_board.remove_fruits()
            fruit1 = [int(fruits[0]), int(fruits[1]), int(fruits[2])]
            fruit2 = [int(fruits[3]), int(fruits[4]), int(fruits[5])]
            self.game_board.board[fruit1[1]][fruit1[0]].type = 2
            self.game_board.board[fruit2[1]][fruit2[0]].type = 2
            self.game_board.board[fruit1[1]][fruit1[0]].fruit_type = fruit1[2]
            self.game_board.board[fruit2[1]][fruit2[0]].fruit_type = fruit2[2]
            # Zmiana wartości graczy
            self.game_board.agents[0].direction = int(p1_state[0])
            self.game_board.agents[0].points = int(p1_state[1])
            self.game_board.agents[1].direction = int(p2_state[0])
            self.game_board.agents[1].points = int(p2_state[1])
        except (IndexError, ValueError):
            pass

    # ==================== Funkcje rysujące/odświeżające GUI ====================
    def update_board_scene(self):
        # Funkcja odpowiadająca za rysowanie planszy wyświetlanej w QGraphicsView za pomocą QGraphicsScene.
        # Wyświetla ona również napisy informujące o stanie gry(np. który graz wygrał, kiedy gra się skończyła)
        self.board_scene = QGraphicsScene()
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                pixmap = self.pixmap_empty
                if self.game_board.board[i][j].type == 2:
                    fruit_type = self.game_board.board[i][j].fruit_type
                    pixmap = self.pixmap_list_fruits[fruit_type]
                elif self.game_board.board[i][j].type == 11:
                    if self.game_board.agents[0].snake_array[0] == [j, i]:
                        snake_dir = self.game_board.agents[0].direction
                        pixmap = self.pixmap_list_blue_head[snake_dir]
                    else:
                        pixmap = self.pixmap_snake_blue
                elif self.game_board.board[i][j].type == 12:
                    if self.game_board.agents[1].snake_array[0] == [j, i]:
                        snake_dir = self.game_board.agents[1].direction
                        pixmap = self.pixmap_list_pink_head[snake_dir]
                    else:
                        pixmap = self.pixmap_snake_pink
                g_item = QGraphicsPixmapItem()
                g_item.setPixmap(pixmap)
                x_pos = j // 2 * 2 * (int(TILE_IMG_SIZE * 0.75)) + (j % 2) * (int(TILE_IMG_SIZE * 0.75))
                y_pos = i * TILE_IMG_SIZE + (j % 2) * (int(TILE_IMG_SIZE * 0.5))
                g_item.setPos(x_pos, y_pos)
                self.board_scene.addItem(g_item)
        if self.connected is True and self.host is True and self.multiplayer_server.p2_connected is False:
            g_item = QGraphicsTextItem()
            g_item.setPlainText("Waiting for other player to join...")
            g_item.setDefaultTextColor(QColor(255, 0, 0))
            font = QFont()
            font.setPixelSize(30)
            g_item.setFont(font)
            rect = g_item.boundingRect()
            g_item.setPos((self.board_scene.width() - rect.width()) / 2,
                          (self.board_scene.height() - rect.height()) / 2)
            self.board_scene.addItem(g_item)
        elif self.connected is True and self.multiplayer_client.game_over_waiting is True:
            str = "Game over! Waiting for other player..."
            g_item = QGraphicsTextItem()
            g_item.setPlainText(str)
            g_item.setDefaultTextColor(QColor(255, 0, 0))
            font = QFont()
            font.setPixelSize(30)
            g_item.setFont(font)
            rect = g_item.boundingRect()
            g_item.setPos((self.board_scene.width() - rect.width()) / 2,
                          (self.board_scene.height() - rect.height()) / 2)
            self.board_scene.addItem(g_item)
        elif self.game_board.game_over is True:
            str = "Game over! "
            if self.game_board.agents[0].points > self.game_board.agents[1].points:
                str += "P1 has won!"
            elif self.game_board.agents[1].points > self.game_board.agents[0].points:
                str += "P2 has won!"
            else:
                str += "Its a tie!"
            g_item = QGraphicsTextItem()
            g_item.setPlainText(str)
            g_item.setDefaultTextColor(QColor(255, 0, 0))
            font = QFont()
            font.setPixelSize(30)
            g_item.setFont(font)
            rect = g_item.boundingRect()
            g_item.setPos((self.board_scene.width() - rect.width()) / 2,
                          (self.board_scene.height() - rect.height()) / 2)
            self.board_scene.addItem(g_item)
        elif self.multiplayer is True and self.connected is True:
            draw_string = False
            g_item = QGraphicsTextItem()
            if self.host is True:
                if self.multiplayer_client.p1_ready is False:
                    g_item.setPlainText("You are not ready!")
                    draw_string = True
                elif self.multiplayer_client.p2_ready is False:
                    g_item.setPlainText("Waiting for other player...")
                    draw_string = True
            else:
                if self.multiplayer_client.p2_ready is False:
                    g_item.setPlainText("You are not ready!")
                    draw_string = True
                elif self.multiplayer_client.p1_ready is False:
                    g_item.setPlainText("Waiting for other player...")
                    draw_string = True
            if draw_string is True:
                g_item.setDefaultTextColor(QColor(255, 0, 0))
                font = QFont()
                font.setPixelSize(30)
                g_item.setFont(font)
                rect = g_item.boundingRect()
                g_item.setPos((self.board_scene.width() - rect.width()) / 2, (self.board_scene.height() - rect.height()) / 2)
                self.board_scene.addItem(g_item)
        self.ui.gView_board.setScene(self.board_scene)
        self.update_game_state_text()

    def update_game_state_text(self):
        # Funkcja odświeżająca informacje o stanie gry w kontrolce Textedit(np. który gracz wygrywa)
        text = ''
        if self.game_board.p1_alive is True and self.game_board.p2_alive is True:
            text += 'Both players are alive\n'
        elif self.game_board.p1_alive is True:
            text += 'Player 1 is alive\n'
        elif self.game_board.p2_alive is True:
            text += 'Player 2 is alive\n'
        else:
            text += 'Game over!\n'
        if self.game_board.p1_alive is False and self.game_board.p2_alive is False:
            if self.game_board.agents[0].points > self.game_board.agents[1].points:
                text += 'Player 1 has won!'
            elif self.game_board.agents[0].points < self.game_board.agents[1].points:
                text += 'Player 2 has won!'
            else:
                text += 'Game has ended in a tie!!'
        else:
            if self.game_board.agents[0].points > self.game_board.agents[1].points:
                text += 'Player 1 is winning'
            elif self.game_board.agents[0].points < self.game_board.agents[1].points:
                text += 'Player 2 is winning'
            else:
                text += 'Its a tie'
        self.ui.game_state_textbox.setText(text)
        self.ui.p1_points_textbox.setText(str(self.game_board.agents[0].points))
        self.ui.p2_points_textbox.setText(str(self.game_board.agents[1].points))

    # ==================== Funkcje klawiatury ====================
    def change_dir_player1(self):
        # Funkcja zmieniająca kierunek węża gracza 1(oraz gracza 2 w przypadku gry online)
        # Przyjmowane klawisze: q, w, e, a, s, d
        command = self.key_listener.key_pressed_p1
        self.key_listener.key_pressed_p1 = ''
        p1_dir = -1
        if self.multiplayer is True and self.host is False:
            p_id = 1
        else:
            p_id = 0
        if command == 'q':
            if self.game_board.agents[p_id].direction != 5:
                p1_dir = 0
        elif command == 'w':
            if self.game_board.agents[p_id].direction != 4:
                p1_dir = 1
        elif command == 'e':
            if self.game_board.agents[p_id].direction != 3:
                p1_dir = 2
        elif command == 'a':
            if self.game_board.agents[p_id].direction != 2:
                p1_dir = 3
        elif command == 's':
            if self.game_board.agents[p_id].direction != 1:
                p1_dir = 4
        elif command == 'd':
            if self.game_board.agents[p_id].direction != 0:
                p1_dir = 5
        if self.multiplayer is False:
            if p1_dir != -1:
                self.game_board.agents[p_id].direction = p1_dir
            elif self.first_round is True:
                self.first_round = False
                self.game_board.agents[p_id].direction = 5
        else:
            if self.host is True:
                if self.first_round is True:
                    self.first_round = False
                    self.game_board.agents[p_id].direction = 5
                elif p1_dir != -1:
                    self.game_board.agents[p_id].direction = p1_dir
            else:
                if self.first_round is True:
                    self.first_round = False
                    self.game_board.agents[p_id].direction = 0
                elif p1_dir != -1:
                    self.game_board.agents[p_id].direction = p1_dir

    def change_dir_player2(self):
        # Funkcja zmieniająca kierunek węża gracza 2(tylko w przypadku gry lokalnej
        # Przyjmowane klawisze: u, i, o, j, k, l
        if self.multiplayer is False:
            command = self.key_listener.key_pressed_p2
            self.key_listener.key_pressed_p2 = ''
            if command == 'u':
                if self.game_board.agents[1].direction != 5:
                    self.game_board.agents[1].direction = 0
            elif command == 'i':
                if self.game_board.agents[1].direction != 4:
                    self.game_board.agents[1].direction = 1
            elif command == 'o':
                if self.game_board.agents[1].direction != 3:
                    self.game_board.agents[1].direction = 2
            elif command == 'j':
                if self.game_board.agents[1].direction != 2:
                    self.game_board.agents[1].direction = 3
            elif command == 'k':
                if self.game_board.agents[1].direction != 1:
                    self.game_board.agents[1].direction = 4
            elif command == 'l':
                if self.game_board.agents[1].direction != 0:
                    self.game_board.agents[1].direction = 5
        if self.first_round is True:
            self.first_round = False
            self.game_board.agents[1].direction = 0

    # ==================== Funkcje kontrolek GUI ====================
    def click_btn_pause(self):
        # Przycisk pauzy/nowej gry/gotowości(gra online)
        if self.multiplayer is False:
            if self.game_is_running is False:
                if self.replay is False:
                    self.ui.btn_pause.setText('Unpause game')
                else:
                    self.ui.btn_pause.setText('Unpause replay')
                self.start_game()
            else:
                if self.game_paused is True:
                    self.key_listener.key_pressed_p1 = ''
                    self.key_listener.key_pressed_p2 = ''
                    self.game_paused = False
                    self.timer.timeout.disconnect()
                    self.timer = QTimer(self)
                    self.timer.timeout.connect(self.run)
                    self.timer.start(int(1000 / FPS))
                    if self.replay is False:
                        self.ui.btn_pause.setText('Pause game')
                    else:
                        self.ui.btn_pause.setText('Pause replay')
                else:
                    self.game_paused = True
                    if self.replay is False:
                        self.ui.btn_pause.setText('Unpause game')
                    else:
                        self.ui.btn_pause.setText('Unpause replay')
                    self.timer.stop()
        else:
            if self.game_board.game_over is True:
                self.multiplayer_client.game_over_waiting = True
                self.update_board_scene()
            self.multiplayer_client.send_status(1)

    def click_btn_restart(self):
        # Przycisk restartu gry(gra lokalna)
        if self.multiplayer is False:
            self.start_game()
            if self.replay is False:
                self.ui.btn_pause.setText('Unpause game')
            else:
                self.ui.btn_pause.setText('Unpause replay')

    def click_btn_exit(self):
        # Przycisk wyjścia z programu
        self.multiplayer_server.stop_server()
        self.multiplayer_client.close_connection()
        self.timer.stop()
        self.timer_multi.stop()
        exit(0)

    def combo_game_mode_changed(self):
        # Combobox wyboru trybu gry (lokalna/online)
        if self.ui.combo_game_type.currentIndex() == 0 or self.ui.combo_game_type.currentIndex() == 1:
            self.multiplayer_connection_error = True
            self.ui.btn_pause.setText('Unpause game')
            self.ui.btn_restart.setText('Restart game')
            self.multiplayer = False
            self.replay = False
            self.game_paused = True
            if self.ui.combo_game_type.currentIndex() == 0:
                self.game_with_bot = False
            else:
                self.game_with_bot = True
            self.timer.stop()
        elif self.ui.combo_game_type.currentIndex() == 2:
            self.multiplayer = True
            self.replay = False
            self.game_paused = True
            self.game_with_bot = False
            self.timer.stop()
            self.ui.btn_pause.setText('Ready')
            self.ui.btn_restart.setText('-----')
        elif self.ui.combo_game_type.currentIndex() == 3:
            self.multiplayer_connection_error = True
            self.multiplayer = False
            self.replay = True
            self.game_with_bot = False
            self.ui.btn_pause.setText('Unpause replay')
            self.ui.btn_restart.setText('Restart replay')
            self.start_game()
        self.update_options_file()

    def combo_conn_mode_changed(self):
        # Combobox wyboru trybu połączenia gry online(czy hostujemy grę, czy dołączamy do stworzonego serwera)
        if self.ui.combo_online.currentIndex() == 0:
            self.host = True
            if self.connected is False:
                self.ui.btn_connect.setText('Start server')
        elif self.ui.combo_online.currentIndex() == 1:
            self.host = False
            if self.connected is False:
                self.ui.btn_connect.setText('Join server')
        self.update_options_file()

    def textbox_ip_changed(self):
        # Linedit adresu IP serwera
        self.server_ip = self.ui.ip_textbox.text()
        self.update_options_file()

    def textbox_port_changed(self):
        # Linedit portu serwera
        try:
            self.server_port = int(self.ui.port_textbox.text())
            self.update_options_file()
        except ValueError:
            pass

    def change_online_connection(self):
        # Prycisk połączenia/zakończenia połączenia w grze online
        self.timer.stop()
        if self.multiplayer:
            if self.connected is False:
                self.connected = True
                self.multiplayer_connection_error = False
                if self.host is True:
                    self.multiplayer_server = SnakeServerThread(self.server_ip, self.server_port)
                    self.multiplayer_server.start()
                    time.sleep(0.1)
                    self.multiplayer_client = SnakeClientThread(self, self.server_ip, self.server_port, 1)
                    self.multiplayer_client.start()
                else:
                    self.multiplayer_client = SnakeClientThread(self, self.server_ip, self.server_port, 2)
                    self.multiplayer_client.start()
                time.sleep(0.1)
                self.timer_multi.timeout.disconnect()
                self.timer_multi = QTimer(self)
                self.timer_multi.timeout.connect(self.multi_check_new_frame)
                self.timer_multi.start(20)
                if self.multiplayer_client.is_running is False:
                    self.multiplayer_connection_error = True
                    self.connected = False
                    self.ui.game_state_textbox.setText("Could not connect to server")
                else:
                    self.ui.btn_connect.setText('Disconnect')
                    self.ui.game_state_textbox.setText("Connection with server established")
                    if self.host is False:
                        self.ui.conn_status_textbox.setStyleSheet("color: black; background-color: rgb(0, 255, 0);")
                        self.ui.conn_status_textbox.setText("Connected")
            else:
                self.multiplayer_connection_error = True

    # ==================== Funkcje zapisu/odczytu ====================
    def save_replay(self):
        filename, _ = QFileDialog.getSaveFileName()
        if filename:
            if len(filename) < 5:
                filename += '.xml'
            elif filename[-4:] != '.xml':
                filename += '.xml'
            self.replay_player.save_replay(filename)

    def load_replay(self):
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            if len(filename) > 4:
                if filename[-4:] == '.xml':
                    self.replay_player.load_replay(filename)
                    self.start_game()
                    self.ui.btn_pause.setText('Unpause replay')

    def load_options_file(self):
        try:
            with open('config/options.json') as f:
                options = json.load(f)
                self.ui.ip_textbox.setText(options['server ip'])
                self.ui.port_textbox.setText(options['server port'])
                self.ui.combo_game_type.setCurrentIndex(int(options['game combo']))
                self.ui.combo_online.setCurrentIndex(int(options['connection combo']))
                f.close()
        except (FileNotFoundError, KeyError, ValueError):
            pass

    def update_options_file(self):
        options = {}
        options['server ip'] = self.server_ip
        options['server port'] = str(self.server_port)
        options['game combo'] = str(self.ui.combo_game_type.currentIndex())
        options['connection combo'] = str(self.ui.combo_online.currentIndex())
        with open('config/options.json', 'w+') as f:
            json.dump(options, f)
            f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())



