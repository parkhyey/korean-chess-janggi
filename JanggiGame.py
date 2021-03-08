# Author: Hye Yeon Park
# Date: 03/02/2021
# Description: [CS 162 Portfolio Project] This program is to simulate an abstract board game called Janggi.
# It is played on a board nine lines wide by ten lines long with Blue and Red as the competing players and
# Blue as the starting player. The game ends when one player checkmates the other's general.

import copy


class JanggiGame:
    """
    Janggi Game class
    """

    def __init__(self):
        """
        Initializes all data members
        """
        self._base_board = [
            ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1"],
            ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2"],
            ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3"],
            ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4"],
            ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5"],
            ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6"],
            ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7"],
            ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8"],
            ["a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9"],
            ["a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10"],
        ]

        # RC=RedChariot, RE=RedElephant, RH=RedHorse, RG=RedGuard, RK=RedGeneral, RN=RedCannon, RS=RedSoldier
        # BC=BlueChariot, BE=BlueElephant, BH=BlueHorse, BG=BlueGuard, BK=BlueGeneral, BN=BlueCannon, BS=BlueSoldier
        self._board = [
            ["RC", "RE", "RH", "RG", "OO", "RG", "RE", "RH", "RC"],
            ["OO", "OO", "OO", "OO", "RK", "OO", "OO", "OO", "OO"],
            ["OO", "RN", "OO", "OO", "OO", "OO", "OO", "RN", "OO"],
            ["RS", "OO", "RS", "OO", "RS", "OO", "RS", "OO", "RS"],
            ["OO", "OO", "OO", "OO", "OO", "OO", "OO", "OO", "OO"],
            ["OO", "OO", "OO", "OO", "OO", "OO", "OO", "OO", "OO"],
            ["BS", "OO", "BS", "OO", "BS", "OO", "BS", "OO", "BS"],
            ["OO", "BN", "OO", "OO", "OO", "OO", "OO", "BN", "OO"],
            ["OO", "OO", "OO", "OO", "BK", "OO", "OO", "OO", "OO"],
            ["BC", "BE", "BH", "BG", "OO", "BG", "BE", "BH", "BC"]
        ]

        self._turn_count = 0  # even count = blue's turn, odd count = red's turn
        self._game_state = "UNFINISHED"  # 'UNFINISHED' or 'RED_WON' or 'BLUE_WON'
        self._check = False
        self._checkmate = False
        self._curr_piece = ""  # the piece at the current position
        self._des_piece = ""  # the piece at the destination position
        self._curr_idx = []  # index of the current position
        self._des_idx = []  # index of the destination position
        self._moves = []
        self._captured = []
        self._threat = []       # threatening piece for the general

    def get_board(self):
        """ Print out the board for testing purpose """
        print("-----This is the current board-----")
        for x in self._board:
            for i in range(0, 9):
                print(x[i], end="  ")
            print()
        print("-----------------------------------")

    def get_base_board(self):
        """ Print out the board for testing purpose """
        print("------This is the base board-------")
        for x in self._base_board[:-1]:
            for i in range(0, 9):
                print(x[i], end="  ")
            print()
        # print last row separate for column alignment
        for i in range(0, 9):
            print(self._base_board[9][i], end=" ")
        print()
        print("-----------------------------------")

    def set_board(self, board):
        """ Sets the current board with the given board """
        self._board = board

    def get_game_state(self):
        """ Returns game state """
        return self._game_state

    def set_game_state(self):
        """ Sets game state """
        if self.get_turn() == "B":
            self._game_state = "RED_WON"
        else:
            self._game_state = "BLUE_WON"

    def get_turn(self):
        """ Returns whose turn it is """
        if self._turn_count % 2 == 0:
            return "B"
        else:
            return "R"

    def get_piece(self, row, col):
        """ Returns a piece at a given location"""
        return self._board[row][col]

    def get_opponent(self):
        """ Returns the opposing player """
        if self.get_turn() == "B":
            return "R"
        else:
            return "B"

    def is_in_check(self, player):
        """
        Takes as a parameter either 'red' or 'blue' and returns True if that player is in check,
        but returns False otherwise.
        """
        if self._check == "B" and player == "blue":
            return True
        elif self._check == "R" and player == "red":
            return True
        return False

    def is_check(self):
        """
        Sets _check True if the opposing general is in a direct threat on the player's next move.
        Call check_moves to demonstrate if any pieces can capture the general.
        If yes, sets _check True and call check_escape which checks if there is any possible escape
        move to be out of the check state. If no escape, set _checkmate True and update game state.
        """
        self._captured = []
        # go through the board and check all possible moves for the player's piece
        for x in range(0, 10):
            for y in range(0, 9):
                if self._board[x][y][0] == self.get_turn():
                    piece_initial = self._board[x][y][1]
                    # print("is_check = ", x, y, piece_initial)

                    temp = self._curr_idx
                    self._curr_idx = [x, y]
                    self.call_moves(piece_initial)
                    self._curr_idx = temp

                    # if the opponent's general is captured, the opponent is in check
                    # print("is_check._captured", self._captured)
                    for i in range(len(self._captured)):
                        if self._captured[i][1] == "K" and self._captured[i][0] == self.get_opponent():
                            self._check = self.get_opponent()
                            break
                        else:
                            self._check = None

    def is_checkmate(self):
        """
        Check if the general in check can escape in the next move.
        If not, it's checkmate, set the game state and the game is over
        """
        # if the general can move and escape from check
        # get the general's current position

        for i in range(1, 10):
            for j in range(1, 9):
                if self._board[i][j] == self.get_turn() + "K":
                    self._curr_piece = self._board[i][j]
                    self._curr_idx = [i, j]
                    break
                j += 1
            i += 1

        row = self._curr_idx[0]
        col = self._curr_idx[1]

        # returns all possible moves of the general
        self.call_moves("K")
        print("whose turn", self.get_turn(), "is_checkmate? possible move of general = ", self._moves)

        for (x, y) in self._moves:
            copied_board = copy.deepcopy(self._board)

            # make the move
            self._board[x][y] = self._curr_piece
            self._board[row][col] = "OO"
            print("virtual general move =", self._board[row][col], self._board[x][y])

            # if still in check
            self.is_check()
            # if not, pass
            if self._check != self.get_turn():
                self._board = copied_board

        # the general is still in check
        # check if other pieces can capture the threatening piece
        self._captured = []
        # go through the board and check all possible moves for each piece

        for x in range(0, 10):
            for y in range(0, 9):
                if self._board[x][y][0] == self.get_opponent():
                    piece_initial = self._board[x][y][1]

                    temp = self._curr_idx
                    self._curr_idx = [x, y]
                    self.call_moves(piece_initial)
                    self._curr_idx = temp

                    for i in range(len(self._captured)):
                        if self._captured == self._threat:
                            print("test")
                            self._checkmate = False
                        else:
                            self._checkmate = True

        # if checkmate, set the game state
        if self._checkmate:
            self.set_game_state()

    def is_selfcheck(self):
        """
        Check if the valid move puts or leaves the player's general in check.
        A player cannot make such move.
        """
        self._captured = []
        # go through the board and check all possible moves for each piece
        for x in range(0, 10):
            for y in range(0, 9):
                if self._board[x][y][0] == self.get_opponent():
                    piece_initial = self._board[x][y][1]
                    # print("selfcheck = ", x, y, piece_initial)
                    # update turn temporarily to check if opponent can catch player's general
                    self._turn_count += 1
                    temp = self._curr_idx
                    self._curr_idx = [x, y]
                    self.call_moves(piece_initial)
                    self._curr_idx = temp
                    # put player's turn back to before testing
                    self._turn_count -= 1
                    # if general is captured, the move puts or leaves the player's general in check.
                    # thus, the move is invalid
                    # print("self._captured", self._captured)
                    for i in range(len(self._captured)):
                        if self._captured[i][1] == "K" and self._captured[i][0] == self.get_turn():
                            return True
        return False

    def make_move(self, move_from, move_to):
        """
        Takes two string parameters that represent the square to move from and the square to move to.
        If the square being moved from contains opponent's piece or if the indicated move is not legal,
        or if the game has already been won, then it should just return False.
        Otherwise it should make the indicated move, remove any captured piece, update the game state
        if necessary, update whose turn it is, and return True.
        A player cannot make a move that puts or leaves their general in check.
        """
        print("whose turn?", self.get_turn())  # testing

        if self._game_state != "UNFINISHED":
            print("game already won")
            return False

        # two passed strings are the same, the player passes its turn
        if move_from == move_to:
            self._turn_count += 1
            print("two positions are the same, the player passes its turn")
            return True

        else:
            # get the piece at the starting point and its index
            i = int(move_from[1:]) - 1
            j = 0
            for j in range(0, 9):
                if self._base_board[i][j] == move_from:
                    self._curr_piece = self._board[i][j]
                    self._curr_idx = [i, j]
                    break

            # get the piece at the destination point and its index
            x = int(move_to[1:]) - 1
            y = 0
            for y in range(0, 9):
                if self._base_board[x][y] == move_to:
                    self._des_piece = self._board[x][y]
                    self._des_idx = [x, y]
                    break

            print("before move =", self._curr_piece, self._des_piece)
            print("index = ", self._curr_idx, self._des_idx)

            if self.get_turn() != self._curr_piece[0]:
                print("the starting pos doesn't have the player's piece")
                return False
            if self.get_turn() == self._des_piece[0]:
                print("the destination pos has the player's own piece")
                return False

            # get all moves for the current piece
            self.call_moves(self._curr_piece[1])
            print(self._moves)

            # if move_to position is one of the possible moves, the move is valid
            if (self._des_idx[0], self._des_idx[1]) in self._moves:

                # save the current board
                copied_board = copy.deepcopy(self._board)
                print("copied board", copied_board)
                # make the indicated move
                self._board[x][y] = self._curr_piece
                self._board[i][j] = "OO"
                print("after move =", self._board[i][j], self._board[x][y])

                # check if the opponent is in check
                # if the player's next move can capture the opposing general
                self.is_check()
                print("blue is_in_check?", self.is_in_check("blue"))
                print("red is_in_check?", self.is_in_check("red"))

                # if the move puts or leaves the player's general in check, return False
                if self.is_selfcheck() is True:
                    # revert the board
                    print("copied board2", copied_board)
                    self._board = copied_board
                    print("invalid move - the move puts or leaves the player's general in check.")
                    return False

                self._turn_count += 1

                # check if is_checkmate
                if self._check:
                    # save the threatening piece
                    self._threat.append(self._board[x][y])
                    self.is_checkmate()

                return True

            return False

    def call_moves(self, piece_initial):
        """
        Calls each piece's move. Called by make_move, is_selfcheck, is_check, is_checkmate.
        """
        self._moves = []
        self._captured = ["OO"]

        if piece_initial == "S":
            self.soldier_moves()
            return self._moves
        if piece_initial == "H":
            self.horse_moves()
            return self._moves
        if piece_initial == "E":
            self.elephant_moves()
            return self._moves
        if piece_initial == "C":
            self.chariot_moves()
            return self._moves
        if piece_initial == "N":
            self.cannon_moves()
            return self._moves
        if piece_initial == "K" or "G":
            self.general_guard_moves()
            return self._moves

    def add_to_moves(self, directions):
        """
        Called by each piece's move function to add the moves
        """
        row = self._curr_idx[0]
        col = self._curr_idx[1]

        for (x, y) in directions:
            if self.check_range(row + x, col + y):
                occupant = self.get_piece(row + x, col + y)

                if occupant != "OO":
                    # add opponent pieces that can be captured to _captured list
                    if occupant[0] == self.get_opponent():
                        self._captured.append(occupant)

                else:
                    move = (row + x, col + y)
                    self._moves.append(move)

    def check_range(self, row, col):
        """ Checks if the given position is out of the board """
        if 0 <= row <= 9 and 0 <= col <= 8:
            return True

    def soldier_moves(self):
        """ Returns all possible moves for Soldier piece """

        row = self._curr_idx[0]
        col = self._curr_idx[1]
        if self.get_turn() == "B":
            directions = [(0, -1), (0, 1), (-1, 0)]
        else:
            directions = [(0, -1), (0, 1), (1, 0)]

        # if the current position is in palace, diagonal move may be possible
        diag_pos = [(7, 3), (7, 5), (9, 3), (9, 5), (8, 4), (0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
        diag_directions = []
        if (row, col) in diag_pos:
            if self.get_turn() == "B":
                diag_directions = [(-1, -1), (-1, 1)]
            else:
                diag_directions = [(1, 1), (1, -1)]

        self.add_to_moves(directions + diag_directions)

        return self._moves

    def horse_moves(self):
        """ Returns all possible moves for Horse piece """
        row = self._curr_idx[0]
        col = self._curr_idx[1]
        path = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        # remove directions with intervening piece on the path
        for (x, y) in path:
            if self.check_range(row + x, col + y):
                if self.get_piece(row + x, col + y) != "OO":
                    if y == 0:
                        directions.remove((x * 2, y + 1))
                        directions.remove((x * 2, y - 1))
                    if x == 0:
                        directions.remove((x + 1, y * 2))
                        directions.remove((x - 1, y * 2))

        self.add_to_moves(directions)
        return self._moves

    def elephant_moves(self):
        """ Returns all possible moves for Elephant piece """
        row = self._curr_idx[0]
        col = self._curr_idx[1]
        path1 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        path2 = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        directions = [(3, 2), (3, -2), (-3, 2), (-3, -2), (2, 3), (2, -3), (-2, 3), (-2, -3)]

        # remove directions with any intervening piece on the path
        # first check path1 and remove invalid move directions
        for (x, y) in path1:
            if self.check_range(row + x, col + y):
                if self.get_piece(row + x, col + y) != "OO":
                    if y == 0:  # vertical move
                        path2.remove((x * 2, y + 1))
                        path2.remove((x * 2, y - 1))
                        directions.remove((x * 3, y + 2))
                        directions.remove((x * 3, y - 2))
                    if x == 0:  # horizontal move
                        path2.remove((x + 1, y * 2))
                        path2.remove((x - 1, y * 2))
                        directions.remove((x + 2, y * 3))
                        directions.remove((x - 2, y * 3))

        # then check path2 and remove invalid move directions
        for (x, y) in path2:
            if self.check_range(row + x, col + y):
                if self.get_piece(row + x, col + y) != "OO":
                    if abs(x) == 2:
                        # remove one of (3, 2), (3, -2), (-3, 2), (-3, -2)
                        directions.remove((int(x * 1.5), y * 2))
                    if abs(y) == 2:
                        # remove one of (2, 3), (2, -3), (-2, 3), (-2, -3)
                        directions.remove((x * 2, int(y * 1.5)))

        self.add_to_moves(directions)
        return self._moves

    def chariot_moves(self):
        """ Returns all possible moves for Chariot piece """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_direction = []
        row = self._curr_idx[0]
        col = self._curr_idx[1]

        for (x, y) in directions:
            i = 1
            while row + (x * i) in range(10) and col + (y * i) in range(9):
                occupant = self.get_piece(row + (x * i), col + (y * i))
                if occupant == "OO":
                    valid_direction.append((x * i, y * i))
                    i += 1
                elif occupant[0] == self.get_opponent():
                    valid_direction.append((x * i, y * i))
                    break
                # if the occupant is player's own piece, break
                else:
                    break

        # if in palace, diagonal move may be possible
        diag_pos = [(7, 3), (7, 5), (9, 3), (9, 5), (8, 4), (0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        # if the chariot is in diag_pos and the given move is diagonal
        # then the move_to position must be within the palace
        if (row, col) in diag_pos:
            i = 1
            for (x, y) in directions:
                while (row + (x * i), col + (y * i)) in diag_pos:
                    occupant = self.get_piece(row + (x * i), col + (y * i))
                    if occupant == "OO":
                        valid_direction.append((x * i, y * i))
                        i += 1
                    elif occupant[0] == self.get_opponent():
                        valid_direction.append((x * i, y * i))
                        print(valid_direction)
                        break
                    else:
                        break

        self.add_to_moves(valid_direction)
        return self._moves

    def cannon_moves(self):
        """ Returns all possible moves for Cannon piece """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_direction = []
        jumpover_piece = None
        row = self._curr_idx[0]
        col = self._curr_idx[1]

        for (x, y) in directions:
            i = 1
            while row + (x * i) in range(10) and col + (y * i) in range(9):
                occupant = self.get_piece(row + (x * i), col + (y * i))

                # if not jumped yet
                if jumpover_piece is None:
                    # if not occupied, continue the loop
                    if occupant == "OO":
                        i += 1
                    # if occupied with non-cannon piece, save the piece, jump and continue
                    elif occupant[1] != "N":
                        jumpover_piece = occupant
                        i += 1
                    # if the occupied piece is cannon, break
                    else:
                        break
                # if already jumped
                else:
                    # if not occupied, add the direction and continue
                    if occupant == "OO":
                        valid_direction.append((x * i, y * i))
                        i += 1
                    # if occupied by opponent, add the direction and break
                    elif occupant[0] == self.get_opponent() and occupant[1] != "N":
                        valid_direction.append((x * i, y * i))
                        print(valid_direction)
                        break
                    else:
                        break

        # if in the corner of palace, diagonal move is possible
        diag_pos = [(7, 3), (7, 5), (9, 3), (9, 5), (0, 3), (0, 5), (2, 3), (2, 5)]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        # if the cannon is in diag_pos and the given move is diagonal
        # then the move_to position must be within the palace
        if (row, col) in diag_pos:

            for (x, y) in directions:
                while (row + (x * 2), col + (y * 2)) in diag_pos:
                    occupant = self.get_piece(row + x, col + y)
                    corner_piece = self.get_piece(row + (x * 2), col + (y * 2))

                    if corner_piece == "OO":
                        if occupant[0] == self.get_opponent() and occupant[1] != "N":
                            valid_direction.append((x * 2, y * 2))

                    else:
                        if corner_piece[0] == self.get_opponent() and corner_piece[1] != "N":
                            valid_direction.append((x * 2, y * 2))

        self.add_to_moves(valid_direction)
        return self._moves

    def general_guard_moves(self):
        """ Returns all possible moves for General and Guard pieces """
        row = self._curr_idx[0]
        col = self._curr_idx[1]

        # palace index for each player
        if self.get_turn() == "B":
            # positions where diagonal move is allowed
            diag_pos = [(7, 3), (7, 5), (9, 3), (9, 5), (8, 4)]
            # positions where only linear is allowed
            straight_pos = [(8, 3), (8, 5), (7, 4), (9, 4)]
        else:
            diag_pos = [(0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
            straight_pos = [(1, 3), (0, 4), (1, 5), (2, 4)]

        if (row, col) in diag_pos:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        else:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # generals and guards cannot leave the palace
        palace = diag_pos + straight_pos
        for (x, y) in directions:
            if self.check_range(row + x, col + y):
                if (row + x, col + y) not in palace:
                    directions.remove((x, y))

        self.add_to_moves(directions)
        return self._moves


def main():
    game = JanggiGame()
    # print(game.get_game_state())
    game.get_base_board()
    game.get_board()
    print(game.make_move("a10", "a9"))  # blue turn
    print(game.make_move("i4", "h4"))  # red turn
    print(game.make_move("a9", "d9"))  # blue turn
    print(game.make_move("i1", "i5"))  # red turn
    print(game.make_move("d9", "d8"))  # blue turn
    print(game.make_move("i5", "f5"))  # red turn
    print(game.make_move("e9", "e8"))  # blue turn
    game.get_board()
    print(game.make_move("f5", "f8"))  # red turn - checkmate (red won)
    print(game.get_game_state())
    # print(game.get_game_state())
    game.get_board()
    # blue_in_check = game.is_in_check('blue')    # should return False


if __name__ == '__main__':
    main()
