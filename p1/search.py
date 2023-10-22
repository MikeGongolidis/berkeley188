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
    "*** YOUR CODE HERE ***"

   #INITIALISE THE SEARCH TREE USING THE INITIAL STATE OF THE PROBLEM
    # TREE = util.Stack()
    # TREE.push(problem.getStartState())
    # actions = []
    # not_chosen = []
    # # print("Start:", problem.getStartState())
    
    # tree_dict = {}
    
    # #LOOP DO
    # # print("While not the goal state ", problem.isGoalState(TREE.list[-1]))
    # while not problem.isGoalState(TREE.list[-1]):
        
    #     #CHECK FOR CANDIDATE EXPANSION


    #     # print("Get's fridnge:", problem.getSuccessors(TREE.list[-1]))

    #     #IF THEY EXIST, PICK ONE BASED ON STRATEGY
        
    #     potential_successors = [ s for s in problem.getSuccessors(TREE.list[-1]) if s[0] not in TREE.list]
    #     # print("Potential successors, not visited states:", potential_successors)
        
    #     if len(potential_successors) > 0:
    #         leftmost_state = potential_successors[0]
    #         tree_dict[leftmost_state[0]] = {"move": leftmost_state[1],"parent":TREE.list[-1]}
    #         for not_gonna_chose in potential_successors[1:]:
    #             if not_gonna_chose not in TREE.list:
    #                 not_chosen.append(not_gonna_chose[0])
    #                 tree_dict[not_gonna_chose[0]] = {"move": not_gonna_chose[1],"parent":TREE.list[-1]}
    #         TREE.push(leftmost_state[0])
    #     else:
    #         print("Chosing another path:",not_chosen)
    #         if len(not_chosen)>0:
    #             TREE.push(not_chosen[0])
    #             not_chosen.pop(0)
    #         else:
    #             break
    #     # print(f"Action length: {len(actions)}")
    #     # print(f"Actions: {actions}")
    #     # print(f"Position length: {len(TREE.list)}")
    #     # print(f"position: {TREE.list}")
    
    # # print(tree_dict)
    
    # node = TREE.list[-1]
    # # print(node)
    # while not node == problem.getStartState():
    #     actions.append(tree_dict[node]['move'])
    #     # print(node, actions)
    #     node = tree_dict[node]['parent']
    
    # actions.reverse()
    
    visited = []
    search_next = util.Stack()
    path = {}

    search_next.push(problem.getStartState())
    
    while True:
        node = search_next.pop()
        visited.append(node)
        if problem.isGoalState(node):
            break
        
        neighbours = problem.getSuccessors(node)
        if neighbours:
            for n in neighbours:
                pos, direction, _ = n
                if pos not in visited:
                    search_next.push(pos)
                    path[pos] = (node,direction)
    
    actions = []
    while True:
        try:
            parent, direction = path[node]
        except KeyError:
            break
        
        actions.append(direction)
        node = parent
    
    actions.reverse()
    return actions
    
    ## RECURSION

    # def visit(state, visited):
        
    #     if problem.isGoalState(state):
    #         return [],True

    #     visited.append(state)
    #     for neighbour in problem.getSuccessors(state):
    #         position, direction, _ = neighbour
    #         if position not in visited:
    #             directions, goal_reached = visit(position,visited)
    #             if goal_reached:
    #                 directions.append(direction)
    #                 return directions, True
                
    #     return [], False
        
    # directions,_ = visit(problem.getStartState(),[])
    # directions.reverse()
    # print(directions)
    return directions



def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    visited = []
    search_next = util.Queue()
    path = {}

    search_next.push(problem.getStartState())
    
    while True:
        node = search_next.pop()
        visited.append(node)
        if problem.isGoalState(node):
            break
        
        neighbours = problem.getSuccessors(node)
        if neighbours:
            for n in neighbours:
                pos, direction, _ = n
                if pos not in visited and pos not in search_next.list:
                    search_next.push(pos)
                    path[pos] = (node,direction)
    
    actions = []
    while True:
        try:
            parent, direction = path[node]
        except KeyError:
            break
        
        actions.append(direction)
        node = parent
    
    actions.reverse()
    return actions


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited = []
    search_next = util.PriorityQueue()
    path = {}
    search_next.push(problem.getStartState(),0)
    
    while True:
        current_priority, node = search_next.pop()
        visited.append(node)
        
        if problem.isGoalState(node):
            break
        
        neighbours = problem.getSuccessors(node)
        if neighbours:
            for n in neighbours:
                pos, direction, priority = n
                if pos not in visited:
                    cumulative_priority = current_priority + priority
                    search_next.update(pos,cumulative_priority)
                    if pos not in path or path[pos][2] > cumulative_priority:
                        path[pos] = (node,direction,cumulative_priority)
    
    actions = []
    while True:
        try:
            parent, direction,_ = path[node]
        except KeyError:
            break
        
        actions.append(direction)
        node = parent
    
    actions.reverse()
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    search_next = util.PriorityQueue()
    path = {}
    search_next.push(problem.getStartState(),0)
    
    while True:
        current_priority, node = search_next.pop()
        visited.append(node)
        
        if problem.isGoalState(node):
            break
        
        neighbours = problem.getSuccessors(node)
        if neighbours:
            for n in neighbours:
                pos, direction, priority = n
                if pos not in visited:
                    f = current_priority + priority + heuristic(pos,problem) - heuristic(node,problem)
                    search_next.update(pos,f)
                    if pos not in path or path[pos][2] > f:
                        path[pos] = (node,direction,f)
    
    actions = []
    while True:
        try:
            parent, direction,_ = path[node]
        except KeyError:
            break
        
        actions.append(direction)
        node = parent
    
    actions.reverse()
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
