# Sudoku
Sudoku Game from Scratch

  The idea of this repo comes from a friends' chat. One friend needs to design a Sudoku GUI, which game is quite popular among us but none has ever thought about writing a GUI by ourselves. This project sounds very interesting and can be a good training on both algorithms and GUI development. Thus, I spent some time researching and developing this Sudoku repo.
  The key file is the "Sudoku Game.py", which includes all the implementation of both Sudoku algorithms and GUI design.
  As for the algorithm part, two similar but slightly different algorithms have been developed to solve Sudoku games using depth-first searching (DFS) algorithms. So far, the difficulty levels of generated new games are determined based on numbers of cells to fill. This strategy seems intuitive but may not be the best one. However, in order to ensure solution uniqueness for all generated new games, this strategy is conveniently adopted.
  GUI section mainly relies on the pygame module. The interface not only allows players to make changes to the gaming board, but also incorporates some useful functionalities including staring over and giving hints. Players will be able to play a Sudoku game with all the fundermental elements implemented. 
