# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """ 

    from util import Stack

    stack = Stack() # A stack with items in the form: (state, path that leads from the starting point to the state)
    stack.push((problem.getStartState(), [])) # The stack's first item is (starting state, empty path).
    visited = [] # A list of the visited states.
    
    while (stack.isEmpty() == False): # While the stack is not empty:
        current, path = stack.pop() # Pop the stack.
        if (problem.isGoalState(current) == True): # If the current state is the goal, return it's path.
            return path
        if current not in visited: # If the current state has not been previously visited:
            visited.append(current) # Add it to the 'visited' list.
            successors = problem.getSuccessors(current) # Get all the possile next states.
            for suc, act, cost in successors: # For every possible next state:
                if suc not in visited: # If it has not been previously visited: 
                    stack.push((suc, path + [act])) # Add it to the stack, along with its path - which is calculated as follows:
                    # path = 'path that leads from the starting point to the previous state' + 'action that leads from the previous state to this current state'
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    from util import Queue

    queue = Queue() # A queue with items in the form: (state, path that leads from the starting point to the state)
    queue.push((problem.getStartState(), [])) # The queue's first item is (starting state, empty path).
    visited = [] # A list of the visited states.
    
    while (queue.isEmpty() == False): # While the queue is not empty:
        current, path = queue.pop() # Pop the queue.
        if (problem.isGoalState(current) == True): # If the current state is the goal, return it's path.
            return path
        if current not in visited: # If the current state has not been previously visited:
            visited.append(current) # Add it to the 'visited' list.
            successors = problem.getSuccessors(current) # Get all the possile next states.
            for suc, act, cost in successors: # For every possible next state:
                if suc not in visited: # If it has not been previously visited: 
                    queue.push((suc, path + [act])) # Add it to the queue, along with its path - which is calculated as follows:
                    # path = 'path that leads from the starting point to the previous state' + 'action that leads from the previous state to this current state'
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""

    from util import PriorityQueue

    visited = [] # A list of the visited states.
    priority = PriorityQueue() # A priority queue with items in the form: ((state, path that leads from the starting point to the state, path's cost), path's cost)
    priority.push((problem.getStartState(), [], 0), 0) # The queue's first item is ((starting state, empty path, 0), 0).
    """
    Since 'pop' only returns an item without its cost/priority - wich is a variable I needed for my implementation - I had to
    include the path cost in the item form passed with the 'push(item, priority)' function, while also passing it seperately as the priority variable.
    """
    
    while (priority.isEmpty() == False): # While the queue is not empty:
        current, path, cost = priority.pop() # Pop the queue.
        if (problem.isGoalState(current) == True): # If the current state is the goal, return it's path.
            return path
        if current not in visited: # If the current state has not been previously visited:
            visited.append(current) # Add it to the 'visited' list.
            successors = problem.getSuccessors(current) # Get all the possile next states.
            for suc, act, cos in successors: # For every possible next state:
                if suc not in visited: # If it has not been previously visited: 
                    priority.push((suc, path + [act], cost + cos), cost + cos) 
                    # Add it to the queue, along with its path and the path's cost - which are calculated as follows:
                    # path = 'path that leads from the starting point to the previous state' + 'action that leads from the previous state to this current state'
                    # cost = 'cost of the path that leads from the starting point to the previous state' + 'cost of the action that leads from the previous state to this current state'
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    from util import PriorityQueue

    priority = PriorityQueue() # A priority queue with items in the form: ((state, path that leads from the starting point to the state, path's cost), path's cost)
    priority.push((problem.getStartState(), [], 0), 0) # The queue's first item is ((starting state, empty path, 0), 0).
    visited = [] # A list of the visited states.
    
    while (priority.isEmpty() == False): # While the queue is not empty:
        current, path, cost = priority.pop() # Pop the queue.
        if (problem.isGoalState(current) == True): # If the current state is the goal, return it's path.
            return path
        if current not in visited: # If the current state has not been previously visited:
            visited.append(current) # Add it to the 'visited' list.
            successors = problem.getSuccessors(current) # Get all the possile next states.
            for suc, act, cos in successors: # For every possible next state:
                if suc not in visited: # If it has not been previously visited: 
                    priority.push((suc, path + [act], cost + cos), cost + cos + heuristic(suc, problem)) 
                    """ Add it to the queue, along with its path, the path's cost, and the priority - which are calculated as follows:
                    path = 'path that leads from the starting point to the previous state' + 'action that leads from the previous state to this current state'
                    cost = 'cost of the path that leads from the starting point to the previous state' + 'cost of the action that leads from the previous state to this current state'
                    priority = cost + 'the estimated cost from the current state to the goal'
                    """
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
