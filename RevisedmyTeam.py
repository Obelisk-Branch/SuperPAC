import abc
from pacai.util import util
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


class ReflexAgent(CaptureAgent):

    def __init__(self, index, timeForComputing=0.1):
        super().__init__(index)
        self.agentIndex = index
        self.CapsuleTime = 0
        self.lastCapsuleEaten = None
        self.capsuleSelfPos = None

    # Returns the best action to take based on the game state
    def chooseAction(self, gameState):
        # Loop through legal actions to find the one with the best value
        actions = gameState.getLegalActions(self.agentIndex)
        bestValue = float('-inf')
        bestAction = Directions.STOP
        for action in actions:
            value = self.getActionValue(action)
            if value > bestValue:
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
        if pos != util.nearestPoint(pos):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.agentIndex, action)
        else:
            return successor

    # Deriving classes must override this to calculate the value of an action
    @abc.abstractmethod
    def getActionValue(self, action):
        return 0

    # Returns the closest enemy
    def getClosestEnemy(self):
        gameState = self.getCurrentObservation()
        enemiesList = self.getOpponents(gameState)
        selfPos = gameState.getAgentPosition(self.agentIndex)

        # Loop through enemies to find the closest one based on maze distance
        distance = float("inf")
        closestEnemy = None
        for enemy in enemiesList:
            enemyPos = gameState.getAgentPosition(enemy)
            distanceBetween = self.getMazeDistance(selfPos, enemyPos)
            if distanceBetween < distance:
                distance = distanceBetween
                closestEnemy = enemy
        return closestEnemy

    # Returns the enemy deepest into our side
    def getDeepestEnemy(self):
        gameState = self.getCurrentObservation()
        enemiesList = self.getOpponents(gameState)

        # Loop through enemies to find the one with the greatest or least x-position based on team
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

    # Return the value of the action if taken
    def getActionValue(self, action):
        value = 0
        gameState = self.getCurrentObservation()
        nextPos = self.getSuccessor(gameState, action).getAgentState(self.agentIndex).getPosition()
        # Prevent moving to other team's side by devaluing positions on their side
        if self.red:
            if nextPos[0] >= gameState.getWalls().getWidth() / 2:
                return -1
        elif nextPos[0] < gameState.getWalls().getWidth() / 2:
            return -1

        # Get maze distance to the deepest enemy
        enemyPos = gameState.getAgentPosition(self.getDeepestEnemy())
        enemyDist = self.getMazeDistance(nextPos, enemyPos)
        # If the enemy is close, chase them
        if enemyDist < 5:
            if enemyDist > 0:
                value = 1.0 / enemyDist
            else:
                value = 2
        else:  # Otherwise defend food that is closest to deepest enemy
            # Put food and capsules in same list to defend
            defendingFood = self.getFoodYouAreDefending(gameState).asList()
            defendingFood += self.getCapsulesYouAreDefending(gameState)
            closeFood = None
            closeFoodDist = float('inf')
            # Find the food closest to the enemy
            for food in defendingFood:
                dist = self.getMazeDistance(food, enemyPos)
                if dist < closeFoodDist:
                    closeFoodDist = dist
                    closeFood = food

            # Move toward food closest to enemy
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
        
        gameState = self.getCurrentObservation()
        if(self.getScore(gameState) > 2):
            value = 0
            nextPos = self.getSuccessor(gameState, action).getAgentState(self.agentIndex).getPosition()
            # Prevent moving to other team's side by devaluing positions on their side
            if self.red:
                if nextPos[0] >= gameState.getWalls().getWidth() / 2:
                    return -1
            elif nextPos[0] < gameState.getWalls().getWidth() / 2:
                return -1

        
            # Get maze distance to the enemy not targeted by defense agent
            takenEnemy = self.getDeepestEnemy()
            EnemiesList = self.getOpponents(gameState)
            for enemy in EnemiesList:
                if enemy != takenEnemy:
                    enemyPos = gameState.getAgentPosition(enemy)
            enemyDist = self.getMazeDistance(nextPos, enemyPos)
            # If the enemy is close, chase them
            if enemyDist < 5:
                if enemyDist > 0:
                    value = 1.0 / enemyDist
                else:
                    value = 2
            else:  # Otherwise defend food that is closest to deepest enemy
                # Put food and capsules in same list to defend
                defendingFood = self.getFoodYouAreDefending(gameState).asList()
                defendingFood += self.getCapsulesYouAreDefending(gameState)
                closeFood = None
                closeFoodDist = float('inf')
                # Find the food closest to the enemy
                for food in defendingFood:
                    dist = self.getMazeDistance(food, enemyPos)
                    if dist < closeFoodDist:
                        closeFoodDist = dist
                        closeFood = food

                # Move toward food closest to enemy
                if closeFood is not None:
                    dist = self.getMazeDistance(nextPos, closeFood)
                    if dist > 0:
                        value = 1.0 / dist
                    else:
                        value = 2
            return value

        else:
            value = 0
            selfPosition = gameState.getAgentPosition(self.agentIndex)
            if selfPosition is not self.capsuleSelfPos:
                if self.CapsuleTime > 0:
                    self.CapsuleTime -= 1
                self.capsuleSelfPos = selfPosition
            successor = self.getSuccessor(gameState, action)
            nextPos = self.getSuccessor(gameState, action).getAgentState(self.agentIndex).getPosition()
            enemyPos = gameState.getAgentPosition(self.getClosestEnemy())
            enemyDist = self.getMazeDistance(nextPos, enemyPos)
            lastCapsule = self.lastCapsuleEaten
            '''
            #If you're on the enemy side, don't move back over to your side
            if self.red:
                if selfPosition[0] >= gameState.getWalls().getWidth() / 2 and nextPos[0] < gameState.getWalls().getWidth() / 2:
                    return -1
            elif not self.red and selfPosition[0] <= gameState.getWalls().getWidth() / 2 and nextPos[0] > gameState.getWalls().getWidth() / 2:
                    return -1
            '''
            if lastCapsule is not None:
                if self.lastCapsuleEaten is None:
                    self.lastCapsuleEaten = lastCapsule
                    self.CapsuleTime = 40
                if self.lastCapsuleEaten is not None and self.lastCapsuleEaten is not lastCapsule:
                    self.CapsuleTime = 40

            #If you're getting chased by a ghost, run
            if enemyDist < 5:
                if enemyDist > 0:
                    value = -(1.0 / enemyDist)
                else:
                    value = -5
                
            if enemyDist < 5 and self.CapsuleTime > 0 and self.CapsuleTime is not None:
                if enemyDist > 0:
                    value = 5.0 / enemyDist
                else:
                    value = 7
                
            #otherwise, go after the nearest food
            else:
                attackingFood = self.getFood(gameState).asList()
                attackingFood += self.getCapsules(gameState)
                closeFood = None
                closeFoodDist = float('inf')
                for food in attackingFood:
                    dist = self.getMazeDistance(nextPos, food)
                    if dist < closeFoodDist:
                        closeFoodDist = dist
                        closeFood = food

                    '''
                for capsules in self.getCapsules(gameState):
                    dist = self.getMazeDistance(capsules, enemy)
                    pacdist = self.getMazeDistance(capsules, nextPos)
                    if pacdist < dist:
                        value = 5.0/dist
                        return value
                    '''
                if closeFood is not None:
                    dist = self.getMazeDistance(nextPos, closeFood)
                    if dist > 0:
                        value = 1.0 / dist

                    else:
                        value = 2
            return value
