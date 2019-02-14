from tree_factory import attack_tree_structured
from tree_factory import attack_defense_tree_structured
from tree_factory import attack_tree_semantics_faster
from bas_factory import pareto_ba


def create_batch():
    '''
    Generate structured trees for tests.
    '''
    # the choice of parameters follows from the expected illustrative value of the
    # results obtained
    m_for_AT = [10, 12, 14, 15]
    m_for_ADT = [5, 7, 9]
    m_for_balanced = [10, 11, 12, 13]
    for m in m_for_AT:
        # k = number of repeated basic actions
        for k in [0, m // 4, m // 2, m - 2]:
            T = attack_tree_structured(m, k)
            yield(T)
    # adtrees
    for m in m_for_ADT:
        # in the resulting tree there will be 2*k repeated basic actions of the
        # proponent
        for k in [0, m // 4, m // 2, m - 2]:
            T = attack_defense_tree_structured(m, k)
            yield(T)
    # attack trees with the size of the set semantics smaller than the
    # expected runtime of the repeated bottom-up
    for m in m_for_balanced:
        T = attack_tree_semantics_faster(m)
        yield(T)


def create_assignments(T, name):
    '''
    Generate basic assignments of Pareto attributes for tree T.
    '''
    ba1 = pareto_ba(T, 1, 1, 1)
    ba5 = pareto_ba(T, 5, 1, 1)
    ba1.output(name + str('_1_cost'))
    ba5.output(name + str('_5_costs'))


def generate_everything():
    '''
    Generate .xml files of structured trees and .txt files holding corresponding basic assignments.
    '''
    name = 'tree'
    test_num = 1
    for T in create_batch():
        # modify the name
        if test_num < 10:
            new_name = name + '0' + str(test_num)
        else:
            new_name = name + str(test_num)
        test_num += 1
        # create and output assignments
        create_assignments(T, new_name)
        # output the structure of the tree to an .xml file
        T.output(new_name)


if __name__ == '__main__':
    # generate_everything()
    pass
