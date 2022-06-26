from board import Board
from copy import deepcopy

def is_empty_matrix(mx) -> bool:
    for i in range(9):
        for j in range(9):
            if mx[i][j] != None:
                return False
    return True

def has_simple_solution(game: Board) -> bool:
    return not is_empty_matrix(game.getOptionsMatrix(1))

def branch_solution_matrix(game:Board):
    pass

def solve(g: Board):
    game = deepcopy(g)
    # Impossible? Return None
    if game.is_impossible():
        return
    # Solved? Return solution
    if game.is_solved():
        return game
    if has_simple_solution(game):
        # Unsolved, but simple solution? Apply simple solution
        game.applyOptionMatrix(game.getOptionsMatrix(1))
        return solve(game)
    else:
        # Unsolved but complicated solution? Branch 
        possibilities = game.getOptionsMatrix()
        elected = []
        elected_x = 0
        elected_y = 0
        found = False
        for x in range(9):
            if found:
                break
            for y in range(9):
                if found:
                    break
                if possibilities[y][x] != None:
                    elected = list(possibilities[y][x])
                    elected_x, elected_y = x,y
                    found = True
        for p in elected:
            new_game = deepcopy(game)
            new_game.setItem(elected_x, elected_y, set([p]))
            solved = solve(new_game)
            if solved != None:
                return solved
            




    
  
