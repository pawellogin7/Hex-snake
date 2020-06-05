import numpy as np


class Bot:
    def __init__(self):
        self.initialized = False
        self.p1_is_dead = False
        self.move_route = []

    def get_next_move(self, snake_head):
        if len(self.move_route) > 1:
            try:
                move_id = self.move_route.index(snake_head)
                if move_id == len(self.move_route) - 1:
                    move_id = 0
                else:
                    move_id += 1
                return self.move_route[move_id]
            except ValueError:
                return [-1, -1]
        else:
            return [-1, -1]

    def random_move(self, board, head):
        neighbours = board[head[1]][head[0]].get_empty_neighbours(board)
        if len(neighbours) > 0:
            move_id = np.random.randint(len(neighbours))
            route = []
            route.append(head)
            route.append(neighbours[move_id])
            self.move_route = route
        else:
            self.move_route = []

    def get_route_A_algorithm(self, board, start_point, end_point):
        open_set = []
        closed_set = []
        g = np.zeros_like(board)
        h = np.zeros_like(board)
        f = np.full_like(board, 1000)
        came_from = np.full((board.shape[0], board.shape[1], 2), -1)
        open_set.append(start_point)
        g_n, h_n, f_n = self.A_algorithm_get_vals(start_point, end_point, 0)
        g[open_set[0][1], open_set[0][0]] = g_n
        h[open_set[0][1], open_set[0][0]] = h_n
        f[open_set[0][1], open_set[0][0]] = f_n
        while len(open_set) > 0:
            min_f = np.where(f == np.min(f))
            if len(min_f[0]) > 1:
                min_f = [min_f[0][0], min_f[1][0]]
            point = [int(min_f[1]), int(min_f[0])]
            if point == end_point:
                route = self.A_algorithm_reconstruct_route(came_from, end_point)
                return True, route
            f[point[1], point[0]] = 1000
            try:
                open_set.remove(point)
            except ValueError:
                return False, []
            closed_set.append(point)
            if point[0] % 2 == 0:
                x = point[0]
                y = point[1]
                neighbours = [[x - 1, y - 1], [x, y - 1], [x, y + 1],
                              [x - 1, y], [x, y - 1], [x + 1, y]]
            else:
                x = point[0]
                y = point[1]
                neighbours = [[x - 1, y], [x, y - 1], [x + 1, y],
                              [x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]
            new_neighbours = []
            for neigh in neighbours:
                if 0 <= neigh[0] < len(board[0]) and 0 <= neigh[1] < len(board):
                    try:
                        closed_set.index(neigh)
                    except ValueError:
                        if board[neigh[1]][neigh[0]] == 0 or board[neigh[1]][neigh[0]] == 2:
                            new_neighbours.append(neigh)
            neighbours = new_neighbours
            for neigh in neighbours:
                g_curr = g[point[1], point[0]]
                g_n, h_n, f_n = self.A_algorithm_get_vals(neigh, end_point, g_curr)
                try:
                    open_set.index(neigh)
                    if g_n < g[neigh[1], neigh[0]]:
                        g[neigh[1], neigh[0]] = g_n
                        f[neigh[1], neigh[0]] = f_n
                        came_from[neigh[1], neigh[0], 0] = point[0]
                        came_from[neigh[1], neigh[0], 1] = point[1]
                except ValueError:
                    open_set.append(neigh)
                    g[neigh[1], neigh[0]] = g_n
                    h[neigh[1], neigh[0]] = h_n
                    f[neigh[1], neigh[0]] = f_n
                    came_from[neigh[1], neigh[0], 0] = point[0]
                    came_from[neigh[1], neigh[0], 1] = point[1]
        return False, []

    def A_algorithm_get_vals(self, point, end_point, g):
        g_n = g + 1
        h_n = (end_point[0] - point[0]) * np.sqrt(2) / 2 + (end_point[1] - point[1])
        f_n = g_n + h_n
        return g_n, h_n, f_n

    def A_algorithm_reconstruct_route(self, came_from_array, end_point):
        route = []
        route.append(end_point)
        point = [int(came_from_array[end_point[1], end_point[0], 0]), int(came_from_array[end_point[1], end_point[0], 1])]
        while point[0] != -1:
            route.append(point)
            point = [int(came_from_array[point[1], point[0], 0]), int(came_from_array[point[1], point[0], 1])]
        route.reverse()
        return route

    def create_loop(self, board, head):
        head_x = head[0]
        head_y = head[1]
        if board[head_y][head_x - 1].type == 0:
            loop_x = [head_x, head_x - 1, head_x - 1]
            loop_y = [head_y, head_y, head_y - 1]
        else:
            loop_x = [head_x, head_x + 1, head_x + 1]
            loop_y = [head_y, head_y, head_y + 1]
        return np.asarray(loop_x), np.asarray(loop_y)

    def create_move_graph_singleplayer(self, board_height, board_width):
        move_x = np.zeros(board_width*board_height)
        move_y = np.zeros_like(move_x)
        if board_height % 2 == 0:
            max_iter = board_height
        else:
            max_iter = board_height - 2

        for i in range(max_iter):
            start_id = i * (board_width - 1)
            end_id = i * (board_width - 1) + board_width - 1
            if i % 2 == 0:
                move_x[start_id:end_id] = np.arange(1, board_width, 1)
            else:
                move_x[start_id:end_id] = np.arange(board_width - 1, 0, -1)
            move_y[start_id:end_id] = i

        if board_height % 2 != 0:
            for i in range(board_width):
                start_id = (board_height - 2) * (board_width - 1) + 2*i
                end_id = (board_height - 2) * (board_width - 1) + 2*i + 2
                if i % 2 == 0:
                    move_y[start_id:end_id] = np.arange(board_height - 2, board_height, 1)
                else:
                    move_y[start_id:end_id] = np.arange(board_height - 1, board_height - 3, -1)
                move_x[start_id:end_id] = board_width - i - 1
        move_x[-board_height:] = 0
        move_y[-board_height:] = np.arange(board_height - 1, -1, -1)
        return move_x, move_y
