
import numpy as np


def policy_evaluation(pi, P, gamma=1.0, epislon=1e-10):
    prev_V = np.zeros(len(P))
    while True:
        V = np.zeros(len(P))
