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
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        if successorGameState.isWin(): # If the successor state is a win state:
            return 10000
    
        for ghost in newGhostStates: # Check if the successor state collides with a ghost.
            if newPos == ghost.getPosition():
                return -10000

        foods = []
        for food in newFood.asList(): # Get the distance from all the foods.
            foods.append(manhattanDistance(newPos, food))

        foodScore = 1 / min(foods) # The smaller the minimum food distance, the larger the "foodScore".

        return successorGameState.getScore() + foodScore

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        def maximizer(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            value = -10000

            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, minimizer(successor, depth, 1))

            return value
        
        def minimizer(state, depth, agent):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            value = 10000

            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)

                if agent == (gameState.getNumAgents() - 1):
                    value = min(value, maximizer(successor, depth+1))
                else:
                    value = min(value, minimizer(successor, depth, agent+1))

            return value

        score = -10000
        move = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            newScore = minimizer(successor, 0, 1)

            if score < newScore:
                score = newScore
                move = action

        return move

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        def maximizer(state, depth, a, b):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            value = -10000

            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, minimizer(successor, depth, 1, a, b))

                if value > b:
                    return value
                a = max(a, value)

            return value
        
        def minimizer(state, depth, agent, a, b):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            value = 10000

            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)

                if agent == (gameState.getNumAgents() - 1):
                    value = min(value, maximizer(successor, depth+1, a, b))
                else:
                    value = min(value, minimizer(successor, depth, agent+1, a , b))

                if value < a:
                    return value
                b = min(b, value)

            return value

        score = -10000
        a = -10000
        b = 10000
        move = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            newScore = minimizer(successor, 0, 1, a, b)

            if score < newScore:
                score = newScore
                move = action
            
            if newScore > b:
                return move
            a = max(a, newScore)

        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their legal moves.
        """
        def maximizer(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            value = -10000

            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, expectimax(successor, depth, 1))

            return value
        
        def expectimax(state, depth, agent):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            value = 10000
            counter = 0
            total = 0

            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)

                if agent == (gameState.getNumAgents() - 1):
                    value = maximizer(successor, depth+1)
                else:
                    value = expectimax(successor, depth, agent+1)

                counter += 1
                total += value

            if counter == 0:
                return 0
            return total/counter
            

        score = -10000
        move = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            newScore = expectimax(successor, 0, 1)

            if score < newScore:
                score = newScore
                move = action

        return move

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
    1. If the closest ghost is scared, the overall score increases to encourage pacman to chase it.
    2. If the closest ghost is not scared, the overall score decreases to encourage pacman to get away from it.
    3. The smaller the minimum food distance, the larger the overall score.
    4. The smaller the minimum capsule distance, the larger the overall score.

    """

    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentGhostStates = currentGameState.getGhostStates()
    currentCapsule = currentGameState.getCapsules()

    score = 0    

    if currentGameState.isWin():
        return 10000
    

    ghosts = manhattanDistance(currentPos, currentGhostStates[0].getPosition())

    for ghost in currentGhostStates: 
        if currentPos == ghost.getPosition() and ghost.scaredTimer == 0: # Check if the current state collides with a ghost.
            return -10000
              
        if manhattanDistance(currentPos, ghost.getPosition()) <= ghosts: # Find the closest ghost.
            ghosts = manhattanDistance(currentPos, ghost.getPosition())
            if ghost.scaredTimer > 0: # Check if the closest ghost is currently scared.
                scared = True
            else:
                scared = False

    # If the closest ghost is scared, the overall score increases, otherwise it decreases.   
    if scared: 
        score += 1 / ghosts
    else:
        score -= 1 / ghosts


    foods = []
    for food in currentFood.asList(): # Get the distance from all the foods.
        foods.append(manhattanDistance(currentPos, food))

    score += 1 / min(foods) # The smaller the minimum food distance, the larger the overall score.


    capsules = []
    for capsule in currentCapsule: # Get the distance from all the capsules.
        capsules.append(manhattanDistance(currentPos, capsule))

    if len(capsules) > 0:
        score += 1 / min(capsules) # The smaller the minimum capsule distance, the larger the overall score.


    return currentGameState.getScore() + score
 
# Abbreviation
better = betterEvaluationFunction
