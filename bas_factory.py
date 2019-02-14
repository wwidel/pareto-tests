from adtrees import BasicAssignment
import numpy as np


def pareto_ba(T, m, k, n):
    '''
    Generate a basic assignment for basic actions in ADTree T,
    for the Pareto domain induced by
        m minimal cost domains,
        k minimal difficulty domains, and
        n minimal time domains.

    The actions of the defender are assigned vector of infinities.
    '''
    min_cost = 0
    max_cost = 50
    diff_vals = [0, 10, 100]
    min_time = 0
    max_time = 50
    infty = 2**20
    ba = BasicAssignment()
    for b in T.basic_actions('a'):
        vals = []
        # m costs
        for i in range(m):
            vals.append(np.random.randint(min_cost, max_cost + 1))
        # k diffs
        for i in range(k):
            vals.append(diff_vals[np.random.randint(0, 3)])
        # n times
        for i in range(n):
            vals.append(np.random.randint(min_time, max_time + 1))

        ba[b] = [vals]

    for b in T.basic_actions('d'):
        ba[b] = [[infty for i in range(m + k + n)]]

    return ba
