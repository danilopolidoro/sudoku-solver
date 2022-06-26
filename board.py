from copy import deepcopy
import pandas as pd

class Board:

    def __init__(self, db=None, options = None):
        self.__DB = [[None for _ in range(9)] for _ in range(9)]
        if db != None:
            for x_i in range(9):
                for y_i in range(9):
                    self.__DB[x_i][y_i] = {db[x_i][y_i]} if db[x_i][y_i] != None else None
        
        if options != None:
            self.__all_options = set(options)
        else:
            self.__all_options = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    
    def getCleanDB(self):
        base_db = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if self.__DB[i][j] != None:
                    base_db[i][j] = list(self.__DB[i][j])[0]
        return base_db
    
    def getDF(self):
        return pd.DataFrame(self.getCleanDB())

    def __str__(self):
        pretty = self.getDF()
        return str(pretty)

    def setItem(self, x, y, item):
        # set an item to a specific position
        self.__DB[y][x] = item

    def getItem(self, x, y):
        # get the item in the specific position (null if none)
        return self.__DB[y][x]

    def applyOptionMatrix(self, opt_mx:list):
        for x_i in range(9):
            for y_i in range(9):
                candidate = opt_mx[y_i][x_i]
                if type(candidate) == set:
                    if len(candidate) == 1:
                        self.setItem(x_i, y_i, candidate)

    def getLocalGrid(self, x, y) -> set:
        # get the 3x3 grid enclosing the specific position
        start_x = ((x//3)+1)*3-3
        start_y = ((y//3)+1)*3-3
        base_grid_set = set()
        for x_i in range(3):
            for y_i in range(3):
                local_set = self.getItem(start_x+x_i, start_y+y_i)
                base_grid_set = base_grid_set | local_set if type(
                    local_set) == set else base_grid_set
        return base_grid_set

    def getRow(self, x, y) -> set:
        # get the elements of a row, given a specific position
        base_set = set()
        for i in range(9):
            local_set = self.getItem(i, y)
            base_set = base_set | local_set if type(
                local_set) == set else base_set
        return base_set

    def getColumn(self, x, y) -> set:
        # get the elements of a column, given a specific position
        base_set = set()
        for i in range(9):
            local_set = self.getItem(x, i)
            base_set = base_set | local_set if type(
                local_set) == set else base_set
        return base_set

    def getOptions(self, x, y) -> set:
        # return a set of possible options for a given position
        if self.getItem(x,y) == None: # make sure it's an open position
            all_options = self.__all_options - self.getLocalGrid(x, y) - self.getRow(x, y) - self.getColumn(x, y)
            if len(all_options) == 0:
                raise Exception("Impossible to solve!")
            return all_options
        return self.getItem(x,y)

    def getOptionsMatrix(self, threshold = 10):
        # get a 9x9 matrix of suitable next items given the current board (one at a time)
        blank_matrix = [[None for _ in range(9)] for _ in range(9)]
        for x in range(9):
            for y in range(9):
                candidate = self.getOptions(x, y)
                blank_matrix[y][x] = candidate if len(
                    candidate) <= threshold and self.getItem(x,y) == None else None
        return blank_matrix
    
    def is_solved(self) -> bool:
        next_step = self.getOptionsMatrix(10)
        for i in range(9):
            for j in range(9):
                if next_step[i][j] != None:
                    return False
        return True

    def is_impossible(self) -> bool:
        try:
            self.getOptionsMatrix(10)
            return False
        except:
            return True
    
    

