This document describes how the experimental results presented in
Table **TODO** of the manuscript *Efficient attack–defense tree analysis using Pareto
attribute domains* were obtained and how can they be reproduced.

**1. Input preparation**

**1.1 Generation of trees**

Attack and attack-defense trees on which tests were conducted were generated
using `create_batch` function from [*generator.py*](./generator.py). The function itself makes calls
to functions `attack_tree_structured`, `attack_defense_tree_structured` and
`attack_tree_semantics_faster` from [*tree_factory.py*](./tree_factory.py). The structure of the trees generated by those functions
and some of their properties, which depend on the arguments provided, are described in descriptions of the functions.

**1.2 Generation of basic assignments**

For each of the trees, two basic assignments have been created. The first
of them consists of one value of cost, one value of difficulty, and one
value of time. The second one differs from the first one in that it contains
five values of cost instead of one. Values have been assigned only to the
actions of the attacker (who is the proponent in each of the trees). During
the computations performed later, each of the actions of the defender is assumed
to be assigned a vector of infinities (of appropriate length).

The assignments have been created using `pareto_ba` function from [*bas_factory.py*](./bas_factory.py).
Each of the values of cost and time has been picked uniformly at random from
the interval [0, 50], and each of the values of difficulty has been picked uniformly
at random from the set {0, 10, 100}.

**1.3 Storage of generated trees and values**

The trees have been exported to .xml files by the `generate_everything` function from
the file [*generator.py*](./generator.py). These files can be provided as input to
the [ADTool](https://satoss.uni.lu/members/piotr/adtool/) for graphical visualization.
For the convenience of the reader, we place three .jpg files containing
visualizations of trees *tree20.xml*, *tree24.xml* and *tree29.xml* in this directory.
The .xml files themselves are stored in the [trees](./trees) directory.

The basic assignments for the tree *treeXX.xml* are stored in files *treeXX_1_cost.txt*
and *treeXX_5_costs.txt*. Each line of each of the files is of the following form.

```
<name of basic action> <indent> <list of values assigned to the action, in the following order: costs, difficulty, time>
```

All of the basic assignments on which tests were performed are stored in the [assignments](./assignments) directory.

**2. Experiment description**

The experimental results were obtained by calling `main` function from the
[*tests.py*](./tests.py) file. The function iterates over the range of integers provided
as input, for each of them loads the corresponding tree from an .xml file,
and the corresponding basic assignments.

The `main` function first makes a call to the `basic_params` function,
defined in [*tests.py*](./tests.py). This function computes the basic parameters corresponding
to the tree. See comments in the body of the function for more details.

The time measurements were performed using `timingParetoOnSetSem`
and `timingParetoPOST` functions, defined in [*tests.py*](./tests.py). Each of the functions
starts a clock, runs the corresponding method of evaluation of Pareto domain for a
specified number *n* of times, stops the clock afterwards, and returns the elapsed time
divided by *n*. If at least one of the runs takes more than *3600* seconds, then the function
returns string *> 3600*. The value we chose for *n* was *20*.


**3. How to reproduce the results**

The following steps lead to reproducing the results.

1. Install Python, version >= 3.5.6.
2. Install the [adtrees](https://github.com/wwidel/adtrees) package using `pip install adtrees`.
3. Download the contents of this repository.
4. In the folder where the contents of this repository are stored, run
  * `python tests.py`, if you want to generate results for all of the trees (will take days). For each of the trees, a separate .txt files storing the results will be created.
  * `python reproduce.py i`, with "i" being an integer from the set {1, 2, ..., 32}. For the tree stored in *trees\treeXX.xml* file, a .txt file containing the tree's parameters as well as the results of time measurements for a single run of both methods of evaluation will be created.
