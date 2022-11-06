## Tic Tac Toe game with AI bots.

A Tic Tac Toe game script with command line UI.

To start the program run main.py.

User interface commands are:

* **start player_type player_type** - starts the game with defined palyers

* **exit** - exits the game

Available player's types are:
* **user** - a human player
* **easy** - an easy AI bot that picks a random move
* **medium** - a medium AI bot that will make finishing/ blocking move if available
* **hard** - an unbeatable hard AI bot that evaluates every move based on minimax algorithm 


The program uses a [Backtracking minimax algorithm](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/) for hard AI bot that evaluates every move and performs the most efficient one. The hard bot is unbeatable.
