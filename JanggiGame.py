# Author: Hye Yeon Park
# Date: 03/09/2021
# Description: [CS 162 Portfolio Project] This program is to simulate an abstract board game called Janggi.
# It is played on a board nine lines wide by ten lines long with Blue and Red as the competing players and
# Blue as the starting player. The game ends when one player checkmates the other's general.

import copy


class JanggiGame:
    """
    Janggi Game class with a board nine lines wide by ten lines long with Blue and Red
    as the competing players and Blue as the starting player.
    The game ends when one player checkmates the other's general.
    Includes methods called is_in_check, make_move, get_game_state and etc.
    Current board can be printed using a method called get_board.
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

        # RC=RedChariot, RE=RedElephant, RH=RedHorse, RG=RedGuard, *RK=RedGeneral, *RN=RedCannon, RS=RedSoldier
        # BC=BlueChariot, BE=BlueElephant, BH=BlueHorse, BG=BlueGuard, *BK=BlueGeneral, *BN=BlueCannon, BS=BlueSoldier
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

        self._turn_count = 0        # even count = blue's turn, odd count = red's turn
        self._game_state = "UNFINISHED"  # 'UNFINISHED' or 'RED_WON' or 'BLUE_WON'
        self._check = False
        self._checkmate = False
        self._move_from_idx = []    # index of the move_from position
        self._move_to_idx = []      # index of the move_to position
        self._moves = []            # all possible moves of the given piece as index of destination
        self._captured = ["OO"]
        self._threat = None         # threatening piece for the general

    def get_board(self):
        """ Print out the current board for testing purpose """
        print("-----This is the current board-----")
        for x in self._board:
            for i in range(0, 9):
                print(x[i], end="  ")
            print()
        print("-----------------------------------")

    def get_base_board(self):
        """ Print out the base board for testing purpose """
        print("------This is the base board-------")
        for x in self._base_board[:-1]:
            for i in range(0, 9):
                print(x[i], end="  ")
            print()
        # print last row separate, for column alignment
        for i in range(0, 9):
            print(self._base_board[9][i], end=" ")
        print()
        print("-----------------------------------")

    def get_game_state(self):
        """ Returns game state """
        return self._game_state

    def set_game_state(self):
        """ Sets game state """
        if self.get_player() == "B":
            self._game_state = "RED_WON"
        else:
            self._game_state = "BLUE_WON"

    def get_player(self):
        """ Returns whose turn it is """
        if self._turn_count % 2 == 0:
            return "B"
        else:
            return "R"

    def get_piece(self, row, col):
        """ Returns a piece at a given location """
        return self._board[row][col]

    def get_opponent(self):
        """ Returns the opposing player """
        if self.get_player() == "B":
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
        Checks if the opposing general is in a direct threat on the player's next move.
        Generate all possible moves of all the player's pieces.
        If any pieces can capture the opponent's general, sets _check to the opponent.
        """
        self._captured = ["OO"]     # reset captured list

        # go through the board and check all possible moves for the player's piece
        for x in range(0, 10):
            for y in range(0, 9):
                if self._board[x][y][0] == self.get_player():
                    piece_initial = self._board[x][y][1]

                    # save the current piece's index
                    temp_idx = self._move_from_idx
                    self._move_from_idx = [x, y]
                    self.call_moves(piece_initial)
                    # revert the index
                    self._move_from_idx = temp_idx

                    # if the opponent's general is captured, the opponent is in check
                    for i in range(len(self._captured)):
                        if self._captured[i][1] == "K" and self._captured[i][0] == self.get_opponent():
                            self._check = self.get_opponent()

    def is_checkmate(self):
        """
        Checks if the general in check can escape in the next move.
        First check if the general can move away or capture the threatening piece
        If not, check if any pieces can capture the threatening piece.
        If there is no escape, it's checkmate.
        Sets _checkmate to True, sets the game state and the game is over.
        """
        move_from_piece = None

        # get the general's current position
        for i in range(1, 10):
            for j in range(1, 9):
                if self._board[i][j] == self.get_player() + "K":
                    move_from_piece = self._board[i][j]
                    self._move_from_idx = [i, j]
                    break
                j += 1
            i += 1

        row = self._move_from_idx[0]
        col = self._move_from_idx[1]

        # get all possible moves of the general
        self.call_moves("K")

        # save the current board
        copied_board = copy.deepcopy(self._board)

        for (x, y) in self._moves:
            # make the general's move
            self._board[x][y] = move_from_piece
            self._board[row][col] = "OO"

            # check if still in check, if not, it's not checkmate
            self._turn_count += 1       # switch player for is_check test

            temp_check = self._check    # save current _check
            self._check = False         # reset _check
            self.is_check()             # rerun is_check to see if still in check
            if self._check is False:
                self._checkmate = False

            self._check = temp_check
            self._turn_count -= 1       # switch player back

            # if player in check doesn't match the current player
            if self._check != self.get_player():
                self._checkmate = False

        # revert the board
        self._board = copied_board

        # the general is still in checkmate
        # check if other pieces can capture the threatening piece
        # go through the board and check all possible moves for each piece
        self._captured = ["OO"]    # reset captured list
        for x in range(0, 10):
            for y in range(0, 9):

                if self.get_piece(x, y)[0] == self.get_player():
                    piece_initial = self._board[x][y][1]

                    self._move_from_idx = [x, y]    # set the current index with x, y
                    self.call_moves(piece_initial)

                    # if the threatening piece can be captured, it's not checkmate
                    for i in range(len(self._captured)):
                        if self._captured[i] == self._threat:
                            self._checkmate = False
                            break
                        # if not, continue the loop

        # if checkmate, set the game state
        if self._checkmate:
            self.set_game_state()

    def is_selfcheck(self):
        """
        Check if the valid move puts or leaves the player's general in check.
        A player cannot make such moves.
        """
        self._captured = ["OO"]     # reset captured list

        # go through the board and check all possible moves for each piece
        for x in range(0, 10):
            for y in range(0, 9):
                if self._board[x][y][0] == self.get_opponent():
                    piece_initial = self._board[x][y][1]

                    # switch player to check if opponent can catch player's general
                    self._turn_count += 1
                    # save the current piece's index
                    temp_idx = self._move_from_idx
                    self._move_from_idx = [x, y]
                    self.call_moves(piece_initial)
                    self._move_from_idx = temp_idx    # revert the index
                    self._turn_count -= 1   # switch player back

                    # if general is captured, the move puts or leaves the player's general in check.
                    # the move is invalid
                    for i in range(len(self._captured)):
                        if self._captured[i][1] == "K" and self._captured[i][0] == self.get_player():
                            return True

        return False

    def make_move(self, move_from, move_to):
        """
        Takes two string parameters that represent the square to move from and the square to move to.
        If the square being moved from contains opponent's piece or if the indicated move is not legal,
        or if the game has already been won, then return False.
        Otherwise make the indicated move, remove any captured piece, update the game state if necessary
        update whose turn it is, and return True.
        Call is_selfcheck to check if a player makes a move that puts or leaves their general in check.
        Call is_check to check if the opponent's general is in check.
        Call is_checkmate to check if it's checkmate and the game is over.
        """
        move_from_piece = None
        move_to_piece = None
        self._check = False     # reset _check

        if self._game_state != "UNFINISHED":
            return False

        # two passed strings are the same, the player passes its turn and return True
        if move_from == move_to:
            self._turn_count += 1
            return True

        else:
            # get the piece at the move_from position and its index
            i = int(move_from[1:]) - 1
            j = 0
            for j in range(0, 9):
                if self._base_board[i][j] == move_from:
                    move_from_piece = self._board[i][j]
                    self._move_from_idx = [i, j]
                    break

            # get the piece at the move_to position and its index
            x = int(move_to[1:]) - 1
            y = 0
            for y in range(0, 9):
                if self._base_board[x][y] == move_to:
                    move_to_piece = self._board[x][y]
                    self._move_to_idx = [x, y]
                    break

            # the move_from position doesn't have the player's piece
            if self.get_player() != move_from_piece[0]:
                return False

            # the move_to position has the player's own piece
            if self.get_player() == move_to_piece[0]:
                return False

            # get all possible moves for the current piece
            self.call_moves(move_from_piece[1])

            # if move_to index is one of the possible moves, the move is valid
            if (self._move_to_idx[0], self._move_to_idx[1]) in self._moves:

                # save the current board
                copied_board = copy.deepcopy(self._board)

                # make the indicated move
                self._board[x][y] = move_from_piece
                self._board[i][j] = "OO"

                # check if the opponent's general is in check
                temp_check = self._check    # save whose in check
                self.is_check()

                # check if the move puts or leaves the player's general in check
                if self.is_selfcheck() is True:
                    # if yes, revert the board and return False
                    self._board = copied_board
                    self._check = temp_check  # is_selfcheck() is True, invalid move, revert _check
                    return False

                # update the turn
                self._turn_count += 1

                # if general in check, check if it's checkmate
                if self._check:
                    # save the threatening piece to use it in is_checkmate
                    self._threat = self._board[x][y]
                    self.is_checkmate()

                # the move is valid
                return True

            return False

    def call_moves(self, piece_initial):
        """
        Calls each piece's move and return all possible moves of the piece.
        Called by make_move, is_selfcheck, is_check, is_checkmate.
        """
        self._moves = []            # reset moves list
        self._captured = ["OO"]     # reset captured list

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
        Called by each piece's move function to save the possible moves and any captured pieces
        """
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]

        for (x, y) in directions:
            if self.check_range(row + x, col + y):
                occupant = self.get_piece(row + x, col + y)

                if occupant != "OO":
                    # add captured piece and add the move
                    if occupant[0] == self.get_opponent():
                        self._captured.append(occupant)
                        move = (row + x, col + y)
                        self._moves.append(move)

                else:
                    # add the move
                    move = (row + x, col + y)
                    self._moves.append(move)

    def check_range(self, row, col):
        """ Checks if the given position is out of the board """
        if 0 <= row <= 9 and 0 <= col <= 8:
            return True

    def soldier_moves(self):
        """ Returns all possible moves for Soldier piece """
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]

        if self.get_player() == "B":
            directions = [(0, -1), (0, 1), (-1, 0)]
        else:
            directions = [(0, -1), (0, 1), (1, 0)]

        # if in palace, diagonal move may be possible
        diag_pos = [(7, 3), (7, 5), (9, 3), (9, 5), (8, 4), (0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
        diag_directions = []
        if (row, col) in diag_pos:
            if self.get_player() == "B":
                diag_directions = [(-1, -1), (-1, 1)]
            else:
                diag_directions = [(1, 1), (1, -1)]

        # add all the possible moves to self._moves
        self.add_to_moves(directions + diag_directions)
        return self._moves

    def horse_moves(self):
        """ Returns all possible moves for Horse piece """
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]
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

        # add all the possible moves to self._moves
        self.add_to_moves(directions)
        return self._moves

    def elephant_moves(self):
        """ Returns all possible moves for Elephant piece """
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]
        path1 = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 1st landing pos
        path2 = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]  # 2nd landing pos
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

        # add all the possible moves to self._moves
        self.add_to_moves(directions)
        return self._moves

    def chariot_moves(self):
        """ Returns all possible moves for Chariot piece """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_direction = []
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]

        for (x, y) in directions:
            i = 1  # a factor to multiply the directions

            while self.check_range(row + (x * i), col + (y * i)):
                move_to_piece = self.get_piece(row + (x * i), col + (y * i))

                # if the position is empty, that direction is valid
                if move_to_piece == "OO":
                    valid_direction.append((x * i, y * i))
                    i += 1

                # if the position is occupied with opponent piece, valid direction and stop the loop
                elif move_to_piece[0] == self.get_opponent():
                    valid_direction.append((x * i, y * i))
                    break

                # if the occupant is player's own piece, no more valid direction, stop the loop
                else:
                    break

        # if in palace, diagonal move may be possible
        diag_position = [(7, 3), (7, 5), (9, 3), (9, 5), (8, 4), (0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # if the chariot is in diag_position and the given move is diagonal
        if (row, col) in diag_position:

            for (x, y) in directions:
                i = 1  # a factor to multiply the directions

                # the move_to position must be within the palace
                while (row + (x * i), col + (y * i)) in diag_position:
                    move_to_piece = self.get_piece(row + (x * i), col + (y * i))

                    # if the position is empty, that direction is valid
                    if move_to_piece == "OO":
                        valid_direction.append((x * i, y * i))
                        i += 1

                    # if the position is occupied with opponent piece, valid direction and stop the loop
                    elif move_to_piece[0] == self.get_opponent():
                        valid_direction.append((x * i, y * i))
                        break

                    # if the occupant is player's own piece, no more valid direction, stop the loop
                    else:
                        break

        # add all the possible moves to self._moves
        self.add_to_moves(valid_direction)
        return self._moves

    def cannon_moves(self):
        """ Returns all possible moves for Cannon piece """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_direction = []
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]

        for (x, y) in directions:
            i = 1  # a factor to multiply the directions
            jumpover_piece = None

            while self.check_range(row + (x * i), col + (y * i)):
                occupied_piece = self.get_piece(row + (x * i), col + (y * i))

                # if the cannon has not jumped yet
                if jumpover_piece is None:
                    # if not occupied, continue the loop
                    if occupied_piece == "OO":
                        i += 1
                    # if occupied with non-cannon piece, save the piece and continue
                    elif occupied_piece[1] != "N":
                        jumpover_piece = occupied_piece
                        i += 1
                    # if the occupied piece is cannon, stop the loop
                    else:
                        break

                # if the cannon already jumped one piece
                else:
                    # if not occupied, it's valid direction and continue
                    if occupied_piece == "OO":
                        valid_direction.append((x * i, y * i))
                        i += 1
                    # if occupied by opponent, add the direction and stop
                    elif occupied_piece[0] == self.get_opponent() and occupied_piece[1] != "N":
                        valid_direction.append((x * i, y * i))
                        break
                    # if the occupied piece is cannon or self piece, stop the loop
                    else:
                        break

        # if cannon is at the corner of palace, diagonal move is possible
        diag_position = [(7, 3), (7, 5), (9, 3), (9, 5), (0, 3), (0, 5), (2, 3), (2, 5)]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # if the cannon is in diag_position and the given move is diagonal
        if (row, col) in diag_position:

            for (x, y) in directions:
                # then the move_to position must be within the palace
                if (row + (x * 2), col + (y * 2)) in diag_position:
                    jumpover_piece = self.get_piece(row + x, col + y)
                    move_to_piece = self.get_piece(row + (x * 2), col + (y * 2))

                    # if jumpover piece exists and is not cannon
                    if jumpover_piece != "OO" and jumpover_piece[1] != "N":

                        # if move_to position is empty, valid move
                        if move_to_piece == "OO":
                            valid_direction.append((x * 2, y * 2))

                        # if move_to is occupied with opponent's piece other than cannon, valid move
                        elif move_to_piece[0] == self.get_opponent() and move_to_piece[1] != "N":
                            valid_direction.append((x * 2, y * 2))

        # add all the possible moves to self._moves
        self.add_to_moves(valid_direction)
        return self._moves

    def general_guard_moves(self):
        """ Returns all possible moves for General and Guard pieces """
        row = self._move_from_idx[0]
        col = self._move_from_idx[1]

        # palace index for each player
        if self.get_player() == "B":
            # positions with diagonal move allowed
            diag_position = [(7, 3), (7, 5), (9, 3), (9, 5), (8, 4)]
            # positions with only linear move
            linear_position = [(8, 3), (8, 5), (7, 4), (9, 4)]
        else:
            diag_position = [(0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
            linear_position = [(1, 3), (0, 4), (1, 5), (2, 4)]

        if (row, col) in diag_position:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        else:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # generals and guards cannot leave the palace
        palace = diag_position + linear_position
        for (x, y) in directions:
            if self.check_range(row + x, col + y):
                if (row + x, col + y) not in palace:
                    directions.remove((x, y))

        # add all the possible moves to self._moves
        self.add_to_moves(directions)
        return self._moves


def main():
    game = JanggiGame()
    game.get_base_board()
    game.get_board()
    print(game.make_move("c7", "c6"))  # blue turn
    print(game.make_move("c1", "d3"))  # red turn
    print(game.make_move("b10", "d7"))  # blue turn
    print(game.make_move("b3", "e3"))  # red turn
    print(game.make_move("c10", "d8"))  # blue turn
    print(game.make_move("h1", "g3"))  # red turn
    print(game.make_move("e7", "e6"))  # blue turn
    print(game.make_move("e3", "e6"))  # red turn
    print(game.make_move("h8", "c8"))  # blue turn
    print(game.make_move("d3", "e5"))  # red turn
    print(game.make_move("c8", "c4"))  # blue turn
    print(game.make_move("e5", "c4"))  # red turn
    print(game.make_move("i10", "i8"))  # blue turn
    print(game.make_move("g4", "f4"))  # red turn
    print(game.make_move("i8", "f8"))  # blue turn
    print(game.make_move("g3", "h5"))  # red turn
    print(game.make_move("h10", "g8"))  # blue turn
    print(game.make_move("e6", "e3"))  # red turn
    game.get_board()
    print("blue in check?", game.is_in_check("blue"))
    print("red in check?", game.is_in_check("red"))
    print(game.get_game_state())


if __name__ == '__main__':
    main()
