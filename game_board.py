class GameBoard:
    """Class representing game board of Tic Tac Toe game.

    Attributes:
        board (list): A list representing lists of TicTacToe game board rows.
        winner (str): String representing winner if game is not finishedd
        the winner is None
        empty_cells (list): List of tuples representing (x,y) coordinates
                            of empty cells
    """

    def __init__(self, board=None):
        """The constructor for GameBoard class
        Params:
            board (list): Default = None, used to construct GameBoard object
                          using existing list of rows
        """
        if board is not None:
            self.board = board
        else:
            self.board = [
                [' ', ' ', ' '],
                [' ', ' ', ' '],
                [' ', ' ', ' '],
            ]
        self.winner = None
        self.empty_cells = self.get_empty_cells(self.board)

    def input_to_board(self, x, y, sign):
        """Method to put 'X' or 'O' sign into board's cell.

        Params:
            x (int): X coordinate - row number.
            y (int): Y coordinate - column number.
            sign (str): sign to be inserted into the board's cell.
        """
        self.board[x][y] = sign
        self.empty_cells.remove((x, y))

    def board_empty_cells(self):
        """Returns board's object empty cells"""
        return self.get_empty_cells(self.board)

    def is_board_finished(self):
        """Method to evaluate the game board's state.

        Returns: True, winner if the game board is finished.
                 False, None if the game is not finished.
        """
        _is_finished, winner = self.is_finished(self.board)
        return (True, winner) if _is_finished else (False, None)

    def get_board(self, row_format=False, string_format=False):
        """Method used to return current board.
        Params:
        row_format (bool): if True returns row1, row2, row3
        string_format(bool): if True returns board in '___X_O_XO' format
        Returns:
            board.copy(): Copy of a board attribute.
        """
        if row_format:
            row1, row2, row3 = self.board
            return row1, row2, row3
        elif string_format:
            str_board = ''
            for row in self.board:
                str_board += ''.join(row).replace(' ', '_')
            return str_board
        else:
            return self.board.copy()

    def get_winner(self):
        """Method to return winner attribute of GameBoard."""
        return self.winner

    @staticmethod
    def get_empty_cells(board):
        """"Static method to create list of empty cells coordinates:

        Params: board (list): TicTacToe game board list of rows.

        Returns: empty (list): List of (X,Y) coordinates tuples of board
                 empty cells.
        """
        empty = []
        for row_no, row in enumerate(board):
            for cell_no, cell in enumerate(row):
                if cell == ' ':
                    empty.append((row_no, cell_no))
        return empty

    @staticmethod
    def is_finished(board, string=False):
        """Static method to evaluate if game board is finished.

        Params:
            board (list): TicTacToe game board list of rows.
            string (bool): Shows if the board is in string format.

        Returns:
            bool (bool): True if game is finished else False
            winner (str/None): winner of the game if exists else None
        """
        if string:
            board = GameBoard.from_string(board, init=False)
        row1, row2, row3 = board
        for i in range(3):
            # looks for win in column
            if row1[i] == row2[i] == row3[i] and row1[i] != ' ':
                return True, row1[i]
            # look for win in row
            elif len(set(board[i])) == 1 and ' ' not in board[i]:
                return True, board[i][0]
        # look for win in diagonals
        if row1[0] == row2[1] == row3[2] != ' ':
            return True, row1[0]
        elif row1[-1] == row2[-2] == row3[-3] != ' ':
            return True, row1[-1]
        # checks if there is free space
        elif ' ' not in row1 + row2 + row3:
            return True, None
        else:
            return False, None

    @classmethod
    def from_string(cls, string, init=True):
        """Class method used to construct the GameBoard object from string.
        Params:
            string (str): String representing the TicTacToe board '___XO_XOO'
            init (bool): Orders if to construct the GameBoard object or return
                         list of rows

        Returns:
            Creating GameBoard object if init is True else returns:
            board (list): List of rows of TicTacToe game board
        """
        board = [list(string[i: i + 3].replace('_', ' ')) for i in
                 range(0, 9, 3)]
        return cls(board) if init else board

    def __str__(self):
        """User friendly view of current board state"""
        board_view = '---------\n'
        for row in self.get_board(row_format=True):
            board_view += f'| {" ".join(row)} |\n'
        board_view += '---------'
        return board_view
