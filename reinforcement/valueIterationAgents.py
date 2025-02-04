# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections
import math

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()
        for _ in range(self.iterations):
            newValues = util.Counter()
            for state in allStates:
                #print('Looking at state:', state)
                possibleActions = self.mdp.getPossibleActions(state)
                #if not possibleActions:
                    #newValues[state] = self.values[state]
                if possibleActions:
                    maxValue = -math.inf
                    for action in possibleActions:
                        #print('State ', state, ' has action', action)
                        newVal = sum([prob*(self.mdp.getReward(state,action,nextState) + self.discount*self.values[nextState]) for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action)])
                        if newVal > maxValue:
                            #print('Changing max value for state ', state, ' with action ',action)
                            maxValue = newVal
                            #print('Max value is now for action/state',action,state,':',maxValue)
                    newValues[state] = maxValue
            self.values = newValues

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        return sum([prob*(self.mdp.getReward(state,action,nextState) + self.discount*self.values[nextState]) for nextState,prob in self.mdp.getTransitionStatesAndProbs(state,action)])
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possibleActions = self.mdp.getPossibleActions(state)
        if not possibleActions:
            return None
        else:
            maxValue = -math.inf
            bestAction = None
            for action in possibleActions:
                newValue = sum([prob*(self.mdp.getReward(state,action,nextState)+(self.discount*self.values[nextState])) for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action)])
                if newValue > maxValue:
                    maxValue = newValue
                    bestAction = action
            return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()
        numStates = len(allStates)
        for k in range(self.iterations):
            state = allStates[k % numStates]
            if self.mdp.isTerminal(state):
                continue
            else:
                possibleActions = self.mdp.getPossibleActions(state)
                if possibleActions:
                    maxValue = -math.inf
                    for action in possibleActions:
                        newValue = sum([prob*(self.mdp.getReward(state,action,nextState)+(self.discount*self.values[nextState])) for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action)])
                        if newValue > maxValue:
                            maxValue = newValue
                    self.values[state] = maxValue

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        possibleStates = self.mdp.getStates()
        updateStates = util.PriorityQueue()

        for state in possibleStates:
            predecessors[state] = set()

        for state in possibleStates:
            for action in self.mdp.getPossibleActions(state):
                nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState, _ in nextStates:
                    predecessors[nextState] = predecessors[nextState].union({state})

        for state in possibleStates:
            if self.mdp.isTerminal(state):
                continue
            maxValue = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
            #for action in self.mdp.getPossibleActions(state):
            #    newValue = self.getQValue(state,action)
            #    if newValue > maxValue:
            #        maxValue = newValue
            diff = abs(self.values[state] - maxValue)
            updateStates.push(state, -diff)

        for _ in range(self.iterations):
            if updateStates.isEmpty():
                break
            state = updateStates.pop()
            possibleActions = self.mdp.getPossibleActions(state)
            if possibleActions:
                maxValue = -math.inf
                for action in possibleActions:
                    newVal = sum(
                        [prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
                         for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action)])
                    if newVal > maxValue:
                        maxValue = newVal
                self.values[state] = maxValue
                for predState in predecessors[state]:
                    maxValue = max([self.getQValue(predState, action) for action in self.mdp.getPossibleActions(predState)])
                    #for action in self.mdp.getPossibleActions(state):
                    #    newValue = self.getQValue(state, action)
                    #    if newValue > maxValue:
                    #        maxValue = newValue
                    diff = abs(self.values[predState] - maxValue)
                    if diff > self.theta:
                        updateStates.update(predState, -diff)

