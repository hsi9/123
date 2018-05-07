"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        ##target_value = (col + self._width * target_row)
        if self._grid[target_row][target_col] == 0:
            for col in range(target_col + 1, self._width):
                if (target_row, col) != self.current_position(target_row, col):
                    return False
            for row_below in range(target_row + 1, self._height):                
                for col_below in range(self._width):
                    if (row_below, col_below) != self.current_position(row_below, col_below):
                        return False
            return True
        return False
        
    def move(self, target_row, target_col, row, col):
        '''
        place a tile on the target position
        '''
        move_list = ''
        combo = 'druld'
        
        col_delta = target_col - col
        row_delta = target_row - row
        
        move_list += row_delta * 'u'
        
        if col_delta == 0:
            move_list += 'ld' + (row_delta - 1) * combo
        else:
            if col_delta > 0:
                move_list += col_delta * 'l'
                if row == 0:
                    move_list += (abs(col_delta) - 1) * 'drrul'
                else:
                    move_list += (abs(col_delta) - 1) * 'urrdl'
            elif col_delta < 0:
                move_list += (abs(col_delta) - 1) * 'r'
                if row == 0:
                    move_list += abs(col_delta) * 'rdllu'
                else:
                    move_list += abs(col_delta) * 'rulld'
            move_list += row_delta * combo
        return move_list
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        row, column = self.current_position(target_row, target_col)
        move_list = self.move(target_row, target_col, row, column)
        
        self.update_puzzle(move_list)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_list

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        move_list = 'ur'
        self.update_puzzle(move_list)
        
        row, column = self.current_position(target_row, 0)
        if row == target_row and column == 0:
            step = (self.get_width() - 2) * 'r'
            self.update_puzzle(step)
            move_list += step
        else:
            step = self.move(target_row - 1, 1, row, column)
            step += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'
            self.update_puzzle(step)
            move_list += step
            
        return move_list

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.get_number(0, target_col) == 0:
            return False
        
        for column in range(self.get_width()):
            for row in range(self.get_height()):
                if (row == 0 and column > target_col) or (row == 1 and column >= target_col) or row > 1:
                    if not (row, column) == self.current_position(row, column):
                        return False
        return True
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.lower_row_invariant(1, target_col):
            return False
        
        for column in range(target_col + 1, self.get_width()):
            if not (0, column) == self.current_position(0, column):
                return False            
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_list = 'ld'
        self.update_puzzle(move_list)
        
        row, column = self.current_position(0, target_col)
        if row == 0 and column == target_col:
            return move_list
        else:
            step = self.move(1, target_col - 1, row, column)
            step += 'urdlurrdluldrruld'
            self.update_puzzle(step)
            move_list += step
        
        assert self.row1_invariant(target_col - 1)
        return move_list
        

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        row, column = self.current_position(1, target_col)
        move_list = self.move(1, target_col, row, column)
        move_list += 'ur'
        self.update_puzzle(move_list)
        return move_list
    
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        step = ''
        if self.get_number(1, 1) == 0:
            move_list = 'ul'
            self.update_puzzle(move_list)
            if (0, 1) == self.current_position(0, 1) and (1, 1) == self.current_position(1, 1):
                return move_list
            
            if self.get_number(0, 1) < self.get_number(1, 0):
                step += 'rdlu'
            else:
                step += 'drul'
            self.update_puzzle(step)
            move_list += step
        return move_list

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_list = ''
        row = self.get_height() - 1
        column = self.get_width() - 1
        
        row_current, column_current = self.current_position(0, 0)
        
        column_delta = column_current - column
        row_delta = row_current - row
        step = abs(column_delta) * 'r' + abs(row_delta) * 'd'
        self.update_puzzle(step)
        move_list += step
        
        for dummy_row in range(row, 1, -1):
            for dummy_column in range(column, 0, -1):
                move_list += self.solve_interior_tile(dummy_row, dummy_column)
            move_list += self.solve_col0_tile(dummy_row)
            
        for dummy_column in range (column, 1, -1):
            move_list += self.solve_row1_tile(dummy_column)
            move_list += self.solve_row0_tile(dummy_column)
            
        move_list += self.solve_2x2()
        return move_list
# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
