from adtrees import ADNode, ADTree


def attack_tree_structured(m, k=0, dic=0):
    '''
    int m >= 2
    int k <= m

    Return attack tree ANDp(ORp(b1, b2), ..., ORp(b_{2*m-1}, b_{2*m})), with
        2*m leaf nodes,
        k <= m repeated basic actions, and
        3*m + 1 nodes.

    If dic == 1, then return dictionary holding the structure of the tree, and not tree itself.

    Remark: if k=0, then the size of the set semantics of the tree is 2**m.
    '''
    root = ADNode('a', 'root', 'AND')
    dict = {root: []}
    new_leaf = 1
    for i in range(m):
        # create new nodes
        ornode = ADNode('a', 'ref_' + str(i + 1), 'OR')
        leftchild = ADNode('a', new_leaf)
        rightchild = ADNode('a', new_leaf + 1)
        # update dictionary
        dict[root].append(ornode)
        dict[ornode] = [leftchild, rightchild]
        dict[leftchild] = []
        dict[rightchild] = []
        # update the label of the next leaf node
        if new_leaf < k:
            new_leaf += 1
        else:
            new_leaf += 2

    if dic:
        return dict

    return ADTree(dictionary=dict)


def attack_defense_tree_structured(m, k):
    '''
    int m >= 2
    int k <= m

    Return attack-defense tree
    ANDp(ORp(Cp(b1, Co(b_{2*m+1}, b_{4*m+1})), Cp(b2, Co(b_{2*m+2}, b_{4*m+2}))), ..., ORp(Cp(b_{2*m-1}, Co(b_{4*m-1}, b_{6*m+1})), Cp(b_{2*m}, Co(b_{4*m}, b_{6*m}))),
    with
        7*m + 1 nodes,
        6*m nodes holding basic actions, and
        k <= 2*m repeated basic actions of the proponent.


    Remark: if k=0, then the size of the set semantics of the tree is 2**(2 * m).
    '''
    d = attack_tree_structured(m, k, dic=1)
    basics = [node for node in d if d[node] == []]
    for node in basics:
        counternode = ADNode('d', int(node.label) + 2 * m)
        countercounter = ADNode('a', int(node.label) + 4 * m)
        d[node].append(counternode)
        d[counternode] = [countercounter]
        d[countercounter] = []
    return ADTree(dictionary=d)


def attack_tree_semantics_faster(m):
    '''
    m >= 2

    Return attack tree
    ANDp(T, ORp(b_{13}, b_{13}, ..., b_{12 + m},b_{12 + m})),
    where
    T = ANDp(ORp(b1, b2), ..., ORp(b_11, b_12})),
    i.e., T is a tree obtained by calling attack_tree_structured(6, 0).

    The tree created has
        2*m + 21 nodes,
        2*m + 12 nodes holding basic actions,
        m repeated basic actions of the proponent, and
        set semantics of size 64*m.

    Therefore, the repeated bottom-up procedure is expected to terminate in time
    O((2*m + 21) * 2**m)) = O(m * 2**m).
    '''
    T = attack_tree_structured(6)
    new_root = ADNode('a', 'new_root', 'AND')
    new_ref = ADNode('a', 'ref_7', 'OR')
    d = T.dict
    d[new_root] = [T.root, new_ref]
    d[new_ref] = [ADNode('a', 12 + i)
                  for i in range(1, m + 1) for j in range(2)]
    for child in d[new_ref]:
        d[child] = []
    return ADTree(dictionary=d)


if __name__ == '__main__':
    pass
