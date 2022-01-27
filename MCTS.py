import copy
import math


class State:
    def __init__(self, board, current_player, another_player):
        self.board = board
        self.current_player = current_player
        self.another_player = another_player

    def get_all_possible_states(self):
        result = []
        for i in range(self.board.row):
            for j in range(self.board.col):
                if self.board.map[i, j] == self.board.fill:
                    state = copy.deepcopy(self)
                    state.current_player = self.another_player
                    state.another_player = self.current_player
                    state.board.set_bit(i, j, self.current_player.piece)
                    result.append(state)
        return result

    def terminal(self):
        return self.board.result() is not None

    def random_play(self):
        state = copy.deepcopy(self)
        while True:
            result = state.board.result()
            if result is not None:
                if result == self.current_player.piece:
                    return 1
                elif result == self.another_player.piece:
                    return -1
                else:
                    return 0    # tie
            (x, y) = state.board.random_choose()
            state.board.set_bit(x, y, state.current_player.piece)

            p = state.current_player
            state.current_player = state.another_player
            state.another_player = p


class MCTSNode:
    def __init__(self, state, parent, exploration_weight=1):  # move is from parent to node
        self.state, self.parent, self.children = state, parent, []
        self.wins, self.visits = 0, 0
        self.exploration_weight = exploration_weight

    def expand_node(self):
        if not self.state.terminal():
            for state in self.state.get_all_possible_states():
                nc = MCTSNode(state, self)  # new child node
                self.children.append(nc)

    def back_propagation(self, result):
        self.visits += 1
        self.wins += result
        if self.has_parent():
            self.parent.back_propagation(result)

    def is_leaf(self):
        return len(self.children) == 0

    def has_parent(self):
        return self.parent is not None

    def select_best_child(self):
        if self.is_leaf():
            return self
        max_score = 0
        best_child = self.children[0]
        for child in self.children:
            uct = child.uct()
            if uct > max_score:
                max_score = uct
                best_child = child
        return best_child

    def uct(self):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + self.exploration_weight * math.sqrt(2 * math.log(self.parent.visits) / self.visits)

    def select_best_move(self):
        max_score = 0
        best_child = self.children[0]
        for child in self.children:
            win_rate = child.wins / child.visits
            if win_rate > max_score:
                max_score = win_rate
                best_child = child
        for i in range(best_child.state.board.row):
            for j in range(best_child.state.board.col):
                if best_child.state.board.map[i, j] != self.state.board.map[i, j]:
                    return i, j
        return None

    def move(self, x, y):
        for child in self.children:
            board = child.state.board
            if board.map[x, y] == self.state.current_player.piece:
                return child

    def MCTS(self):
        root_node = self
        for time in range(2000):
            node = root_node
            while not node.is_leaf():  # select leaf
                node = node.select_best_child()

            node.expand_node()  # expand
            node = node.select_best_child()

            result = node.state.random_play()   # simulate

            node.back_propagation(result)   # back propagation

        return self.select_best_move()

