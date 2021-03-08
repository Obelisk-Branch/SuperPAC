# import random
import abc
from pacai.util import util
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
    secondAgent = reflection.qualifiedImport('pacai.agents.capture.offense.OffensiveReflexAgent')  # Replace with OffenseAgent when implemented

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class ReflexAgent(CaptureAgent):

    def __init__(self, index, timeForComputing=0.1):
        super().__init__(index)
        self.agentIndex = index

    def chooseAction(self, gameState):
        # Loop through legal actions to find the one with the best value
        actions = gameState.getLegalActions(self.agentIndex)
        bestValue = float('-inf')
        bestAction = Directions.STOP
        for action in actions:
            value = self.getActionValxue(action)
            if (value > bestValue):
                bestValue = value
                bestAction = action
        return bestAction

    # Copied from ReflexCaptureAgent
    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """

        successor = gameState.generateSuccessor(self.agentIndex, action)
        pos = successor.getAgentState(self.agentIndex).getPosition()
        if (pos != util.nearestPoint(pos)):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.agentIndex, action)
        else:
            return successor

    # Deriving classes must override this to calculate the value of an action
    @abc.abstractmethod
    def getActionValue(self, action):
        return 0

    def getClosestEnemy(self):
        gameState = self.getCurrentObservation()
        enemiesList = self.getOpponents(gameState)
        selfPos = gameState.getAgentPosition(self.agentIndex)

        distance = 9999999999
        closestEnemy = None
        for enemy in enemiesList:
            enemyPos = gameState.getAgentPosition(enemy)
            distanceBetween = self.getMazeDistance(selfPos, enemyPos)
            if distanceBetween < distance:
                distance = distanceBetween
                closestEnemy = enemy
        return closestEnemy

    def getDeepestEnemy(self):
        gameState = self.getCurrentObservation()
        enemiesList = self.getOpponents(gameState)

        depth = -1
        deepestEnemy = None
        for enemy in enemiesList:
            enemyPos = gameState.getAgentPosition(enemy)
            enemyDepth = enemyPos[0]
            if self.red:
                enemyDepth = gameState.getWalls().getWidth() - enemyDepth
            if enemyDepth > depth:
                depth = enemyDepth
                deepestEnemy = enemy
        return deepestEnemy


# Inherits from ReflexAgent
class DefenseAgent(ReflexAgent):

    def getActionValue(self, action):
        value = 0
        gameState = self.getCurrentObservation()
        # selfPos = gameState.getAgentPosition(self.agentIndex)
        nextPos = self.getSuccessor(gameState, action).getAgentState(self.agentIndex).getPosition()
        if self.red:
            if nextPos[0] >= gameState.getWalls().getWidth() / 2:
                return -1
        elif nextPos[0] < gameState.getWalls().getWidth() / 2:
            return -1

        enemyPos = gameState.getAgentPosition(self.getDeepestEnemy())
        enemyDist = self.getMazeDistance(nextPos, enemyPos)
        if enemyDist < 5:
            if enemyDist > 0:
                value = 1.0 / enemyDist
            else:
                value = 2
        else:
            defendingFood = self.getFoodYouAreDefending(gameState).asList()
            defendingFood += self.getCapsulesYouAreDefending(gameState)
            closeFood = None
            closeFoodDist = float('inf')
            for food in defendingFood:
                dist = self.getMazeDistance(food, enemyPos)
                if dist < closeFoodDist:
                    closeFoodDist = dist
                    closeFood = food

            if closeFood is not None:
                dist = self.getMazeDistance(nextPos, closeFood)
                if dist > 0:
                    value = 1.0 / dist
                else:
                    value = 2
        return value


# Inherits from ReflexAgent
class OffenseAgent(ReflexAgent):

    def getActionValue(self, action):
        value = 0
         gameState = self.getCurrentObservation()
        selfPosition = gameState.getAgentPosition(self.agentIndex)
        nextPos = self.getSuccessor(gameState, action).getAgentState(self.agentIndex).getPosition()
        if self.red:
            if nextPos[0] >= gameState.getWalls().getWidth() / 2:
                return -1
        elif nextPos[0] < gameState.getWalls().getWidth() / 2:
            return -1

        enemyPos = gameState.getAgentPosition(self.getClosestEnemy())
        enemyDist = self.getMazeDistance(nextPos, enemyPos)
        if enemyDist < 5:
            if enemyDist > 0:
                value = 1.0 / enemyDist
            else:
                value = 0
        else:
            attackingFood = self.getFood(gameState).asList()
            attackingFood += self.getCapsules(gameState)
            closeFood = None
            closeFoodDist = float('inf')
            for food in atackingFood:
                dist = self.getMazeDistance(food, enemyPos)
                if dist < closeFoodDist:
                    closeFoodDist = dist
                    closeFood = food

            if closeFood is not None:
                dist = self.getMazeDistance(nextPos, closeFood)
                if dist > 0:
                    value = 2.0 / dist
                else:
                    value = 2
        return value
