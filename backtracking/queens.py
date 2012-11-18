import sys
import copy


class QueensBoard(object):
    __slots__ = ("board", "size", "pop")

    def __init__(self, size):
        self.board = [[None for i in range(size)] for i in range(size)]
        self.size = size
        self.pop = 0

    def __str__(self):
        retString = ''
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    retString = retString + ' -'
                else:
                    retString = retString + ' Q'
            retString = retString + '\n'
        return retString


def successors(configuration):
    neighbors = []
    for i in range(configuration.size):
        for j in range(configuration.size):
            if configuration.board[i][j] is None:
                newNeighbor = copy.deepcopy(configuration)
                newNeighbor.board[i][j] = 'Q'
                newNeighbor.pop += 1
                if isPlacementValid(newNeighbor, i, j):
                    neighbors.append(newNeighbor)
    return neighbors


def successorsOpt(configuration):
    neighbors = []
    row = configuration.pop
    for col in range(configuration.size):
        newNeighbor = copy.deepcopy(configuration)
        newNeighbor.board[row][col] = 'Q'
        newNeighbor.pop += 1
        if isPlacementValid(newNeighbor, row, col):
            neighbors.append(newNeighbor)
    return neighbors


def isValid(configuration):
    for i in range(configuration.size):
        for j in range(configuration.size):
            if configuration.board[i][j] is not None:
                valid_col = _isValidColDown(configuration, i, j)
                valid_row = _isValidRowRight(configuration, i, j)
                valid_diag = _isValidDiagDown(configuration, i, j)
                if not (valid_col and valid_row and valid_diag):
                    return False
    return True


def isPlacementValid(configuration, i, j):
    valid_col = _isValidColUp(configuration, i, j)
    valid_diag = _isValidDiagUp(configuration, i, j)
    return (valid_col and valid_diag)


def _isValidRowRight(configuration, i, j):
    for col in range(j + 1, configuration.size):
        if configuration.board[i][col] is not None:
            return False
    return True


def _isValidColDown(configuration, i, j):
    for row in range(i + 1, configuration.size):
        if configuration.board[row][j] is not None:
            return False
    return True


def _isValidDiagDown(configuration, i, j):
    row = i + 1
    col_l = j - 1
    col_r = j + 1
    while (row < configuration.size) and ((col_l > 0) or (col_r < configuration.size)):
        if (col_l > 0) and (configuration.board[row][col_l] is not None):
            return False
        if (col_r < configuration.size) and (configuration.board[row][col_r] is not None):
            return False
        row += 1
        col_r += 1
        col_l -= 1
    return True


def _isValidColUp(configuration, i, j):
    for row in range(0, i):
        if configuration.board[row][j] is not None:
            return False
    return True


def _isValidDiagUp(configuration, i, j):
    row = i - 1
    col_l = j - 1
    col_r = j + 1
    while (row >= 0) and ((col_l >= 0) or (col_r < configuration.size)):
        if (col_l >= 0) and (configuration.board[row][col_l] is not None):
            return False
        if (col_r < configuration.size) and (configuration.board[row][col_r] is not None):
            return False
        row -= 1
        col_r += 1
        col_l -= 1
    return True


def isGoal(configuration):
    return isValid(configuration) and (configuration.pop == configuration.size)


def isGoalOpt(configuration):
    return configuration.pop == configuration.size


def solve(configuration):
    # if we hit a goal, return it
    if isGoal(configuration):
        return configuration

    # otherwise, loop through each child
    for child in successors(configuration):
        solution = solve(child)
        if solution != None:
            return solution

    # if none of the soutions are valid, return none
    return None


def solveOpt(configuration):
    # if we hit a goal, return it
    if isGoalOpt(configuration):
        return configuration

    # otherwise, loop through each child
    for child in successorsOpt(configuration):
        solution = solveOpt(child)
        if solution != None:
            return solution

    # if none of the soutions are valid, return none
    return None


def main():
    bsize = int(sys.argv[1])
    initial_board = QueensBoard(bsize)
    try:
        solution = solveOpt(initial_board)
        print 'Found a solution!'
        print(solution)
    except KeyboardInterrupt:
        print 'Aborting!'


if __name__ == '__main__':
    main()
