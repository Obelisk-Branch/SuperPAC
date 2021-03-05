import random
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
    secondAgent = OffenseAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class ExpectimaxAgent(CaptureAgent):

    

# Inherits from ExpectimaxAgent
class DefenseAgent(ExpectimaxAgent):

    def getActionValue(self, action):
        value = 0
        gameState = self.getCurrentObservation()
        selfPos = gameState.getAgentPosition(self.agentIndex)
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



# Inherits from ExpectimaxAgent

class OffenseAgent(ExpectimaxAgent):

    def __init__(self, index, timeForComputing=0.1):
        super().__init__(index)
        self.agentIndex = index
        self.eFood = None
        self.eFoodPercent = 0
        self.totalFoodStart = 0
        self.powerTimeLeft = 0
        self.nextAction = None

    def chooseAction(self, gameState):
        # Loop through legal actions to find the one with the best value
        actions = gameState.getLegalActions(self.agentIndex)
        bestValue = float('-inf')
        bestAction = Directions.STOP
        for action in actions:
            value = self.getActionValue(action)
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

    def getClosestEnemy(agent, agentIndex):
        gameState = CaptureAgent.getCurrentObservation(agent)
        enemiesList = CaptureAgent.getOpponents(gameState)
        selfPos = gameState.getAgentPosition(agentIndex)

    def getClosestEnemy(self):
        gameState = self.getCurrentObservation()
        enemiesList = self.getOpponents(gameState)
        selfPos = gameState.getAgentPosition(self.agentIndex)

        distance = 9999999999
        closestEnemy = None
        #Check distance between given agent and every enemy, return closest enemy index and distance
        for enemy in enemiesList:
            enemyPos = gameState.getAgentPosition(enemy)
            distanceBetween = self.getMazeDistance(selfPos, enemyPos)
            if distanceBetween < distance:
                distance = distanceBetween
                closestEnemy = enemy
        return closestEnemy

        #set amount of enemy food on the board at beginning of game
    def setEFoodRemaining(self, gameState):
        if self.eFood is None:
            self.totalFoodStart = gameState.getNumFood()
            self.eFood = (gameState.getNumFood()) / 2
            #Agents should update self.eFood every time they eat a pellet
        return
        
    def eFoodQuery(self, gameState):
        if self.eFood is not None:
            self.eFoodQuery = self.eFood / (self.totalFoodStart / 2)
        return self.eFoodQuery

    def scaredEnemyQuery(self, gameState):
        if self.powerTimeLeft == 0:
            return False
        '''
        This is pseudocode because we don't have the route mechanism fleshed out yet
=======
# Inherits from ExpectimaxAgent
class DefenseAgent(ExpectimaxAgent):

    def getActionValue(self, action):
        value = 0
        gameState = self.getCurrentObservation()
        selfPos = gameState.getAgentPosition(self.agentIndex)
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

        #This gets the time it would take for pacman to reach the scared ghost
        routeTime = getRoute(scaredEnemy)

        #If pacman can reach the scared ghost before it becomes brave, chase it 
        if routeTime <= self.powerTimeLeft:
            return Route

        #If pacman can't reach the ghost, plan a route for the food far away from the ghost
        if routeTime > self.powerTimeLeft:
            return "Can't Reach Ghost"
        return False
        '''
    def getPolicy(self, gameState):

    def goToClosestFood(self, gameState):
        agentPos = gameState.getAgentPosition(self.agentIndex)
        actions = gameState.getLegalActions(self.agentIndex)

        distanceToFood = []
        enemyFood = gameState.getFood()

        return




    def chooseAction(self, gameState):
        setEFoodRemaining(gameState)

        eFood = eFoodQuery(gameState) 

        if (eFood <= (self.totalFoodStart / 2) / 3):
            #Switch to Defense somehow
        else:
            pacmanLocation = pacLocationQuery

        if pacmanLocation == 'HOME':

            # Go to closest enemy dot

        if pacmanLocation == 'ENEMY':

            #if enemy ghosts are scared


        #This is placeholder code that chooses a random action until chooseAction is finished
        actions = gameState.getLegalActions(self.agentIndex)
        bestValue = float('-inf')
        bestAction = Directions.STOP
        for action in actions:
            value = self.getActionValue(action)
            if (value > bestValue):
                bestValue = value
                bestAction = action
        return bestAction

            


    def pacLocationQuery(self, gameState):
        pacPos = gameState.getAgentPosition(self.agentIndex)
        x, y = pacPos

        #not sure if this works, supposed to check whether pac is on enemy side or home side
        if (x < 0):
            return 'ENEMY'
        else:
            return 'HOME'
        return




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

