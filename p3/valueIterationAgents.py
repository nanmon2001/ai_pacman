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
import operator#for finding max value in a dictionary

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

        for i in range(self.iterations):
            temp = self.values.copy()
            for state in self.mdp.getStates():
                
                if self.mdp.isTerminal(state) == True: continue
                actions = self.mdp.getPossibleActions(state)
                temp[state] = max([self.getQValue(state, act) for act in actions])

            self.values = temp


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
        reward = 0
        qstate = self.mdp.getTransitionStatesAndProbs(state, action)
        for next_state, prob in qstate:
            reward += prob*(self.mdp.getReward(state, action, next_state) + self.values[next_state]*self.discount)

        return reward

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state) == True:
            return None

        actions = self.mdp.getPossibleActions(state)

        #calculate the reward for every action taken
        act_reward = {}
        for act in actions:
            act_reward[act] = self.getQValue(state,act)

       
        return max(act_reward.items(), key=operator.itemgetter(1))[0]

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
        for i in range(self.iterations):
            index = i % len(self.mdp.getStates())
            state = self.mdp.getStates()[index]
            if self.mdp.isTerminal(state) == True: continue
            actions = self.mdp.getPossibleActions(state)
            self.values[state] = max([self.getQValue(state, act) for act in actions])


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
        #create a dictionary for every states
        #initialize the of the dictionary, such that {state: {predecessors}}
        predec_dic = {}
        for state in self.mdp.getStates():
            predec_dic[state] = set()

        #fill the dictionary with predecessors
        pq = util.PriorityQueue()
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state) == True: continue #terminate states will not be an predecessor
            actions = self.mdp.getPossibleActions(state)
            for act in actions:
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, act):
                    predec_dic[next_state].add(state)

            #push the difference for state value change on the priorityQueue
            maxQ = max([self.getQValue(state, act) for act in actions])
            diff = abs(self.values[state] - maxQ)
            pq.push(state,-diff)

        #update the state values according to priority
        for i in range(self.iterations):
            if pq.isEmpty() == True: break
            s = pq.pop()
            actions = self.mdp.getPossibleActions(s)
            self.values[s] = max([self.getQValue(s, act) for act in actions])
            for p in predec_dic[s]:
                actions = self.mdp.getPossibleActions(p)
                diff = abs(self.values[p] - max([self.getQValue(p, act) for act in actions]))
                if diff > self.theta:
                    pq.update(p ,-diff)


       
