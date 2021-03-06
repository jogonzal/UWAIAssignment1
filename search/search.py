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

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

class StateWithHistory:
    "A container class for solving DFS/etc problems."
    def __init__(self, movementHistory, lastCoordinates, accumulatedCost):
        self.movementHistory = movementHistory;
        self.lastCoordinates = lastCoordinates;
        self.hashableState = self.lastCoordinates;
        self.accumulatedCost = accumulatedCost;

    def getMovementHistory(self):
        return self.movementHistory;

    def getLastCoordinates(self):
        return self.lastCoordinates;

    def getHashableState(self):
        return self.hashableState;

    def getAccumulatedCost(self):
        return self.accumulatedCost;

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


def GetStateWithHistoryFromState(currentState, newState):
    if (currentState == None):
        movementHistory = [];
        accumulatedCost = 0;
    else:
        movementHistory = list(currentState.getMovementHistory());
        accumulatedCost = currentState.getAccumulatedCost();

    movementHistory.append(newState[1]);
    coordinates = newState[0];
    accumulatedCost = accumulatedCost + newState[2];

    return StateWithHistory(movementHistory, coordinates, accumulatedCost);


def SolveUsingDataStructure(problem, dataStructure, withCosts, heuristic=nullHeuristic):

    startState = problem.getStartState();
    # Check if we're done
    if (problem.isGoalState(startState)):
        return [];

    l = set(); # To keep track of visited states
    l.add(startState);

    # push successors of the start state
    firstSuccessors = problem.getSuccessors(startState);
    for successor in firstSuccessors:
        successorStateWithHistory = GetStateWithHistoryFromState(None, successor);
        hashableState = successorStateWithHistory.getHashableState()
        if (not hashableState in l):
            if (not withCosts):
                dataStructure.push(successorStateWithHistory);
            else:
                dataStructure.push(successorStateWithHistory, successorStateWithHistory.getAccumulatedCost() + heuristic(successorStateWithHistory.getLastCoordinates(), problem));


    while not dataStructure.isEmpty():
        # Process the current item
        currentStateWithHistory = dataStructure.pop();
        hashableState = currentStateWithHistory.getHashableState()

        # Only do work here if we have not processed this state
        if (not hashableState in l):
            l.add(hashableState);

            currentStateCoordinates = currentStateWithHistory.getLastCoordinates();
            if (problem.isGoalState(currentStateCoordinates)):
                return currentStateWithHistory.getMovementHistory();
            # Put successors in the data structure
            successors = problem.getSuccessors(currentStateCoordinates);
            for successor in successors:
                successorStateWithHistory = GetStateWithHistoryFromState(currentStateWithHistory, successor);
                if (not withCosts):
                    dataStructure.push(successorStateWithHistory);
                else:
                    dataStructure.push(successorStateWithHistory, successorStateWithHistory.getAccumulatedCost() + heuristic(successorStateWithHistory.getLastCoordinates(), problem));

    # Should never get here unless there is no solution!
    return [];


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    """
    return SolveUsingDataStructure(problem, util.Stack(), False);

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return SolveUsingDataStructure(problem, util.Queue(), False);

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return SolveUsingDataStructure(problem, util.PriorityQueue(), True)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return SolveUsingDataStructure(problem, util.PriorityQueue(), True, heuristic);


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
