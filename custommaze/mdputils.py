
from functools import partial

import numpy as np


def make_dict_to_indices(iterable):
    indexdict = {
        key: i
        for i, key in enumerate(iterable)
    }
    return indexdict


def convert_dict_to_function(dictionary):
    def fcn(x, dict1):
        return dict1[x]
    return partial(fcn, dict1=dictionary)


def policy_evaluation(pi, P, gamma=1.0, epislon=1e-10, stateindexdict=None):
    # dictionary from pos to index i
    if stateindexdict is None:
        stateindexdict = make_dict_to_indices(P.keys())

    # looping
    prev_V = np.zeros(len(P))
    while True:
        V = np.zeros(len(P))
        for state in P.keys():
            i = stateindexdict[state]
            action = pi[state]
            if action in P[state]:
                for policy_element in P[state][action]:
                    newstate = policy_element['state']
                    j = stateindexdict[newstate]
                    prob = policy_element['probability']
                    reward = policy_element['reward']
                    done = policy_element['terminal']
                    V[i] += prob * (reward + gamma*prev_V[j]*(not done))

        if np.max(np.abs(V - prev_V)) < epislon:
            break

        prev_V = V.copy()

    return V


def policy_improvement(V, P, gamma=1.0, stateindexdict=None, actionindexdict=None):
    # dictionary from pos to indeces
    if stateindexdict is None:
        stateindexdict = make_dict_to_indices(P.keys())
    # dictionary from action to indices
    actions = set([action for pos in P for action in P[pos]])
    if actionindexdict is None:
        actionindexdict = make_dict_to_indices(actions)

    # looping
    Q = np.zeros((len(P), len(actions)))
    for state in P.keys():
        i = stateindexdict[state]
        for action in actionindexdict.keys():
            j = actionindexdict[action]
            for policy_element in P[state][action]:
                newstate = policy_element['state']
                ip = stateindexdict[newstate]
                prob = policy_element['probability']
                reward = policy_element['reward']
                done = policy_element['terminal']
                Q[i, j] += prob * (reward + gamma*V[ip]*(not done))

    optimal_actions_index = np.argmax(Q, axis=1)
    new_pi = convert_dict_to_function({
        state: actions[optimal_actions_index[i]]
        for state, i in stateindexdict.items()
    })
    return new_pi
