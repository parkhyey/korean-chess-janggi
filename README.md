# korean-chess-janggi

This program simulates an abstract board game called Janggi, aka Korean Chess. This was created by myself as a final project for the python class. It was my first big project and completed in about a week. I spent quite some time thinking of the algorithms for check and checkmate scenarios and enjoyed the process of solving each piece of puzzles.

The game is similar to Chess but has some differences. My program follows the general rules on the Wikipedia page https://en.wikipedia.org/wiki/Janggi but excludes rules regarding perpetual check, position repetition, and any kind of draw or the miscellaneous rules to align with the project requirements in class.

The program does not have GUI, and here is a very simple example of how the JanggiGame class could be used:
```python
game = JanggiGame()
game.make_move('c1', 'e3') #return False because it's not Red's turn
game.make_move('a7', 'b7') #True
game.is_in_check('blue') #False
game.make_move('a4', 'a5') #True
game.get_game_state() #return UNFINISHED
game.make_move('b7', 'b6') #True
game.make_move('b3', 'b6') #return False because it's an invalid move
game.make_move('a1', 'a4') #True
game.make_move('c7', 'd7') #True
game.make_move('a4', 'a4') #pass Red's turn and return True
```

## Basic Rules
It is played on a board nine lines wide by ten lines long.
Blue and Red are the competing players and Blue is the starting player.
The game ends when one player checkmates the other’s general.

## Boards
### Base board:
Locations on the board is specified using algebraic notation, with columns labeled a-i and rows labeled 1-10.
spacer
### Current board:
With row 1 being the Red side and row 10 the Blue side, the initial board setup has the Elephant transposed with the Horse, on the right side, as seen on the image from Wikipedia.
```
------This is the base board-------
a1  b1  c1  d1  e1  f1  g1  h1  i1  
a2  b2  c2  d2  e2  f2  g2  h2  i2  
a3  b3  c3  d3  e3  f3  g3  h3  i3  
a4  b4  c4  d4  e4  f4  g4  h4  i4  
a5  b5  c5  d5  e5  f5  g5  h5  i5  
a6  b6  c6  d6  e6  f6  g6  h6  i6  
a7  b7  c7  d7  e7  f7  g7  h7  i7  
a8  b8  c8  d8  e8  f8  g8  h8  i8  
a9  b9  c9  d9  e9  f9  g9  h9  i9  
a10 b10 c10 d10 e10 f10 g10 h10 i10 
-----------------------------------
```

- Player Red : RC=RedChariot, RE=RedElephant, RH=RedHorse, RG=RedGuard, RK=RedGeneral, RN=RedCannon, RS=RedSoldier
- Player Blue : BC=BlueChariot, BE=BlueElephant, BH=BlueHorse, BG=BlueGuard, BK=BlueGeneral, BN=BlueCannon, BS=BlueSoldier

```
-----This is the current board-----
RC  RE  RH  RG  OO  RG  RE  RH  RC 
OO  OO  OO  OO  RK  OO  OO  OO  OO 
OO  RN  OO  OO  OO  OO  OO  RN  OO 
RS  OO  RS  OO  RS  OO  RS  OO  RS 
OO  OO  OO  OO  OO  OO  OO  OO  OO 
OO  OO  OO  OO  OO  OO  OO  OO  OO 
BS  OO  BS  OO  BS  OO  BS  OO  BS 
OO  BN  OO  OO  OO  OO  OO  BN  OO 
OO  OO  OO  OO  BK  OO  OO  OO  OO 
BC  BE  BH  BG  OO  BG  BE  BH  BC 
-----------------------------------
```

## Main methods
- An init method that initializes any data members.
- A method called get_game_state that just returns one of these values, depending on the game state: ‘UNFINISHED’ or ‘RED_WON’ or ‘BLUE_WON’.
- A method called is_in_check that takes as a parameter either ‘red’ or ‘blue’ and returns True if that player is in check, but returns False otherwise.
- A method called make_move that takes two parameters – strings that represent the square to move from and the square to move to. For example, make_move('b3', 'b10'). If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the indicated move is not legal, or if the game has already been won, then it should just return False. Otherwise it should make the indicated move, remove any captured piece, update the game state if necessary, update whose turn it is, and return True.
- If the make_move method is passed the same string for the square moved from and to, it should be processed as the player passing their turn, and return True.
- When make_move is called,
```
check game status if still ‘UNFINISHED’ –> if not, invalid move, return False
check if the player is passing the turn –> if yes, return True
find indexes for move_from and move_to locations
check both positions’ occupying pieces if invalid –> if invalid, return False
call call_moves to check all possible moves for current piece
if the move_to location is among the possible moves
save the current board and make the move
check if the move puts or leaves their general in check.(I call it _selfcheck)
if not, update the player’s turn
check if the opposing general is in check
if yes, call is_checkmate to check if it’s checkmate
```

## Piece-specific Rules
- Generals and Guards aren’t allowed to leave the palace.
- Horses and Elephants can be blocked.
- Cannons cannot capture or jump over other cannons.

## Check and Checkmate
- A general is in check if it could be captured on the opposing player’s next move.
- A player cannot make a move that puts or leaves their general in check.
- The game ends when one player checkmates the other’s general. Players don’t actually capture a general, instead they have to put it in such a position that it cannot escape being in check, meaning that no matter what, it could be captured on the next move. This works the same as in chess, if you’re familiar with that game.

## Other rules
- Unlike chess, Janggi allows you to pass a turn and thus there is no stalemate (a scenario when no legal moves can be made).
