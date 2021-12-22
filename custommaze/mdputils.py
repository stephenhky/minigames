
import numpy as np


def policy_evaluation(pi, P, gamma=1.0, epislon=1e-10):
    # dictionary from (x, y) to index i
    indexdict = {
        (x, y): i
        for i, (x, y) in enumerate(P)
    }

    # looping
    prev_V = np.zeros(len(P))
    while True:
        V = np.zeros(len(P))
        for x, y in P.keys():
            i = indexdict[(x, y)]
            direction = pi[(x, y)]
            if direction in P[(x, y)]:
                for policy_element in P[(x, y)][direction]:
                    newx, newy = policy_element['state']
                    j = indexdict[(newx, newy)]
                    prob = policy_element['probability']
                    reward = policy_element['reward']
                    done = policy_element['terminal']
                    V[i] += prob * (reward + gamma*prev_V[j]*(not done))

        if np.max(np.abs(V - prev_V)) < epislon:
            break

        prev_V = V.copy()

    return V


