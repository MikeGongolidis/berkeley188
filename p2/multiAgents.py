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
import math 
import search
import searchAgents

import numpy as np

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    foodWeights = [3,2,1]

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

        score = successorGameState.getScore() 
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0:
                ghostPosx,ghostPosy = ghost.getPosition()
                dist = searchAgents.mazeDistance(newPos,(int(ghostPosx),int(ghostPosy)),successorGameState)
                if dist < 4:
                    score = score - dist*10
            else:
                # ghostPosx,ghostPosy = ghost.getPosition()
                # dist = searchAgents.mazeDistance(newPos,(int(ghostPosx),int(ghostPosy)),successorGameState)
                # score = score + dist
                pass

        if len(newFood.asList()) > 0:
            
            dist_from_food = [searchAgents.mazeDistance(newPos,food,successorGameState) for food in newFood.asList()]
            dist_from_food.sort()
            food_len = min(len(dist_from_food),3)
            avg_dist_food = np.average(dist_from_food[:food_len],weights=self.foodWeights[:food_len])
            score = score - avg_dist_food

        return score

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
        "*** YOUR CODE HERE ***"
        
        def value(state, current_depth, current_agent):
            
            if state.isWin() or state.isLose() or current_depth == self.depth:
                return self.evaluationFunction(state) , ''
            
            if current_agent == self.index:
                return max_value(state, current_depth, current_agent)
            else:
                return min_value(state, current_depth, current_agent)
            
        
        def min_value(state, current_depth, current_agent):
            next_agent = (current_agent + 1) % self.total_agents
            next_depth = current_depth
            if next_agent < current_agent:
                next_depth  = current_depth + 1
            available_actions = state.getLegalActions(agentIndex=current_agent)


            v = 1000000
            for next_state,action in [(state.generateSuccessor(current_agent, action),action) for action in available_actions]:
                temp_val , _ = value(next_state, next_depth, next_agent)
                if v > temp_val:
                    v = temp_val
                    best_action = action
            return v,best_action
        
        def max_value(state, current_depth, current_agent):
            next_agent = (current_agent + 1) % self.total_agents
            next_depth = current_depth
            if next_agent < current_agent:
                next_depth  = current_depth + 1
            available_actions = state.getLegalActions(agentIndex=current_agent)

            v = -1000000
            for next_state,action in [(state.generateSuccessor(current_agent, action),action) for action in available_actions]:
                temp_val, _ = value(next_state, next_depth, next_agent)
                if v < temp_val:
                    v = temp_val
                    best_action = action 
            return v,best_action
        
        self.total_agents = gameState.getNumAgents()

        value,action = value(gameState,0,0)
        print(value,action)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def value(state, current_depth, current_agent, a, b):
            print('value',a,b)
            if state.isWin() or state.isLose() or current_depth == self.depth:
                return self.evaluationFunction(state) , ''
            
            if current_agent == self.index:
                return max_value(state, current_depth, current_agent, a, b)
            else:
                return min_value(state, current_depth, current_agent, a, b)
            
        
        def min_value(state, current_depth, current_agent, a, b):
            print('min',a,b)
            next_agent = (current_agent + 1) % self.total_agents
            next_depth = current_depth
            if next_agent < current_agent:
                next_depth  = current_depth + 1
            available_actions = state.getLegalActions(agentIndex=current_agent)


            v = 1000000
            for next_state,action in [(state.generateSuccessor(current_agent, action),action) for action in available_actions]:
                temp_val , _ = value(next_state, next_depth, next_agent, a, b)
                if v > temp_val:
                    v = temp_val
                b = min(b, v)
                if v < a: 
                    return v
            return v
        
        def max_value(state, current_depth, current_agent, a, b):
            print('max',a,b)
            next_agent = (current_agent + 1) % self.total_agents
            next_depth = current_depth
            if next_agent < current_agent:
                next_depth  = current_depth + 1
            available_actions = state.getLegalActions(agentIndex=current_agent)

            v = -1000000
            for next_state,action in [(state.generateSuccessor(current_agent, action),action) for action in available_actions]:
                temp_val = value(next_state, next_depth, next_agent, a, b)
                if v < temp_val:
                    v = temp_val
                    best_action = action 
                a = max(a, v)
                if v > b: 
                    return v, best_action
            return v,best_action
        
        self.total_agents = gameState.getNumAgents()
        value,action = value(gameState,0,0,-10,10)
        print(value,action)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


