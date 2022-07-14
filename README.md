# ChessGame
A custom chess game that uses Tkinter to visualize a chess board. The ChessMain.py file setups up the game. 
The top level class for the chess game is the Game.GameMaster.py class. 

## Installation
Install the requirements using requirements.txt and use python 3.10

### Run the game
Run the ChessMain.py file and you are good to go!

### Work in progress
- Some rules of the game of chess are not yet implemented
  - Castling
  - Promotion
  - Checking does not prevent movement of unchecking moves
- Resolution of the game (i.e. there are no more moves to be made) is not yet functional
- Resigning is not yet possible.
- The AIPlayer who iteratively learns using MachineLearning is not yet functional
- The GUI does not display the clock.

###ake sure that the "home" location in the python venv/pyvenv.cfg is set to the base interpreter for python. 
1) Open anaconda prompt and type in "where python"
2) Open the venv/pyvenv.cfg file with notepad
3) Copy the return of 1) after the "home" keyword. For me the file looks like this:

home = C:\Users\tijme\AppData\Local\Continuum\anaconda3
include-system-site-packages = false
version = 3.10