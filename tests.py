import time
from adtrees.default_domains import setSemSize  # SetSemBound
from adtrees import ParetoDomain
from adtrees import ADTree
from adtrees import BasicAssignment


def basic_params(T):
    '''
    For a tree T, return the list of basic parameters, roughly of the following form.
        [order, number_of_clones, SetSemBound, SetSemSize, uncounteredBound, uncounteredStrats]
    '''
    result = ['number of nodes: ' + str(T.order())]
    number_of_clones = len(
        [label for label in T.basic_actions('a') if T.isclone(label)])
    result.append(
        'number of repeated basic actions of the proponent: ' + str(number_of_clones))
    # 1. SetSemBound
    ba = BasicAssignment()
    # 1.1 Create a basic assignment as defined in Lemma 5 of
    # "Efficient attack–defense tree analysis using Pareto attribute domains".
    for b in T.basic_actions():
        ba[b] = 1
    # 1.2 Perform the bottom-up evaluation of the SetSemBound domain under the
    # above basic assignment.
    SetSemBound = setSemSize.evaluateBU(T, ba)
    result.append('bound on the size of the set semantics: ' +
                  str(SetSemBound))
    # 2. SetSemSize: create the set semantics and get the number of its
    # elements.
    setsem = T.set_semantics()
    SetSemSize = len(setsem)
    result.append('size of the set semantics: ' + str(SetSemSize))
    # 3. uncounteredBound
    # 3.1 Modify the basic assignment defined before, so it becomes the one defined in Lemma 6 of
    # "Efficient attack–defense tree analysis using Pareto attribute domains".
    for b in T.basic_actions('d'):
        ba[b] = 0
    # 3.2 Perform the bottom-up evaluation of the SetSemBound domain under the
    # above basic assignment.
    uncounteredBound = setSemSize.evaluateBU(T, ba)
    result.append(
        'bound on the number of uncountered strategies: ' + str(uncounteredBound))
    # 4. uncounteredStrats: the actual number of uncountered strategies
    # is the number of pairs in the set semantics whose second element is the
    # empty set.
    uncounteredStrats = len([strat for strat in setsem if strat[1] == set()])
    result.append('number of uncountered strategies: ' +
                  str(uncounteredStrats))
    return result


def timingParetoOnSetSem(tree, domain, ba, how_many_times):
    '''
    Measure the average time it takes to compute the set of all Pareto
    optimal values for ADTree "tree", for the Pareto domain  "domain", under
    the basic assignment "ba", using evaluation on the set semantics.
    '''
    start = time.clock()
    for i in range(how_many_times):
        innerClockStart = time.clock()
        domain.evaluateSS(tree, ba)
        innerClockEnd = time.clock()
        if innerClockEnd - innerClockStart > 3600:
            return '> 3600'
    end = time.clock()
    res = (end - start) / how_many_times
    if res < 0.01:
        return '< 0.01'
    else:
        return str(round(res, 2))


def timingParetoPOST(tree, domain, ba, neutral, absorbing, how_many_times):
    '''
    Measure the average time it takes to compute the set of all Pareto
    optimal values for ADTree "tree", for the Pareto domain  "domain", under
    the basic assignment "ba", using evaluation method defined in
        "On quantitative analysis of attack-defense trees with repeated labels"
    (proceedings of POST 2018).
    '''
    start = time.clock()
    for i in range(how_many_times):
        innerClockStart = time.clock()
        domain.evaluateRBU(tree, ba, neutral, absorbing)
        innerClockEnd = time.clock()
        if innerClockEnd - innerClockStart > 3600:
            return '> 3600'
    end = time.clock()
    res = (end - start) / how_many_times
    if res < 0.01:
        return '< 0.01'
    else:
        return str(round(res, 2))


def main(trees, number_of_measurements=20):
    # create the two Pareto domains
    domain_1_cost = ParetoDomain(1, 2)
    domain_5_costs = ParetoDomain(5, 2)
    neutral1 = [[0, 0, 0]]
    neutral5 = [[0, 0, 0, 0, 0, 0, 0]]
    absorbing1 = [[2**30, 2**30, 2**30]]
    absorbing5 = [[2**30, 2**30, 2**30, 2**30, 2**30, 2**30, 2**30]]
    #
    name = 'tree'
    for test_num in trees:
        # modify the name
        if test_num < 10:
            new_name = name + '0' + str(test_num)
        else:
            new_name = name + str(test_num)
        # load tree
        T = ADTree('trees\\' + new_name + '.xml')
        # feedback
        print('Tree stored in "trees\\' +
              new_name + '.xml" has been loaded.')
        print('Start, the time is ' + time.ctime() + '.')
        # create output file to store results in
        res_name = new_name + '_results.txt'
        result = open(res_name, 'w')

        # feedback
        print('Computing basic parameters.')

        # 1. basic parameters
        bparams = basic_params(T)
        num_of_clones = int(bparams[0].split(':')[1].strip())
        for item in bparams:
            result.write(item + '\n')

        # 2. with 1 cost
        # feedback
        print('Computing Pareto optimal values using 1+2 Pareto domain.')

        ba = BasicAssignment('assignments\\' + new_name + '_1_cost.txt')

        # 2.0 number of Pareto optimal values
        if num_of_clones < 12:
            # if the number of repeated basic actions of the proponent is
            # "small"
            pareto_optimal = len(domain_1_cost.evaluateRBU(
                T, ba, neutral1, absorbing1))
        else:
            pareto_optimal = len(domain_1_cost.evaluateSS(T, ba))

        result.write(
            'number of pareto optimal values for 1+2 domain: ' + str(pareto_optimal) + '\n')

        # 2.1 timing on set semantics
        result.write('1+2 domain, timing when evaluating on set semantics: ' + timingParetoOnSetSem(
            T, domain_1_cost, ba, number_of_measurements) + '\n')

        # 2.2 timing using repeated bottom-up
        result.write('1+2 domain, timing when using "method of [2]": ' + timingParetoPOST(
            T, domain_1_cost, ba, neutral1, absorbing1, number_of_measurements) + '\n')

        # 3. with 5 costs
        # feedback
        print('Computing Pareto optimal values using 5+2 Pareto domain.')

        ba = BasicAssignment('assignments\\' + new_name + '_5_costs.txt')

        # 3.0 number of Pareto optimal values
        if num_of_clones < 12:
            # if the number of repeated basic actions of the proponent is
            # "small"
            pareto_optimal = len(domain_5_costs.evaluateRBU(
                T, ba, neutral5, absorbing5))
        else:
            pareto_optimal = len(domain_5_costs.evaluateSS(T, ba))

        result.write(
            'number of pareto optimal values for 5+2 domain: ' + str(pareto_optimal) + '\n')

        # 3.1 timing on set semantics
        result.write('5+2 domain, timing on set semantics: ' + timingParetoOnSetSem(
            T, domain_5_costs, ba, number_of_measurements) + '\n')

        # 3.2 timing using repeated bottom-up
        result.write('5+2 domain, timing when using "method of [2]": ' + timingParetoPOST(
            T, domain_5_costs, ba, neutral5, absorbing5, number_of_measurements) + '\n')

        # close the output file
        result.close()

        # feedback
        print('Done, the time is ' + time.ctime() + '.\n')
        print('Results written to ' + res_name + '.')
    return


if __name__ == '__main__':
    # trees to run the tests on
    trees = [i for i in range(1, 33)]
    # run
    main(trees)
