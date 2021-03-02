import random
from pacai.util import reflection
from pacai.agents.capture.capture import CaptureAgent
from pacai.core.directions import Directions

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.student.myTeam.[DefenseAgent]',
        second = 'pacai.student.myTeam.[OffenseAgent]'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = DefenseAgent
    secondAgent = OffenseAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class ExpectimaxAgent(CaptureAgent):

    def __init__(self, index, timeForComputing=0.1):
        super().__init__(index)
        self.agentIndex = index

    def chooseAction(self, gameState):
        return random.choice(gameState.getLegalActions(self.agentIndex))

    def getClosestEnemy(agent, agentIndex):
        gameState = CaptureAgent.getCurrentObservation(agent)
        enemiesList = CaptureAgent.getOpponents(gameState)
        selfPos = gameState.getAgentPosition(agentIndex)

        distance = 9999999999
        closestEnemy = None
        #Check distance between given agent and every enemy, return closest enemy index and distance
        for enemies in enemiesList:
            enemyPos = gameState.getAgentPosition(enemies)
            distanceBetween = CaptureAgent.getMazeDistance(selfPos, enemy)
            if distanceBetween < distance:
                distance = distanceBetween
                closestEnemy = enemy
        return {closestEnemy, enemyPos}


# Inherits from ExpectimaxAgent
class DefenseAgent(ExpectimaxAgent):
    pass


# Inherits from ExpectimaxAgent
class OffenseAgent(ExpectimaxAgent):
    pass

#THIS IS CAMERON'S SALVAGED p2 CODE FOR EXPECTIMAX
'''
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:

    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """
    def getAction(self, state):

        def maxValue(state, agent, depth):
            agent = 0
            legalMaxActions = state.getLegalActions(agent)

            if state._gameover is True or depth >= self.depth or len(legalMaxActions) == 0:
                return self.getEvaluationFunction()(state)
            v = float('-inf')
            v = v + 1
            maxVal = max(expValue(state.generateSuccessor(agent, actions),
             agent + 1, depth + 1) for actions in legalMaxActions)
            return maxVal

        #  Function to give expected value
        def expValue(state, agent, depth):
            legalExpActions = state.getLegalActions(agent)
            lenActions = len(legalActions)

            ev = 0
            if lenActions != 0:
                prob = 1 / lenActions
            if lenActions == 0 or state._gameover is True or depth >= self.depth:
                return self.getEvaluationFunction()(state)
            for actions in legalExpActions:

                successor = state.generateSuccessor(agent, actions)
                if agent != state.getNumAgents() - 1:
                    expVal = expValue(successor, agent + 1, depth)
                else:
                    expVal = maxValue(successor, agent, depth)
                ev += (prob * expVal)
            return ev

        legalActions = state.getLegalActions(0)
        actionsDict = {}
        for actions in legalActions:
            agentInd = 1
            gameState = state.generateSuccessor(0, actions)
            actionsDict[actions] = expValue(gameState, agentInd, 1)

        return max(actionsDict, key = actionsDict.get)
'''
