# Solve N-queens problems using Simulated annealing algorithm
'''
YOUR TASKS:
1. Read the code to understand
2. Implement the simulated_annealing() function
3. (Optinal) Try other shedule() functions
4. (Optinal) Add GUI, animation...
'''

import sys
from collections import deque
import numpy as np
import random

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        #next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        next_node = Node(next_state, self, action)
        return next_node
# ______________________________________________________________________________

class NQueensProblem:
    """The problem of placing N queens on an NxN board with none attacking each other. 
    A state is represented as an N-element array, where a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been filled in yet. We fill in columns left to right.
    
    Sample code: iterative_deepening_search(NQueensProblem(8))
    Result: <Node (0, 4, 7, 5, 2, 6, 1, 3)>
    """

    def __init__(self, N):
        #self.initial = initial 
        self.initial = tuple([-1]*no_of_queens)  # -1: no queen in that column
        self.N = N

    def actions(self, state):
        """In the leftmost empty column, try all non-conflicting rows."""
        if state[-1] is not -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            #return [(col, row) for row in range(self.N)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        """Place the next queen at the given row."""
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return tuple(new)

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)  # same / diagonal

    def value(self, node): 
        """Return (-) number of conflicting queens for a given node"""
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return -num_conflicts 


''' USE OTHER SCHEDULE FUNCTION IF YOU WANT TO '''
def schedule(t, k=20, lam=0.005, limit=1000):
    """One possible schedule function for simulated annealing"""
    return (k * np.exp(-lam * t) if t < limit else 0) 


''' WRITE THIS FUNCTION: '''
def simulated_annealing(problem):
    """See [Figure 4.5] for the algorithm."""
    current = Node(problem.initial)
    init = current
    for t in range(1,sys.maxsize):
        T = schedule(t)
        if(T == 0):
            return current.state

        list_expand = current.expand(problem)

        if(len(list_expand) == 0): 
            current = init
            continue

        next_index = random.randint(0,len(list_expand) - 1 )
        next = list_expand[next_index]

        if len(list_expand) == 1 and all(node != -1 for node in list_expand[0].state):
            return next.state

        deltaE = problem.value(next) - problem.value(current)

        if(deltaE > 0):
            current = next
        else:
            probability = 1/np.exp(deltaE/T)
            choice = np.random.choice([0,1],p = [1-probability,probability])
            if choice == 1:
                current = next

if __name__ == '__main__':
    no_of_queens = 15;
    problem1 = NQueensProblem(no_of_queens)
    result1 = simulated_annealing(problem1)          
    print(result1)
