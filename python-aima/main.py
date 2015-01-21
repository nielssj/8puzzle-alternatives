__author__ = 'niels'

from aima import search
from aima.search import Problem


# Enum class to represent moves, NOTE: Python 2.7 doesn't support real enums :(
class Move:
    UP, DOWN, LEFT, RIGHT = range(4)

# Problem definition for Eight-puzzle
class EightPuzzle(Problem):
    # Number of steps and direction to move depending on action
    action_steps = [-3, 3, -1, 1]

    # The actions that can be executed in the given state
    # (UP, DOWN, LEFT and/or RIGHT depending on position of 0)
    def actions(self, state):
        valid_moves = [
            [Move.DOWN, Move.RIGHT],
            [Move.DOWN, Move.LEFT, Move.RIGHT],
            [Move.DOWN, Move.LEFT],
            [Move.UP, Move.DOWN, Move.RIGHT],
            [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT],
            [Move.UP, Move.DOWN, Move.LEFT],
            [Move.UP, Move.RIGHT],
            [Move.UP, Move.LEFT, Move.RIGHT],
            [Move.UP, Move.LEFT]
        ]
        position = state.index(0) # Current position is the index where 0 is at

        return valid_moves[position]

    # Return the state that results from executing the given action in the given state.
    # (Moving 0 in one of the four directions)
    def result(self, state, action):
        state_l = list(state)

        # Decide number of steps and direction depending on action
        steps = self.action_steps[action]

        # Move 0 the given number of steps forward or backwards (positive/negative "steps" value)
        f = state_l.index(0)
        t = f + steps
        state_l[f], state_l[t] = state_l[t], state_l[f]

        return tuple(state_l)

# Very simple heurestic (non-admissable) that just considers linear distance from goal
def heurestic_simple(node): # Note assumes goal is (0, 1, 2, 3, 4, 5, 6, 7, 8)
    state_l = list(node.state)
    sum = 0
    for pos, tile in enumerate(state_l):
        sum += abs(pos - tile)
    return sum

# Manhatten distance based heurestic (admissable)
def heurestic_manhatten(node):
    state_l = list(node.state)
    sum = 0
    for pos, tile in enumerate(state_l):
        t_row = tile / 3                    # target row
        t_col = tile % 3                    # target column
        c_row = pos / 3                     # current row
        c_col = pos % 3                     # current column
        sum += abs(t_row - c_row) + abs(t_col - c_col)  # delta_row + delta_col
    return sum

# goal state
goal = (0, 1, 2,
        3, 4, 5,
        6, 7, 8)

# Initial state
s_init = (1, 6, 4,
          8, 7, 0,
          3, 2, 5)

# Instantiate problem
problem = EightPuzzle(s_init, goal)

# Solve problem using A*
result = search.astar_search(problem, heurestic_manhatten)

# Resulting list of moves
solution = result.solution()

# Print solution
print "Solution with %d moves: " % len(solution)
moves = ""
for move in solution:
    move_str = ["UP", "DOWN", "LEFT", "RIGHT"][move]
    moves += move_str + ", "
print moves.rstrip(',')