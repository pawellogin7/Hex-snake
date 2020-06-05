import time
import os
import numpy as np

HEX_SIZE = 3


# ==================== Klasa planszy ====================
class Board:
    # Klasa planszy zawiera inforormacje o obecnym stanie gry - wszystkich pól planszy, agentów obecnych w grze itd.

    # ==================== Konstruktor ====================
    def __init__(self, height, width, players):
        self.height = height
        self.width = width
        self.players = players
        self.p1_alive = True
        self.p2_alive = True
        self.game_over = False
        self.board = []
        self.agents = []

    # ==================== Funkcje mechaniki gry ====================
    def restart_game(self, number_of_agents):
        # Funkcja restartująca grę, działa dla 1 lub 2 agentów
        self.p1_alive = True
        self.p2_alive = True
        self.game_over = False
        self.board = []
        for i in range(self.height):
            board_row = []
            for j in range(self.width):
                tile = Tile(j, i)
                board_row.append(tile)
            self.board.append(board_row)

        self.agents = []
        snake_len = 3
        new_snake = Agent(snake_len, 1, snake_len, 1, 1)
        for tile in new_snake.snake_array:
            self.board[tile[1]][tile[0]].type = 10 + new_snake.team
        self.agents.append(new_snake)
        if number_of_agents == 2:
            new_snake = Agent(self.width - snake_len - 1, self.height - 2, snake_len, 2, -1)
            for tile in new_snake.snake_array:
                self.board[tile[1]][tile[0]].type = 10 + new_snake.team
            self.agents.append(new_snake)
        for i in range(len(self.agents)):
            self.get_new_fruit()

    def get_new_fruit(self):
        # Funkcja losująca na planszy nowy owoc i zwracająca czy udało jej się to zrobić
        # (w przypadku całkowitego zapełnienia planszy nie da się wylosować owoca)
        tile_is_empty = False
        successful = True
        board_array = self.board_to_array()
        if np.sum((np.where(board_array == 0, 1, 0))) == 0:
            successful = False
        else:
            while tile_is_empty is False:
                pos_x = np.random.randint(self.width)
                pos_y = np.random.randint(self.height)
                if self.board[pos_y][pos_x].type == 0:
                    self.board[pos_y][pos_x].type = 2
                    self.board[pos_y][pos_x].fruit_type = np.random.randint(3)
                    tile_is_empty = True
        return successful

    def move_snake(self, id, get_new_fruit):
        # Funkcja poruszająca agenta o danym id na podstawie jego kieronku
        new_x = new_y = new_type = -1
        if self.p1_alive is True and id == 0:
            new_x, new_y, new_type = self.agents[id].get_next_move(self.board)
        elif self.p2_alive is True and id == 1:
            new_x, new_y, new_type = self.agents[id].get_next_move(self.board)
        if new_type == -1:
            if id == 0:
                self.p1_alive = False
            elif id == 1:
                self.p2_alive = False
            self.remove_snake(id)
        elif new_type == 0 or [new_x, new_y] == self.agents[id].snake_array[len(self.agents[id].snake_array) - 1]:
            self.board = self.agents[id].move(self.board, [new_x, new_y])
        elif new_type == 2:
            self.agents[id].fruit_eaten = True
            self.board = self.agents[id].move(self.board, [new_x, new_y])
            if get_new_fruit is True:
                self.get_new_fruit()
        else:
            if id == 0:
                self.p1_alive = False
            elif id == 1:
                self.p2_alive = False
            self.remove_snake(id)

    def move_snake_pos(self, id, pos, get_new_fruit):
        # Funkcja poruszająca agenta o danym id na konkretne pole
        new_x = pos[0]
        new_y = pos[1]
        new_type = self.board[new_y][new_x].type
        self.agents[id].change_dir(self.board, pos)
        if new_type == -1:
            if id == 0:
                self.p1_alive = False
            elif id == 1:
                self.p2_alive = False
            self.remove_snake(id)
        elif new_type == 0 or [new_x, new_y] == self.agents[id].snake_array[len(self.agents[id].snake_array) - 1]:
            self.board = self.agents[id].move(self.board, [new_x, new_y])
        elif new_type == 2:
            self.agents[id].fruit_eaten = True
            self.board = self.agents[id].move(self.board, [new_x, new_y])
            if get_new_fruit is True:
                self.get_new_fruit()
        else:
            if id == 0:
                self.p1_alive = False
            elif id == 1:
                self.p2_alive = False
            self.remove_snake(id)

    def remove_snake(self, id):
        # Funkcja usuwająca wszystkie pola danego agenta(w przypadku jego śmierci)
        while len(self.agents[id].snake_array) > 0:
            tile = self.agents[id].snake_array[0]
            self.agents[id].snake_array.pop(0)
            self.board[tile[1]][tile[0]].type = 0

    def remove_fruits(self):
        # Funkcja usuwająca wszystkie owoce na planszy(używana w grze online - informacje od owocach dostajemy z serwera)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].type == 2:
                    self.board[i][j].type = 0

    # ==================== Funkcje rysujące ====================
    def print_board_qt(self):
        # Funkcja zwracająca zmienna string, która wyświetla planszę na kontrolce QTextEdit
        width = self.width // 2 * 4 * (HEX_SIZE - 1) + self.width % 2 * (2 * HEX_SIZE - 2) + HEX_SIZE
        height = self.height * (2*HEX_SIZE - 2) + HEX_SIZE
        board_array = np.full((height, width), -2)
        for i in range(self.height):
            row = self.board[i]
            for j in range(self.width):
                tile = row[j]
                self.fill_hexagon(board_array, j, i, tile.type, False)
        if self.p1_alive is True:
            self.fill_hexagon(board_array, self.agents[0].snake_array[0][0], self.agents[0].snake_array[0][1],
                              10 + self.agents[0].team, True)
        if self.p2_alive is True:
            self.fill_hexagon(board_array, self.agents[1].snake_array[0][0], self.agents[1].snake_array[0][1],
                              10 + self.agents[1].team, True)

        info = "<span style=\" background-color:#ff0000;\" >  </span>"
        info += "Socket {}:{} is invalid. Closing connection."
        info += "</span>"
        board_str = ''
        for row in board_array:
            row_str = ''
            for tile_str in row:
                if tile_str == -10:
                    row_str += "<span style=\" color:#ffffff; background-color:#ffffff;\" >--</span>"
                if tile_str == -2:
                    row_str += "<span style=\" color:#ffffff; background-color:#ffffff;\" >--</span>"
                if tile_str == -1:
                    row_str += "<span style=\" color:#000000; background-color:#000000;\" >--</span>"
                elif tile_str == 0:
                    row_str += "<span style=\" color:#00ff00; background-color:#00ff00;\" >--</span>"
                elif tile_str == 1:
                    row_str += "<span style=\" color:#ff0000; background-color:#ff0000;\" >--</span>"
                elif tile_str == 2:
                    row_str += "<span style=\" color:#ff0000; background-color:#ff0000;\" >--</span>"
                elif tile_str == 11:
                    row_str += "<span style=\" color:#0000ff; background-color:#0000ff;\" >--</span>"
                elif tile_str == 12:
                    row_str += "<span style=\" color:#ff00ff; background-color:#ff00ff;\" >--</span>"
            board_str += row_str + '\n'
        return board_str

    def fill_hexagon(self, board_array, coord_x, coord_y, type, is_active):
        # Funkcja zapełniająca odpowiednie pola w zmiennej planszy, aby możliwe było narysowanie hexagonu
        start_x = coord_x // 2 * 4 * (HEX_SIZE - 1) + coord_x % 2 * (2 * HEX_SIZE - 2)
        start_y = coord_y * (2 * HEX_SIZE - 2) + coord_x % 2 * (HEX_SIZE - 1)
        wid = HEX_SIZE - 1
        wid_change = -1
        for i in range(2*HEX_SIZE - 1):
            for j in range(wid, (3*HEX_SIZE - 2) - wid, 1):
                if i == 0 or i == 2*HEX_SIZE - 2 or j == wid or j == (3*HEX_SIZE - 2) - wid - 1:
                    if is_active is False:
                        board_array[start_y + i, start_x + j] = -1
                    else:
                        board_array[start_y + i, start_x + j] = -10
                else:
                    board_array[start_y + i, start_x + j] = type
            if i == HEX_SIZE - 1:
                wid_change = 1
            wid += wid_change

    # ==================== Funkcje dodatkowe ====================
    def board_to_array(self):
        # Funkcja zwracająca planszę w postaci tablicy liczb
        self.height = len(self.board)
        self.width = len(self.board[0])
        board_array = np.zeros((self.height, self.width), dtype=np.int16)
        for i in range(self.height):
            for j in range(self.width):
                board_array[i, j] = self.board[i][j].type
        return board_array


# ==================== Klasa pola ====================
class Tile:
    # Klasa pola zawiera informację o danym polu na planszy - jego pozycja x i y, typ, typ owoca(obrazku), sąsiadów itd.

    # ==================== Konstruktor ====================
    def __init__(self, pos_x, pos_y):
        self.type = 0
        self.fruit_type = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.neighbours_up = []
        self.neighbours_down = []
        if pos_x % 2 == 0:
            self.neighbours_up = [[pos_x - 1, pos_y - 1], [pos_x, pos_y - 1], [pos_x + 1, pos_y - 1]]
            self.neighbours_down = [[pos_x - 1, pos_y], [pos_x, pos_y + 1], [pos_x + 1, pos_y]]
        else:
            self.neighbours_up = [[pos_x - 1, pos_y], [pos_x, pos_y - 1], [pos_x + 1, pos_y]]
            self.neighbours_down = [[pos_x - 1, pos_y + 1], [pos_x, pos_y + 1], [pos_x + 1, pos_y + 1]]

    # ==================== Funkcje dodatkowe ====================
    def get_neighbour(self, board, type, id):
        # Funkcja zwracająca pozycję x i y oraz typ sąsiada(jeśli taki istnieje) w danym kierunku
        height = len(board)
        width = len(board[0])
        if type == 'up':
            neighbour = self.neighbours_up[id]
            if -1 < neighbour[0] < width and -1 < neighbour[1] < height:
                return neighbour[0], neighbour[1], board[neighbour[1]][neighbour[0]].type
            else:
                return -1, -1, -1
        elif type == 'down':
            neighbour = self.neighbours_down[id]
            if -1 < neighbour[0] < width and -1 < neighbour[1] < height:
                return neighbour[0], neighbour[1], board[neighbour[1]][neighbour[0]].type
            else:
                return -1, -1, -1
        else:
            return -1, -1, -1

    def get_empty_neighbours(self, board):
        # Funkcja zwracająca wszystkich "pustych" sąsiadów pola(takich, na które może poruszyć się agent)
        empty_neighbours = []
        height = len(board)
        width = len(board[0])
        for neighbour in self.neighbours_up:
            if -1 < neighbour[0] < width and -1 < neighbour[1] < height:
                if board[neighbour[1]][neighbour[0]].type == 0:
                    empty_neighbours.append(neighbour)
        for neighbour in self.neighbours_down:
            if -1 < neighbour[0] < width and -1 < neighbour[1] < height:
                if board[neighbour[1]][neighbour[0]].type == 0:
                    empty_neighbours.append(neighbour)
        return empty_neighbours

    def get_neigh_dir(self, neigh):
        try:
            id_n = self.neighbours_up.index(neigh)
            dir = id_n
            return dir
        except ValueError:
            try:
                id_n = self.neighbours_down.index(neigh)
                dir = id_n + 3
                return dir
            except ValueError:
                return -1

# ==================== Klasa agenta ====================
class Agent:
    # Klasa agenta zawiera informacje o agencie - jego drużyna, położenie segmentów, obecny kierunek, ilość punktów itd.

    # ==================== Konstruktor ====================
    def __init__(self, pos_x, pos_y, start_length, team, start_direction):
        self.team = team
        self.player_type = 'human'
        self.points = 0
        self.fruit_eaten = False
        self.snake_array = []
        if start_direction == -1:
            self.direction = 0
            for i in range(start_length):
                self.snake_array.append([pos_x + i, pos_y])
        else:
            self.direction = 5
            for i in range(start_length):
                self.snake_array.append([pos_x - i, pos_y])

    # ==================== Dodatkowe funkcje ====================
    def get_next_move(self, board):
        # Funkcja zwraca typ sąsiada agenta, po wykonaniu ruchu w obecnym kierunku agenta
        head_x = self.snake_array[0][0]
        head_y = self.snake_array[0][1]
        neigh_x = neigh_y = neigh_type = -1
        if self.direction == 0:
            neigh_x, neigh_y, neigh_type = board[head_y][head_x].get_neighbour(board, 'up', 0)
        elif self.direction == 1:
            neigh_x, neigh_y, neigh_type = board[head_y][head_x].get_neighbour(board, 'up', 1)
        elif self.direction == 2:
            neigh_x, neigh_y, neigh_type = board[head_y][head_x].get_neighbour(board, 'up', 2)
        elif self.direction == 3:
            neigh_x, neigh_y, neigh_type = board[head_y][head_x].get_neighbour(board, 'down', 0)
        elif self.direction == 4:
            neigh_x, neigh_y, neigh_type = board[head_y][head_x].get_neighbour(board, 'down', 1)
        elif self.direction == 5:
            neigh_x, neigh_y, neigh_type = board[head_y][head_x].get_neighbour(board, 'down', 2)
        return neigh_x, neigh_y, neigh_type

    def move(self, board, new_pos):
        # Funkcja poruszająca agentem - zmienia ona odpowiednio tablicę segmentów węża agenta.
        # Najpierw poruszana jest głowa, a dopiero potem ogon, więc agent może poruszyć się głową na pole, gdzie
        # znajduje się jego ogon i nie doprowadzi to do jego śmierci.
        if self.fruit_eaten is True:
            self.fruit_eaten = False
            self.points += 1
        else:
            tail_x = self.snake_array[len(self.snake_array) - 1][0]
            tail_y = self.snake_array[len(self.snake_array) - 1][1]
            board[tail_y][tail_x].type = 0
            self.snake_array.pop()
        self.snake_array.insert(0, new_pos)
        board[new_pos[1]][new_pos[0]].type = 10 + self.team
        return board

    def change_dir(self, board, new_tile):
        head = self.snake_array[0]
        dir = board[head[1]][head[0]].get_neigh_dir(new_tile)
        if dir != -1:
            self.direction = dir







