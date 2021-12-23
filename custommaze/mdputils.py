
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


def make_state_action_dicts(P):
    stateindexdict = make_dict_to_indices(P.keys())
    actions = set([action for pos in P for action in P[pos]])
    actionindexdict = make_dict_to_indices(actions)
    return stateindexdict, actionindexdict


def make_enumerated_list(indexdict):
    items = [None]*len(indexdict)
    for key, value in indexdict.items():
        if value >= len(indexdict):
            raise ValueError('Not a valid enumerated indexdict!')
        items[value] = key
    return items


def policy_evaluation(pi, P, gamma=1.0, epsilon=1e-10, stateindexdict=None):
    # dictionary from pos to index i
    if stateindexdict is None:
        stateindexdict, _ = make_state_action_dicts(P)

    # looping
    prev_V = np.zeros(len(stateindexdict.keys()))
    while True:
        V = np.zeros(len(stateindexdict.keys()))
        for state in stateindexdict.keys():
            i = stateindexdict[state]
            action = pi(state)
            if action in P[state]:
                for policy_element in P[state][action]:
                    newstate = policy_element['state']
                    j = stateindexdict[newstate]
                    prob = policy_element['probability']
                    reward = policy_element['reward']
                    done = policy_element['terminal']
                    V[i] += prob * (reward + gamma*prev_V[j]*(not done))

        if np.max(np.abs(V - prev_V)) < epsilon:
            break

        prev_V = V.copy()

    return V


def policy_improvement(V, P, gamma=1.0, stateindexdict=None, actionindexdict=None):
    # dictionaries
    if stateindexdict is None or actionindexdict is None:
        stateindexdict. actionindexdict = make_state_action_dicts(P)
    actions = make_enumerated_list(actionindexdict)

    # looping
    Q = np.zeros((len(stateindexdict.keys()), len(actions)))
    for state in stateindexdict.keys():
        i = stateindexdict[state]
        for action in P[state].keys():
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


def policy_iteration(P, gamma=1.0, epsilon=1e-10, stateindexdict=None, actionindexdict=None):
    # dictionaries
    if stateindexdict is None or actionindexdict is None:
        stateindexdict. actionindexdict, actions = make_state_action_dicts(P)
    actions = make_enumerated_list(actionindexdict)

    # randomly initialize policy
    pi = convert_dict_to_function({
        state: action
        for state, action in zip(stateindexdict.keys(), np.random.choice(tuple(actions), len(stateindexdict)))
    })

    # looping
    while True:
        old_pi = {state: pi(state) for state in stateindexdict.keys()}
        V = policy_evaluation(pi, P, gamma=gamma, epsilon=epsilon, stateindexdict=stateindexdict)
        pi = policy_improvement(V, P, gamma=gamma, stateindexdict=stateindexdict, actionindexdict=actionindexdict)
        if old_pi == {state: pi(state) for state in stateindexdict.keys()}:
            break

    return V, pi


def value_iteration(P, gamma=1.0, epsilon=1e-10, stateindexdict=None, actionindexdict=None):
    # dictionaries
    if stateindexdict is None or actionindexdict is None:
        stateindexdict. actionindexdict, actions = make_state_action_dicts(P)
    actions = make_enumerated_list(actionindexdict)

    # initialize value function
    V = np.zeros(len(P))

    # looping
    while True:
        Q = np.zeros((len(stateindexdict.keys()), len(actions)))
        for state in stateindexdict.keys():
            i = stateindexdict[state]
            for action in P[state].keys():
                j = actionindexdict[action]
                for policy_element in P[state][action]:
                    newstate = policy_element['state']
                    ip = stateindexdict[newstate]
                    prob = policy_element['probability']
                    reward = policy_element['reward']
                    done = policy_element['terminal']
                    Q[i, j] += prob * (reward + gamma * V[ip] * (not done))

        new_V = np.max(Q, axis=1)
        if np.max(np.abs(V - new_V)) < epsilon:
            break

        V = new_V

    optimal_actions_index = np.argmax(Q, axis=1)
    pi = convert_dict_to_function({
        state: actions[optimal_actions_index[i]]
        for state, i in stateindexdict.items()
    })

    return V, pi
