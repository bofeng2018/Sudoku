# This file demonstrates how to design a Sudoku game from scratch. "pygame" is heavily involved in the GUI design
# section.

from random import shuffle, seed
import time
import pygame
from pygame.locals import (
    K_ESCAPE, KEYDOWN, QUIT, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP1, K_KP2, K_KP3, K_KP4,
    K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_DELETE, MOUSEBUTTONDOWN
)


class Sudoku:

    def __init__(self, grid=None, random_state=None):
        """
        Initiate the Sudoku class with optional user-defined Sudoku grid and random seed to enforce reproducibility.

        :param grid: (optional) a user-defined Sudoku grid to solve.
        :param random_state: (optional) a user-defined random seed to generate reproducible results.
        """
        if random_state is not None:
            self.seed = random_state
        else:
            self.seed = None
        if grid is None:
            self.grid = [[0] * 9 for _ in range(9)]
        else:
            self.grid = [row.copy() for row in grid]

    def solver(self, array=None, method="inorder", random_state=None, verbose=True):
        """
        Solve the given Sudoku game with one of the two available methods, i.e. "inorder" or "sorted". All the cells to
        be filled will be shuffled. "inorder" means to fill the cells in the order that they are shuffled to be, while
        "sorted" means to fill the cells such that cells with least possible candidate numbers will be filled first.
        The idea behind those two algorithms is that obviously, filling the cells with least possibilities first is at
        least as good as not doing so in terms of performance. However, sorting itself can be costly. Then, there might
        not an obvious winner here in terms of overall performance. Thus, two methods are provided.

        :param array: (optional) Sudoku grid to solve. If not specified, self.grid will be used.
        :param method: (optional) Specify either the "inorder" or the "sorted" method to use. The default is to use the
            "inorder" method.
        :param random_state: (optional) a user-defined random seed to generate reproducible results.
        :param verbose: (optional) Decide whether to print messages. The default is to print them.
        :return: a list with 2 components. 1st element is the output from the inside dfs() function. 2nd element is the
            original Sudoku game before being solved.
        """
        if array is None:
            grid = [row.copy() for row in self.grid]
        else:
            grid = [row.copy() for row in array]

        # Trace the valid numbers to fill in terms of rows, columns and blocks. They will be updated whenever a new cell
        # is filled.
        row = [set(range(1, 10)) for i in range(9)]
        col = [set(range(1, 10)) for i in range(9)]
        block = [set(range(1, 10)) for i in range(9)]

        # Save the cells to fill, and numbers of guesses needed to make. A guess is counted if all the current cells to
        # fill have at least two possible valid candidates with no immediate rule violation.
        cell = []
        guess = 0

        # Initiate all the tools involved.
        for i in range(9):
            for j in range(9):
                if grid[i][j]:
                    row[i].remove(grid[i][j])
                    col[j].remove(grid[i][j])
                    block[(i // 3) * 3 + j // 3].remove(grid[i][j])
                else:
                    cell.append([i, j])
        if random_state is not None:
            seed(random_state)
            shuffle(cell)
        elif self.seed is not None:
            seed(self.seed)
            shuffle(cell)

        def dfs(method):
            """
            Define the Sudoku solving algorithms.

            :param method: Either "inorder" or "sorted".
            :return: a list with 3 elements. 1st element is whether the Sudoku could be solved. 2nd element is how many
                guesses were made. 3rd element is what numbers were filled in each cell with their positions listed.
            """
            if not cell:
                return [True, 0, []]

            # "inorder" basically means solving the Sudoku by the cell orders originally in "cell".
            if method == "inorder":
                i, j = cell.pop()

                # "pool" lists all the valid candidates for the current cell.
                pool = list(row[i] & col[j] & block[(i // 3) * 3 + j // 3])
                shuffle(pool)
                for num in pool:
                    grid[i][j] = num
                    row[i].remove(num)
                    col[j].remove(num)
                    block[(i // 3) * 3 + j // 3].remove(num)
                    res = dfs("inorder")
                    if res[0]:
                        return [True, res[1] + (len(pool) != 1), [[i, j, num]] + res[2]]
                    grid[i][j] = 0
                    row[i].add(num)
                    col[j].add(num)
                    block[(i // 3) * 3 + j // 3].add(num)

            # "sorted" basically means solving the Sudoku by filling the cells with least possible candidates first.
            elif method == "sorted":
                cell.sort(key=lambda x: [len(row[x[0]] & col[x[1]] & block[(x[0] // 3) * 3 + x[1] // 3]), x],
                          reverse=True)
                i, j = cell.pop()

                # "pool" lists all the valid candidates for the current cell.
                pool = list(row[i] & col[j] & block[(i // 3) * 3 + j // 3])
                shuffle(pool)
                for num in pool:
                    grid[i][j] = num
                    row[i].remove(num)
                    col[j].remove(num)
                    block[(i // 3) * 3 + j // 3].remove(num)
                    res = dfs("sorted")
                    if res[0]:
                        return [True, res[1] + (len(pool) != 1), [[i, j, num]] + res[2]]
                    grid[i][j] = 0
                    row[i].add(num)
                    col[j].add(num)
                    block[(i // 3) * 3 + j // 3].add(num)
            cell.append([i, j])
            return [False, 0, []]

        res = dfs(method)
        if res[0]:
            return [res, grid]
        if verbose:
            print("Not a valid sudoku game!")
        return [res] + ([self.grid] if array is None else [array])

    def generator(self, array=None, difficulty="easy", random_state=None):
        """
        Generate a Sudoku game board. The difficulty is defined by the straightforward criteria of numbers of cells to
        fill. There must be other criteria available. But to enforce solution uniqueness, this difficulty criteria is
        so far the most proper one to work with.

        :param array: (optional) A completed Sudoku board to start with. If not provided, it will be generated
            automatically.
        :param difficulty: (optional) "easy", "medium", "hard" or "super hard". Any value other than the first 3 values
            will be perceived as "super hard". The default is "easy".
        :param random_state: (optional) a user-defined random seed to generate reproducible results.
        :return: A list with Sudoku game board to play with.
        """
        if array is None:
            grid = self.solver(array=[[0] * 9 for _ in range(9)], method="sorted",
                               random_state=random_state)[1]
        else:
            grid = [row.copy() for row in array]
        row = [set() for _ in range(9)]
        col = [set() for _ in range(9)]
        block = [set() for _ in range(9)]
        cell = [[i, j] for i in range(9) for j in range(9)]
        if random_state is not None:
            seed(random_state)
        elif self.seed is not None:
            seed(self.seed)
        shuffle(cell)

        # Number of cells to fill that corresponds to different levels of difficulties.
        bound = 15 if difficulty == "easy" else 25 if difficulty == "medium" else 40 if difficulty == "hard" else 81

        while cell and bound:
            i, j = cell.pop()
            temp = grid[i][j]
            flag = 0
            row[i].add(grid[i][j])
            col[j].add(grid[i][j])
            block[(i // 3) * 3 + j // 3].add(grid[i][j])

            # "pool" lists all the other possible candidates if the current cell is unfilled.
            pool = (row[i] & col[j] & block[(i // 3) * 3 + j // 3]) - {grid[i][j]}
            for p in pool:
                grid[i][j] = p
                if self.solver(array=grid, method="sorted", verbose=False)[0][0]:
                    # If one other candidate that is filled in the current cell, can lead to a valid Sudoku. Then, it
                    # violates the principle of solution uniqueness and the current cell should not be unfilled. In this
                    # case, "flag" will be set to 1.
                    flag = 1
                    break
            if flag:
                grid[i][j] = temp
                row[i].remove(temp)
                col[j].remove(temp)
                block[(i // 3) * 3 + j // 3].remove(temp)
            else:
                grid[i][j] = 0
                bound -= 1

                # The codes commented out below were used to check the number of guesses need to make in solving the
                # current Sudoku game.
        #                 print("Guesses =", self.solver(array = grid, method = "sorted", verbose = False)[0][1])
        #                 print(bound)
        #                 start = time.time()
        #                 self.solver(array = grid, method = "sorted")
        #                 end = time.time()
        #                 print(end - start)
        return grid

    def GUI(self):
        """
        Generate a Sudoku GUI with some simple functionalities enabled.
        """

        # Set up the Sudoku game display and build the key-number HashMap.
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        screen.fill((255, 255, 255))
        running = True
        keys = {K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6, K_7: 7, K_8: 8, K_9: 9,
                K_KP1: 1, K_KP2: 2, K_KP3: 3, K_KP4: 4, K_KP5: 5, K_KP6: 6, K_KP7: 7, K_KP8: 8, K_KP9: 9}

        class Board(pygame.sprite.Sprite):
            def __init__(self):
                """
                Set up the Sudoku board and define necessary functionalities including addGameValue and addPlayerValue.
                """
                super(Board, self).__init__()
                self.surf = pygame.Surface((396, 396))
                self.surf.fill((255, 255, 255))
                self.rect = self.surf.get_rect(center=(270, 280))
                pygame.draw.rect(surface=self.surf, color=(0, 0, 0),
                                 rect=self.surf.get_rect(center=(198, 198)),
                                 width=5)
                for i in range(8):
                    pygame.draw.line(surface=self.surf, color=(0, 0, 0), start_pos=(44 * (i + 1), 0),
                                     end_pos=(44 * (i + 1), 396), width=3 if i in [2, 5] else 1)
                for i in range(8):
                    pygame.draw.line(surface=self.surf, color=(0, 0, 0), start_pos=(0, 44 * (i + 1)),
                                     end_pos=(396, 44 * (i + 1)), width=3 if i in [2, 5] else 1)

            def addGameValue(self, text, x, y):
                """
                Add numbers originally filled in the Sudoku board.

                :param text: Number to be filled.
                :param x: x position.
                :param y: y position.
                """
                if text is not None:
                    font = pygame.font.SysFont("comicsans", 44)
                    img = font.render(text, True, (0, 0, 0))
                    rect = img.get_rect(center=(x, y))
                    self.surf.blit(img, rect)

            def addPlayerValue(self, text, x, y, color):
                """
                Add numbers filled by the player or shade the cell in the Sudoku board.

                :param text: Number to be filled.
                :param x: x position.
                :param y: y position.
                :param color: Colors are added to enable choice between filling a number or just shading the cell.
                """
                if text is not None:  # Add numbers filled by the player.
                    font = pygame.font.SysFont("comicsans", 44)
                    img = font.render(text, True, color)
                    rect = img.get_rect(center=(x, y))
                    self.surf.blit(img, rect)
                else:  # Shade the current cell.
                    rect = pygame.Rect(x + 4, y + 4, 37, 37)
                    pygame.draw.rect(surface=self.surf, color=color, rect=rect, width=0)

        class Option(pygame.sprite.Sprite):
            def __init__(self, center, width, text=None, border=True):
                """
                Add options for the game such as "New Game", "Hint", etc.

                :param center: Center position of the option box.
                :param width: Width of the option box.
                :param text: Text to be added in the option box.
                :param border: Control whether to generate the option box or to cover it.
                """
                super(Option, self).__init__()
                self.surf = pygame.Surface((width, 50))
                self.surf.fill((255, 255, 255))
                self.rect = self.surf.get_rect(center=center)
                pygame.draw.rect(surface=self.surf, color=(0, 0, 0) if border else (255, 255, 255),
                                 rect=self.surf.get_rect(center=(width // 2, 25)),
                                 width=3)

                if text is not None:
                    fnt = pygame.font.SysFont("comicsans", 40)
                    words = fnt.render(text, True, (0, 0, 0))
                    words_rect = words.get_rect(center=(width // 2, 25))
                    self.surf.blit(words, words_rect)

        board = Board()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(board)
        option = []

        # Define the 4 options for the game.
        for i, j in zip(range(4), ["New Game", "Start Over", "Hint", "Finish"]):
            option.append(Option(center=(650, 130 + i * 100), text=j, width=200))
            all_sprites.add(option[-1])

        # Define the difficulty levels.
        level = []
        for i, j in zip(range(3), ["Easy", "Medium", "Hard"]):
            new_level = Option(center=(150 + i * 250, 520), text=j, width=200)
            level.append(new_level)

        # Define the boxes to cover all difficulty levels once one has been selected.
        cover = []
        for i in range(3):
            new_cover = Option(center=(150 + i * 250, 520), border=False, width=200)
            cover.append(new_cover)

        # Define the 2 messages once the player clicks "Finish".
        message = []
        for i, j in zip(range(2), ["Hmm, something doesn't look right.", "Congratulations! You solved it!"]):
            new_message = Option(center=(400, 520), text=j, width=600)
            message.append(new_message)

        # Define the box to cover the message box.
        cover_message = Option(center=(400, 520), border=False, width=600)

        # Define the indicators and object holders.
        rowIndex = colIndex = blockIndex = None
        newgame = False
        rm_message = False
        sequence = []
        rm_hint = False
        toFill = set()
        filled = {}
        row = [set(range(1, 10)) for i in range(9)]
        col = [set(range(1, 10)) for i in range(9)]
        block = [set(range(1, 10)) for i in range(9)]
        clicked = (None, None)
        grid = None

        while running:
            pygame.time.wait(500)  # Enforce a wait time for smooth game experience.
            for event in pygame.event.get():  # Detect the input signal, i.e. mouse clicking or key typing.
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if board.rect.collidepoint(x, y):  # If one cell is clicked.
                        if clicked[0] is not None:  # Check whether the current cell has been selected by last move.
                            if clicked in filled:
                                board.addPlayerValue(text=None, x=clicked[1] * 44,
                                                     y=clicked[0] * 44, color=(255, 255, 255))  # Remove shade.
                                if (rowIndex, colIndex) in filled:
                                    # If already filled, add in the previously filled number.
                                    board.addPlayerValue(text=filled[rowIndex, colIndex], x=colIndex * 44 + 22,
                                                         y=rowIndex * 44 + 22, color=(255, 0, 0))
                            else:
                                board.addPlayerValue(text=None, x=clicked[1] * 44,
                                                     y=clicked[0] * 44, color=(255, 255, 255))  # Remove shade.
                            clicked = (None, None)
                        rowIndex = (y - 82) // 44
                        colIndex = (x - 72) // 44
                        blockIndex = (y - 82) // 132 * 3 + (x - 72) // 132
                        if (rowIndex, colIndex) in toFill:
                            board.addPlayerValue(text=None, x=colIndex * 44,
                                                 y=rowIndex * 44, color=(211, 211, 211))  # Add shade.
                            if (rowIndex, colIndex) in filled:
                                # If already filled, add in the previously filled number.
                                board.addPlayerValue(text=filled[rowIndex, colIndex], x=colIndex * 44 + 22,
                                                     y=rowIndex * 44 + 22, color=(255, 0, 0))
                            clicked = (rowIndex, colIndex)
                    else:  # If areas other than the board is clicked such as the option box.
                        if clicked[0] is not None:
                            board.addPlayerValue(text=None, x=clicked[1] * 44,
                                                 y=clicked[0] * 44, color=(255, 255, 255))  # Remove shade.
                            clicked = (None, None)
                        if (rowIndex, colIndex) in filled:
                            board.addPlayerValue(text=filled[rowIndex, colIndex], x=colIndex * 44 + 22,
                                                 y=rowIndex * 44 + 22, color=(255, 0, 0))
                        rowIndex = colIndex = blockIndex = None
                        if rm_message:  # If the message should be covered.
                            screen.blit(cover_message.surf, cover_message.rect)
                            rm_message = False
                        elif rm_hint:  # If the hint should be covered.
                            screen.blit(cover_message.surf, cover_message.rect)
                            rm_hint = False
                        elif option[0].rect.collidepoint(x, y):  # If "New Game" is clicked.
                            for i in range(3):
                                screen.blit(level[i].surf, level[i].rect)
                            newgame = True
                        elif any(l.rect.collidepoint(x, y) for l in level):  # If a difficulty level is selected.
                            if newgame:
                                # Reset.
                                board.kill()
                                all_sprites.remove(board)
                                board = Board()
                                all_sprites.add(board)

                                if level[0].rect.collidepoint(x, y):
                                    grid = self.generator(difficulty="easy")
                                elif level[1].rect.collidepoint(x, y):
                                    grid = self.generator(difficulty="medium")
                                elif level[2].rect.collidepoint(x, y):
                                    grid = self.generator(difficulty="hard")

                                row = [set(range(1, 10)) for i in range(9)]
                                col = [set(range(1, 10)) for i in range(9)]
                                block = [set(range(1, 10)) for i in range(9)]
                                toFill = set()
                                for i in range(9):
                                    for j in range(9):
                                        if grid[i][j]:
                                            row[i].remove(grid[i][j])
                                            col[j].remove(grid[i][j])
                                            block[i // 3 * 3 + j // 3].remove(grid[i][j])
                                            board.addGameValue(str(grid[i][j]), j * 44 + 22, i * 44 + 22)
                                        else:
                                            toFill.add((i, j))
                                filled = {}

                                for i in range(3):
                                    screen.blit(cover[i].surf, cover[i].rect)
                                newgame = False

                                sequence = self.solver(grid, method="sorted")[0][2]
                        elif newgame:
                            pass
                        elif option[1].rect.collidepoint(x, y):  # If "Start Over" is selected.
                            for i, j in filled.copy():
                                board.addPlayerValue(text=None, x=j * 44,
                                                     y=i * 44, color=(255, 255, 255))
                            row = [set(range(1, 10)) for i in range(9)]
                            col = [set(range(1, 10)) for i in range(9)]
                            block = [set(range(1, 10)) for i in range(9)]
                            toFill = set()
                            if grid is not None:
                                for i in range(9):
                                    for j in range(9):
                                        if grid[i][j]:
                                            row[i].remove(grid[i][j])
                                            col[j].remove(grid[i][j])
                                            block[i // 3 * 3 + j // 3].remove(grid[i][j])
                                            board.addGameValue(str(grid[i][j]), j * 44 + 22, i * 44 + 22)
                                        else:
                                            toFill.add((i, j))
                            filled = {}
                        elif option[2].rect.collidepoint(x, y):  # If "Hint" is selected.
                            for i, j, value in sequence:
                                if int(filled.get((i, j), 0)) != value:
                                    hint_message = Option(center=(400, 520),
                                                          text="Cell at row {} and column {} = {}".format(i + 1, j + 1,
                                                                                                          value),
                                                          width=600)
                                    screen.blit(hint_message.surf, hint_message.rect)
                                    rm_hint = True
                                    break
                        elif option[3].rect.collidepoint(x, y):  # If "Finish" is selected.
                            if any(row) or any(col) or any(block):
                                screen.blit(message[0].surf, message[0].rect)
                            else:
                                screen.blit(message[1].surf, message[1].rect)
                            rm_message = True
                elif event.type == KEYDOWN:  # If a key typing is detected.
                    if event.key == K_ESCAPE:  # If "ESC" is typed.
                        running = False
                    elif rowIndex is not None:  # If a valid position has been clicked.
                        if event.key in keys:  # If a number is typed.
                            if (rowIndex, colIndex) in toFill and (rowIndex, colIndex) not in filled:
                                # In order to avoid accidentally replacing filled numbers, a number in a filled cell
                                # must be deleted before filling in the cell with a different number.
                                board.addPlayerValue(text=None, x=colIndex * 44,
                                                     y=rowIndex * 44, color=(255, 255, 255))
                                board.addPlayerValue(text=str(keys[event.key]), x=colIndex * 44 + 22,
                                                     y=rowIndex * 44 + 22, color=(255, 0, 0))
                                filled[rowIndex, colIndex] = str(keys[event.key])
                                if keys[event.key] in row[rowIndex]:
                                    row[rowIndex].remove(keys[event.key])
                                if keys[event.key] in col[colIndex]:
                                    col[colIndex].remove(keys[event.key])
                                if keys[event.key] in block[rowIndex // 3 * 3 + colIndex // 3]:
                                    block[rowIndex // 3 * 3 + colIndex // 3].remove(keys[event.key])
                        elif event.key == K_DELETE:  # If a "DELETE" is typed.
                            if (rowIndex, colIndex) in filled:
                                board.addPlayerValue(text=None, x=colIndex * 44,
                                                     y=rowIndex * 44, color=(255, 255, 255))
                                cur = int(filled[rowIndex, colIndex])
                                if all(grid[rowIndex][i] != cur for i in range(9)
                                       ) and all(filled[i, j] != filled[rowIndex, colIndex] for i, j in filled
                                                 if i == rowIndex and j != colIndex):
                                    row[rowIndex].add(cur)
                                if all(grid[i][colIndex] != cur for i in range(9)
                                       ) and all(filled[i, j] != filled[rowIndex, colIndex] for i, j in filled
                                                 if i != rowIndex and j == colIndex):
                                    col[colIndex].add(cur)
                                if all(grid[rowIndex // 3 * 3 + i][colIndex // 3 * 3 + j] != cur
                                       for i in range(3) for j in range(3)
                                       ) and all(filled[i, j] != filled[rowIndex, colIndex] for i, j in filled
                                                 if i // 3 == rowIndex // 3 and j // 3 == colIndex // 3 and
                                                    (i != rowIndex or j != colIndex)):
                                    block[rowIndex // 3 * 3 + colIndex // 3].add(cur)
                                del filled[rowIndex, colIndex]

            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
            pygame.display.flip()

        # Quit the game if it finishes running.
        pygame.display.quit()
        pygame.quit()


MySudoku = Sudoku(grid=[[5, 3, 0, 0, 7, 0, 0, 0, 0],
                        [6, 0, 0, 1, 9, 5, 0, 0, 0],
                        [0, 9, 8, 0, 0, 0, 0, 6, 0],
                        [8, 0, 0, 0, 6, 0, 0, 0, 3],
                        [4, 0, 0, 8, 0, 3, 0, 0, 1],
                        [7, 0, 0, 0, 2, 0, 0, 0, 6],
                        [0, 6, 0, 0, 0, 0, 2, 8, 0],
                        [0, 0, 0, 4, 1, 9, 0, 0, 5],
                        [0, 0, 0, 0, 8, 0, 0, 7, 9]])

# Test whether the two solver algorithms work
MySudoku.solver(method="inorder")

MySudoku.solver(method="sorted")

# Test how long each algorithm would take to solver the same problem 1000 times
start = time.time()
for i in range(1000):
    MySudoku.solver(method="inorder")
end = time.time()
print(end - start)

start = time.time()
for i in range(1000):
    MySudoku.solver(method="sorted")
end = time.time()
print(end - start)

# Generate sudoku games by difficulty
MySudoku.generator(difficulty="easy", random_state=123)
MySudoku.generator(difficulty="medium", random_state=123)
MySudoku.generator(difficulty="hard", random_state=123)

# GUI
MySudoku = Sudoku()
MySudoku.GUI()
