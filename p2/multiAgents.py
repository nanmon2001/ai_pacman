# multiAgents.py
# --------------
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


from util import manhattanDistance
from util import pause
from util import Stack
from game import Directions
import random, util


from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        Author: Mon-Nan How
        """
        #Initialize
        scorechange = 0
        scariness = 500 #This value determin how scary a ghost is.
        c_capsuleList = currentGameState.getCapsules()
        s_capsuleList = successorGameState.getCapsules()
        currentFoodList = currentGameState.getFood().asList() + c_capsuleList
        newFoodList = newFood.asList() + s_capsuleList
        #Encourage the pacman to finish the game.
        if len(newFood.asList()) == 0:
            successorGameState.data.score += 500
            return successorGameState.getScore()
        #A food is consumed after an action is taken, score + 10

        if len(currentFoodList) > len(newFoodList):
            scorechange += 10
        #A fucntion that takes a list of positions and return the boader of the list.
        #Here is I use this to calculate the minimun cost need to finish the game
        def findBoarder(itemList):
            smallest_x = 999999
            largest_x = 1
            smallest_y = 999999
            largest_y = 1
            for x,y in itemList:
                if x <= smallest_x: smallest_x = x
                if y <= smallest_y: smallest_y = y
                if x >= largest_x: largest_x = x
                if y >= largest_y: largest_y = y
            return (smallest_x, largest_x, smallest_y,largest_y )

        #The minium cost at leat needed to eat all the food
        costMin = 0;
        x_set = set()
        y_set = set()
        foodDistane = [] 
        for a,b in newFoodList:
            x_set.add(a)
            y_set.add(b)
            foodDistane.append(manhattanDistance(newPos,(a,b)))
        costMin += min(foodDistane)
        #The smallest manhattan distance need to travel between a group of food
        (smallest_x, largest_x, smallest_y, largest_y) = findBoarder(newFoodList)
        costMin += ((largest_x - smallest_x) + (largest_y - smallest_y))
        #The following guarantee there exists a imaginary rectangular from the manhattan distance path.
        if len(newFoodList) >= 3:
            if len(x_set) >= 3 & len(y_set) >= 3:
                costMin += 1 #At least one 1 step more need for a ideal path
        scorechange -= costMin

        #Consider ghost effect
        c_ghostList = currentGameState.getGhostPositions()
        s_ghostList = successorGameState.getGhostPositions()
        if len(s_ghostList) != 0:
            i = 0
            while i < len(newScaredTimes):
                tempDistance = manhattanDistance(newPos,s_ghostList[i])
                if newScaredTimes[i] > 0 and newScaredTimes[i]>tempDistance*2:
                    scorechange += 200 - (tempDistance*2)

                else:
                    # If the ghost caught the pacman then the game is over.
                    for ghostPos in successorGameState.getGhostPositions():
                        closeToDeath = manhattanDistance(newPos,ghostPos)
                        if (closeToDeath < 2):
                                scorechange -= scariness   
                i+=1
        #Did not consider wall effect, thus put some random value to break tie consition.
        scorechange += random.choice([1,-1,0])
        return scorechange
        
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)

    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        """
        Author: Mon-Nan How
        """
        def get_val(state, num):
            i = num
            index = i%agentNum
            retVal = 0.001
            if (state.isWin() == True or state.isLose() == True):
                return self.evaluationFunction(state)
            if (i >= treeLayer):
                return self.evaluationFunction(state)
            if index == 0:
                maxVal = -9999.001
                for act in state.getLegalActions(0):
                    tempState = state.generateSuccessor(0, act)
                    tempVal = get_val(tempState,i+1)
                    if tempVal > maxVal:
                        maxVal = tempVal
                retVal = maxVal
            else:
                miniVal = 9999.001
                for act in state.getLegalActions(index):
                    tempState = state.generateSuccessor(index, act)
                    tempVal = get_val(tempState,i+1)
                    if tempVal < miniVal:
                        miniVal = tempVal
                retVal = miniVal
            return retVal        
        agentNum = gameState.getNumAgents()
        depth = self.depth
        treeLayer = agentNum*depth
        maxVal = -9999.001
        action = "Stop"
        for act in gameState.getLegalActions(0):
            tempState1 = gameState.generateSuccessor(0, act)
            temp_value = get_val(tempState1,1)
            if temp_value > maxVal:
                maxVal = temp_value
                action = act
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """
        Author: Mon-Nan How
        """
        def value(state, num, maxVal, miniVal):
            index = num%agentNum
            if (state.isWin() == True or state.isLose() == True):
                return self.evaluationFunction(state)
            if (num >= treeLayer):
                return self.evaluationFunction(state)
            #Pacman index is 0, it maximize utility
            if index == 0:
                return max_value(state, num, maxVal, miniVal)
            #Gosht indexes are other than 0, they minimize utility
            else:
                return min_value(state, num, maxVal, miniVal)

        def max_value(state, num, maxVal, miniVal):
            index = num%agentNum
            v = -9999.99
            for act in state.getLegalActions(index):
                tempState = state.generateSuccessor(index, act)
                v = max(v, value(tempState, num+1, maxVal, miniVal))
                if v > miniVal:
                    return v
                maxVal = max(maxVal, v)
            return v

        def min_value(state, num, maxVal, miniVal):
            index = num%agentNum
            v = 9999.99
            for act in state.getLegalActions(index):
                tempState = state.generateSuccessor(index, act)
                v = min(v, value(tempState, num+1, maxVal, miniVal))
                if v < maxVal:
                    return v
                miniVal = min(miniVal, v)
            return v

        agentNum = gameState.getNumAgents()
        depth = self.depth
        treeLayer = agentNum*depth
        action = "Stop"
        maxVal = -9999.99
        for act in gameState.getLegalActions(0):
            tempState1 = gameState.generateSuccessor(0, act)
            temp_value = value(tempState1,1, maxVal, 9999.99)
            if temp_value >= maxVal:
                maxVal = temp_value
                action = act
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        """
        Author: Mon-Nan How
        """
        def value(state, num):
            index = num%agentNum
            if (state.isWin() == True or state.isLose() == True):
                return self.evaluationFunction(state)
            if (num >= treeLayer):
                return self.evaluationFunction(state)
            #Pacman index is 0, it maximize utility
            if index == 0:
                return max_value(state, num)
            #Gosht indexes are other than 0, they minimize utility
            else:
                return radom_value(state, num)

        def max_value(state, num):
            index = num%agentNum
            maxVal = -9999.99
            for act in state.getLegalActions(index):
                tempState = state.generateSuccessor(index, act)
                maxVal = max(maxVal,value(tempState, num+1))
            return maxVal
                
        def radom_value(state, num):
            index = num%agentNum
            randomValList = []
            for act in state.getLegalActions(index):
                tempState = state.generateSuccessor(index, act)
                randomValList.append(value(tempState, num+1))
            return sum(randomValList)/len(randomValList)

        agentNum = gameState.getNumAgents()
        depth = self.depth
        treeLayer = agentNum*depth
        action = "Stop"
        maxVal = -9999.99
        for act in gameState.getLegalActions(0):
            tempState1 = gameState.generateSuccessor(0, act)
            temp_value = value(tempState1,1)
            if temp_value >= maxVal:
                maxVal = temp_value
                action = act
        return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    """
    "*** YOUR CODE HERE ***"
    """
    Author: Mon-Nan How
    DESCRIPTION: 
    Evaluate the state by 
    1. Counting the remaining foods, less the food less the score taken off (capsule are also added).
    2. Try to drive the pacman to move even if that action (th successor state) doesn't consume a food, 
    by mearsuring the manhattan distance between the nearest food (the nearer the lesser score is taken off).
    3. Try to address the situation with a ghost around by considering the scary time and the distance,
    if the distance between the pacman and ghost is smaller than 3 and enough scary time, encourage the pacman to 
    beat the ghost.
    """
    #Initialization
    ghostStates = currentGameState.getGhostStates()
    ghostPosList = currentGameState.getGhostPositions()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    pacPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    capsuleList = currentGameState.getCapsules()
    eatList = foods + capsuleList
    score = 0
    scariness = 500
    #Encourage pacmac to eat every left food 
    score -= len(eatList)*10
    foodDistList = []
    if len(eatList) != 0:
    	for food in eatList:
    		tempDist = manhattanDistance(pacPos,food)
    		foodDistList.append(tempDist)
    if len(eatList) != 0:
        score -= min(foodDistList)

    #The follwing determines how to interact with a ghost. 
    #I only consider the effect of the ghosts when they exist and near the pacman.
    if len(ghostPosList) != 0:
        i = 0
        while i < len(ghostPosList):
            DistToGhost = manhattanDistance(pacPos,ghostPosList[0])
            if DistToGhost < 3:
                if scaredTimes[0] > DistToGhost+1:
                    score -= (DistToGhost*5)
                else:
                    if DistToGhost == 0:
                        score -= scariness
            i += 1
    return score

# Abbreviation
better = betterEvaluationFunction
