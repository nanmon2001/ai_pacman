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

"""
Author: Mon-Nan How
A Node that keep track of the path in a graph.
"""
class Node:
    def __init__(self, state, path = [], priority = 0):
        self.state = state
        self.path = path
        self.priority = priority

def depthFirstSearch(problem):
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
    "*** YOUR CODE HERE ***"
    """
    Author: Mon-Nan How
    DFS practice, class project (CSCE 580 AI, University of South Carolina)
    """
    from util import Stack
    fringe = Stack()
    #Keep tract of the nodes that have been visited
    visited = []
    #Initialize the start node and fringe
    nodePointer = Node(problem.getStartState(), [])
    fringe.push(nodePointer)    
    #Keep track of the fringe till there is no undiscovered node
    while fringe.isEmpty() == False:

        nodePointer = fringe.pop()
        #Check if the state of the current visit node is goal
        if problem.isGoalState(nodePointer.state):
            #If reach the goal state then return the path
            return nodePointer.path
        if nodePointer.state not in visited:
            #If the state hasn't been visited, start expanding from this state
            SucTupList = problem.getSuccessors(nodePointer.state)
            for x,y,z in SucTupList:
                #If the successor's state hasn't visited before push the node on the fringe
                if x not in visited:
                    #Create a Node for every unvisited state
                    sucNodePath = list(nodePointer.path)
                    sucNodePath.append(y)
                    sucNode = Node(x, sucNodePath)
                    fringe.push(sucNode)
        visited.append(nodePointer.state)
    return "No solution found by DFS!"   

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """
    Author: Mon-Nan How
    BFS practice, class project (CSCE 580 AI, University of South Carolina)
    """
    #Fringe keep track the next expanding option
    from util import Queue
    fringe = Queue()
    #Keep tract of the nodes that have been visited
    visited = []
    #Initialize the start node and fringe
    nodePointer = Node(problem.getStartState(), [])
    fringe.push(nodePointer)    
    #Keep track of the fringe till there is no undiscovered node
    while fringe.isEmpty() == False:
        nodePointer = fringe.pop()
        if problem.isGoalState(nodePointer.state):
            #If reach the goal state then return the path
            return nodePointer.path
        if nodePointer.state not in visited:
            #If the state hasn't been visited, start expanding from this state
            SucTupList = problem.getSuccessors(nodePointer.state)
            for x,y,z in SucTupList:
                #If the successor's state hasn't visited before push the node on the fringe
                if x not in visited:
                    #Create a Node for every unvisited state
                    sucNodePath = list(nodePointer.path)
                    sucNodePath.append(y)
                    sucNode = Node(x, sucNodePath)
                    fringe.push(sucNode)
        visited.append(nodePointer.state)
    return "No solution found by BFS!"    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
    Author: Mon-Nan How
    UCS practice class project (CSCE 580 AI, University of South Carolina)
    """
    #Fringe keep track the next expanding option
    from util import PriorityQueue
    fringe = PriorityQueue()
    #Keep tract of the state that have been visited
    visited = []
    #Initialize the start node and fringe
    nodePointer = Node(problem.getStartState(), [], 0)
    fringe.push(nodePointer, 0)
    #Keep track of the fringe till there is no undiscovered node
    while fringe.isEmpty() == False:
        nodePointer = fringe.pop()
        #Check if the state of the current visit node is goal
        if problem.isGoalState(nodePointer.state):
            #If reach the goal state then return the path
            return nodePointer.path
        if nodePointer.state not in visited:
            #If the state hasn't been visited, start expanding from this state
            SucTupList = problem.getSuccessors(nodePointer.state)
            for x,y,z in SucTupList:
                #If the successor's state hasn't visited before push the node on the fringe
                if x not in visited:
                    #Create a Node for every unvisited state
                    sucNodePath = list(nodePointer.path)
                    sucNodePath.append(y)
                    sucNodePriority = int(nodePointer.priority) + z
                    sucNode = Node(x, sucNodePath, sucNodePriority)
                    fringe.push(sucNode,sucNodePriority)
        visited.append(nodePointer.state)
    return "No solution found by UCS!"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    Author: Mon-Nan How
    UCS practice class project (CSCE 580 AI, University of South Carolina)
    """
    #Fringe keep track the next expanding option
    from util import PriorityQueue
    fringe = PriorityQueue()
    #Keep tract of the state that have been visited
    visited = []
    #Initialize the start node and fringe
    nodePointer = Node(problem.getStartState(), [], 0)
    fringe.push(nodePointer, 0)
    #Keep track of the fringe till there is no undiscovered node
    while fringe.isEmpty() == False:
        nodePointer = fringe.pop()
        #Check if the state of the current visit node is goal
        if problem.isGoalState(nodePointer.state):
            #If reach the goal state then return the path
            return nodePointer.path
        if nodePointer.state not in visited:
            #If the state hasn't been visited, start expanding from this state
            SucTupList = problem.getSuccessors(nodePointer.state)
            for x,y,z in SucTupList:
                #If the successor's state hasn't visited before push the node on the fringe
                if x not in visited:
                    #Create a Node for every unvisited state
                    sucNodePath = list(nodePointer.path)
                    sucNodePath.append(y)
                    sucNodePriority = int(nodePointer.priority) + z
                    sucNode = Node(x, sucNodePath, sucNodePriority)
                    fringe.push(sucNode,sucNodePriority + heuristic(x, problem))
        visited.append(nodePointer.state)
    return "No solution found by ASTAR!"

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
