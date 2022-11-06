from game_board import GameBoard
from player import Player, HumanPlayer, Bot


class TicTacToe:
    """This is a class representing Tic Tac Toe game

    Attributes:
        player1 (Player object): A Human or Bot player playing 'X' sign
        player2 (Player object): A Human or Bot player playing 'O' sign
        current_player (Player object): A player1 or player2 playing current
                                        game's turn
        game_board (GameBoard object): The game board of Tic Tac Toe game

    """

    def __init__(self, player_1, player_2):
        """The constructor for TicTacToe class.
        Parameters:
            player_1 (str): String defining the type of the player used for
                            constructing Player object('user' - Human Player
                            or 'easy', 'medium', 'hard' - Bot Player)
            player_2 (str): String defining the type of the player used for
                            constructing Player object('user' - Human Player
                            or 'easy', 'medium', 'hard' - Bot Player)

        """
        self.player1 = self.set_up_player(player_1)
        self.player2 = self.set_up_player(player_2)
        self.current_player = self.player1
        self.game_board = GameBoard()
        print(self.game_board)

    def make_move(self):
        """Method responsible for making current player's move
        Invoking Player.get_cords method - returns x and y coordinates
        Invoking GameBoard.input_to_board - inputting current player's sign
        into the game board on X and Y coordinates
        """
        game_board = self.game_board.get_board()
        cord_x, cord_y = self.current_player.get_cords(game_board)
        self.game_board.input_to_board(cord_x, cord_y,
                                       self.current_player.sign)

    def play_turn(self):
        """Method representing one turn in Tic Tac Toe game, invoking all
        necessary methods to complete a turn. Makes current player move,
        prints current game board, changing the current player for the next turn
        Returns if the game is finished.
        """
        self.make_move()
        print(self.game_board)
        self.change_current_player()
        return self.game_board.is_board_finished()

    @staticmethod
    def set_up_player(player):
        """Static method to set up the players.
         Params:
            player (str): The string describing the player user or bot.

        Returns:
            Player object: HumanPlayer or Bot object.
         """
        if player == 'user':
            return HumanPlayer()
        else:
            return Bot(bot_level=player)

    @staticmethod
    def print_winner(winner):
        """Static method to print the game winner.
            Params: winner (str): game winner.
        """
        if winner is None:
            print('Draw')
        else:
            print(f'{winner} wins')

    def change_current_player(self):
        """Method changing current_player class attribute
        to player1 or player2.
        """
        if self.current_player is self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


def play_game(p1, p2):
    """Function to play Tic Tac Toe game.
    Creates Tic Tac Toe game object.
    Loops TicTacToe.play_turn() until the game is finished.
    Returns: winner (str)
    """
    game_finished, winner = False, None

    game_instance = TicTacToe(p1, p2)
    while game_finished is False:
        game_finished, winner = game_instance.play_turn()
    return winner


def main():
    """The function to set up a TicTacToe game, get user input and validate it.
    Creates an infinite loop until the user decide to break it with exit command
    """
    _actions = ('start', 'exit')
    _players = ('hard', 'medium', 'easy', 'user')
    while True:
        menu_input = input('Input command:')
        if menu_input == 'exit':
            exit()
        else:
            command = menu_input.split()
            if len(command) != 3:
                print('Bad parameters!')
                continue
            valid = bool(command[0] in _actions
                         and command[1] in _players
                         and command[2] in _players)
            if valid:
                winner = play_game(command[1], command[2])
                TicTacToe.print_winner(winner)
                Player.reset_signs()
                continue
            else:
                print('Bad parameters!')
                continue


if __name__ == '__main__':
    main()
