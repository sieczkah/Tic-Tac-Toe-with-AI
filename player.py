from random import choice
from game_board import GameBoard


class Player:
    """This is a parent class representing TicTacToe Player

    Attributes:
        sign (str): Player's instance sign X or O
        opponents_sign (str): Player's instance opponent's sign X or O
        is_bot (bool): Bool defining if the player is Human or AI player
    """
    signs = ['O', 'X']
    SIGNS_DICT = {'O': 'X', 'X': 'O'}

    def __new__(cls, *args, **kwargs):
        """Dunder method to control the number of instances of Player class
        to maximum of two per game
        """
        if len(cls.signs) == 0:
            raise TypeError('Too many players')
        return super(Player, cls).__new__(cls)

    def __init__(self, is_bot=None):
        """The constructor of Player class.
        Parameters:
            is_bot (bool): defining if the player is human or AI player.
        """
        self.sign = self.get_sign()
        self.opponents_sign = self.SIGNS_DICT[self.sign]
        self.is_bot = is_bot

    def _get_cords(self, game_board):
        """Returns players move cords (x,y)"""
        pass

    @classmethod
    def get_sign(cls):
        """Class method to remove used sign for the signs class variable"""
        return cls.signs.pop()

    @classmethod
    def reset_signs(cls):
        """Class method to set class signs variable to initial state"""
        cls.signs = ['O', 'X']


class HumanPlayer(Player):
    """Child class of Player class representing Human Player of TicTacToe game
        Attributes:
        sign (str): Player's instance sign X or O
        opponents_sign (str): Player's instance opponent's sign X or O
        is_bot (bool): Bool defining if the player is Human or AI player
    """

    def __init__(self):
        """The constructor of HumanPlayer class."""
        super().__init__(is_bot=False)

    def get_cords(self, game_board):
        """Method to get X, Y cords from Human player's input.

        Params:
            game_board (list): TicTacToe game board list of rows.

        Returns:
            cord_x (int): Integer (from 0 to 2) representing valid user X move
            cord_y (int): Integer (from 0 to 2) representing valid user Y move
        """
        empty_cells = GameBoard.get_empty_cells(game_board)
        cord_x, cord_y = None, None
        while cord_x is None and cord_y is None:
            user_input = input('Enter the coordinates:')
            cord_x, cord_y = self.validate_input(user_input, empty_cells)
        return cord_x, cord_y

    @staticmethod
    def validate_input(user_input, empty_cells):
        """Static method to validate user's input.

        Params:
            user_input (str): String input from the user.
            empty_cells (list): List of empty cell's (X,Y) coordinates.

        Returns:
            If user input is valid:
                cord_x (int): Integer (from 0 to 2)
                cord_y (int): Integer (from 0 to 2)
            If user input is invalid:
                None, None
        """
        valid_cords = [0, 1, 2]
        try:
            x, y = user_input.split()
            cord_x = int(x) - 1
            cord_y = int(y) - 1
            if (cord_x, cord_y) in empty_cells:
                return cord_x, cord_y
            else:
                if cord_x in valid_cords and cord_y in valid_cords:
                    print('This cell is occupied! Choose another one!')
                    return None, None
                else:
                    print('Coordinates should be from 1 to 3!')
                    return None, None
        except ValueError:
            print('You should enter numbers!')
            return None, None


class Bot(Player):
    """Child class of Player class representing Bot(AI) Player of TicTacToe game.
        Attributes:
        sign (str): Bot's instance sign X or O.
        opponents_sign (str): Bot's instance opponent's sign X or O.
        is_bot (bool): Bool defining if the player is Human or AI player.
        bot_level (str): Representing bot difficulty level(easy, medium, hard).
    """

    def __init__(self, bot_level):
        """The constructor of Bot class.
        Params: bot_level (str): Bot difficulty level (easy, medium, hard)
        """
        super().__init__(is_bot=True)
        self.bot_level = bot_level

    def get_cords(self, game_board):
        """Method to return get_cords method according to bot difficulty."""
        if self.bot_level == 'easy':
            return self.ai_get_cords_easy(game_board)
        if self.bot_level == 'medium':
            return self.ai_get_cords_medium(game_board)
        if self.bot_level == "hard":
            return self.ai_get_cord_hard(game_board)

    def ai_get_cords_easy(self, game_board):
        """Method to return 'easy' bot move.
        Params: game_board(list) TicTacToe game board list of rows.
        Returns: move (tuple): tuple of (X,Y) coordinates."""
        # Easy bot returns a random move from available moves.
        empty_cells = GameBoard.get_empty_cells(game_board)
        print('Making move level "easy"')
        return self.random_move(empty_cells)

    def ai_get_cords_medium(self, game_board):
        """Method to return 'medium' bot move.
        Params: game_board(list) TicTacToe game board list of rows.
        Returns: move (tuple): tuple of (X,Y) coordinates."""
        # Medium bot returns a winning move if it's available.
        # If there is no winning move it returns a blocking move.
        # If neither of both is available it returns a random move.
        print('Making move level "medium"')
        win_moves = self.get_winning_moves(game_board)
        if win_moves[self.sign]:
            return self.random_move(win_moves[self.sign])
        elif win_moves[self.opponents_sign]:
            return self.random_move(win_moves[self.opponents_sign])
        else:
            empty_cells = GameBoard.get_empty_cells(game_board)
            return self.random_move(empty_cells)

    def ai_get_cord_hard(self, game_board):
        """Method to return 'hard' bot move.
        Params: game_board(list) TicTacToe game board list of rows.
        Returns: move (tuple): tuple of (X,Y) coordinates."""
        # 'hard' Bot returns the best move possible.
        # The best move is calculated by minimax algorithm.
        board = game_board.copy()
        best_move = self.minimax(board, 0, True)[:2]

        print('Making move level "hard"')
        return best_move

    def minimax(self, board, depth, is_maximizer):
        """Recursive method implementing Minimax algorithm.
        For Minimax see:
        https://en.wikipedia.org/wiki/Minimax
        Params:
            board (list): TicTacToe game board list of rows.
            depth (int): Depth of the current node.
            is_maximizer (bool): bool defining if the player is maximizing.

        Returns:
            best (list): list of [cord_x, cord_y, score] for the best move
                         possible.
        """
        score_dict = {self.sign: 10, self.opponents_sign: -10}
        empty_cells = GameBoard.get_empty_cells(board)
        is_finished, winner = GameBoard.is_finished(board)
        # base condition  of minimax method
        # if the game is finished, returns score of the move based on winner
        if is_finished:
            return [-1, -1, score_dict.get(winner, 0)]
        # condition for maximizing player
        if is_maximizer:
            best = [-1, -1, -1000]
            sign = self.sign
        # condition for minimazing player
        else:
            best = [-1, -1, +1000]
            sign = self.opponents_sign

        # loop through all the possible moves
        for cord_x, cord_y in empty_cells:
            # for every possible move we perform it, and call minimax for it
            # to score it, then we un-do the move and return it as best_move
            # if the score is greater than best score
            board[cord_x][cord_y] = sign
            score = self.minimax(board, depth + 1, not is_maximizer)
            board[cord_x][cord_y] = ' '
            score[0], score[1] = cord_x, cord_y

            if is_maximizer:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best

    @staticmethod
    def get_winning_moves(board):
        """Static method to evaluate the game board and create a dictionary
        of winning moves for 'X' sign and 'O' sign.

        Params: board (list): TicTacToe game board list of rows

        Returns: win_moves (dict): Dictionary of 'X', 'O' keys storing list
                 of (cord_x, cord_y) coordinates tuples of winning moves.
        """
        win_moves = {'X': [], 'O': []}

        def check_cells(cells):
            if len(set(cells)) == 2 and cells.count(' ') == 1:
                index = cells.index(' ')
                cells.remove(' ')
                return True, cells[0], index
            return False, None, None

        # Loop through rows an columns
        for i in range(3):
            row = board[i].copy()
            column = [board[0][i], board[1][i], board[2][i]]

            # Check rows for possible winning move
            is_row_win, row_sign, row_y = check_cells(row)
            if is_row_win:
                win_moves[row_sign].append((i, row_y))

            # Check columns for possible winning move
            is_col_win, col_sign, col_x = check_cells(column)
            if is_col_win:
                win_moves[col_sign].append((col_x, i))

        # Check for diagonals
        diagonal1 = [board[0][0], board[1][1], board[2][2]]
        diagonal2 = [board[0][2], board[1][1], board[2][0]]

        is_diag1_win, diag1_sign, diag1_xy = check_cells(diagonal1)
        if is_diag1_win:
            win_moves[diag1_sign].append((diag1_xy, diag1_xy))

        is_diag2_win, diag2_sign, diag2_x = check_cells(diagonal2)
        if is_diag2_win:
            y = {0: 2, 1: 1, 2: 0}
            win_moves[diag2_sign].append((diag2_x, y[diag2_x]))

        return win_moves

    @staticmethod
    def random_move(move_list):
        """Static method that returns random chosen move from move_list."""
        return choice(move_list)
