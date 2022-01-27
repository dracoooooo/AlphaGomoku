import random
import numpy as np
import MCTS


class Board:
    def __init__(self, x: int, y: int, p1: str = 'x', p2: str = 'o', fill: str = '-'):
        self.map = np.full((x, y), fill_value=fill, dtype=str)
        self.row = x
        self.col = y
        self.p1 = p1
        self.p2 = p2
        self.fill = fill
        self.count = 0

    def result(self):
        for i in range(self.row):
            for j in range(self.col):
                p = self.map[i, j]
                if p == self.fill:
                    continue
                down, right, down_left, down_right = 0, 0, 0, 0
                for k in range(5):
                    if 0 <= j + k < self.col and self.map[i, j + k] == p:
                        right += 1
                    if 0 <= i + k < self.row and self.map[i + k, j] == p:
                        down += 1
                    if 0 <= i + k < self.row and 0 <= j + k < self.col and self.map[i + k, j + k] == p:
                        down_right += 1
                    if 0 <= i + k < self.row and 0 <= j - k < self.col and self.map[i + k, j - k] == p:
                        down_left += 1
                if down == 5 or right == 5 or down_right == 5 or down_left == 5:
                    return p
                else:
                    continue

        if self.row * self.col - self.count == 0:
            return 'tie'
        else:
            return None

    def set_bit(self, x: int, y: int, piece: str):
        assert 0 <= x < self.row and 0 <= y < self.col
        assert self.map[x, y] == self.fill
        self.map[x, y] = piece
        self.count += 1

    def random_choose(self):
        left = self.row * self.col - self.count
        assert left > 0
        choice = random.randint(0, left - 1)
        for i in range(self.row):
            for j in range(self.col):
                if self.map[i, j] == self.fill:
                    if choice == 0:
                        return i, j
                    choice -= 1

    def print(self):
        print('----------board----------')
        print('player1 with', self.p1)
        print('player2 with', self.p2)
        print('   ', end='')
        for i in range(self.col):
            print(i, end='  ')
        print()
        for i in range(self.row):
            print(i, end='  ')
            for j in range(self.col):
                print(self.map[i, j], end='  ')
            print()


class Player:
    def __init__(self, piece: str, board: Board):
        self.piece = piece
        self.board = board

    def put(self, x: int, y: int):
        self.board.set_bit(x, y, self.piece)


class Game:
    def __init__(self):
        p1 = 'x'
        p2 = 'o'
        self.board = Board(8, 8, p1, p2)
        self.player1 = Player(p1, self.board)
        self.player2 = Player(p2, self.board)


    def start(self):
        state = MCTS.State(self.board, self.player1, self.player2)
        MCT = MCTS.MCTSNode(state, None)
        while(True):
            (x_MCT, y_MCT) = MCT.MCTS()
            self.player1.put(x_MCT, y_MCT)
            self.board.print()
            MCT = MCT.move(x_MCT, y_MCT)
            result = self.board.result()
            if result is not None:
                print(result, 'wins')
                break
            s = [int(i) for i in input().split(' ')]
            (x_human, y_human) = (s[0], s[1])
            self.player2.put(x_human, y_human)
            self.board.print()
            MCT = MCT.move(x_human, y_human)
            result = self.board.result()
            if result is not None:
                print(result, 'wins')
                break





