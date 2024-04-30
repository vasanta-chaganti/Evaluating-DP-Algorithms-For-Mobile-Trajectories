'''
@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A.
'''

'''
From Python 2 to 3:
    Imported modules and classes are adjusted to use the correct Python 3 syntax.
    Updated the compare_grams function to use the appropriate comparison operators (<, ==, >) instead of the deprecated cmp function.
    Replaced the print statements with print() function calls to ensure compatibility with Python 3's print syntax.
    Updated the class definition for Reconstruction to use the correct syntax for inheriting from parent classes.
    Adjusted the compare_grams function to use key argument of the sorted function instead of the deprecated cmp_to_key function.
    Replaced the xrange function calls with range for Python 3 compatibility.
    Adjusted the division operator / to perform floating-point division (/) instead of integer division (//) where necessary.
    Updated the usage of the itertools.imap function to map function for Python 3 compatibility.
    Adjusted the bitarray instantiation to use the correct syntax.
'''

import os
import sys
sys.path.append(os.path.abspath("lib"))
from lib.NGramSet import NGramSet
from lib.NGramTree import NGramTree
from lib.Utils import *
import math
from itertools import compress
import numpy as np
from bitarray import bitarray

def ngram(ngrams_set, n_max, budget, sensitivity): 
    """
    This function takes ngram set, the max ngram length n_max, a privacy budget, and 
    sensitivity. It then initializes an ngram tree structure, where each node represents 
    a different ngram and contains a histogram of counts for each possible next element 
    in the sequence. 

    Laplace noise is added to the counts of each node's histogram in the tree. 

    Histogram of each node is adjusted based on the released counts. Unreleased counts
    are approximated based on Markov assumption. The histogram is then renormalized to 
    make it consistent with the parent node's count. 
    """
    # Loading the set of all ngrams
    budget = float(budget)

    # Python 2.7 - tree = NGramTree.NGramTree(ngrams_set)
    tree = NGramTree(ngrams_set)
    # This creates the root
    root = tree.getRoot()

    # We always release the root
    root.left_level = n_max
    root.eps = budget / root.left_level
    root.laplace(sensitivity / root.eps)
    root.releaseAll()
    # we have no empty sequences:
    root.histogram[root.size-1] = 0

    for (gram, node) in tree.iternodes():
        # We do not process levels beyond n_max
        if node.level > n_max:
            break

        # Python 2.7 - if tree.isRoot(node) or tree.isParentReleased(node) and node.left_level != None:
        if tree.isRoot(node) or tree.isParentReleased(node) and node.left_level is not None:
            theta = sensitivity * math.log(tree.size/2.0) / node.eps
            markovian_neighbor = tree.getReleasedMarkovianParent(node)
            #print("Markovian parent:", markovian_neighbor, "Gram:", tree.getNodeGram(markovian_neighbor))
            for i in range(node.size):
                ## To Rui: we release the leaves: left_level is 1 (and do not do thresholding)
                if node.left_level <= 1 or theta < node.histogram[i]:
                #if theta < node.histogram[i]:
                    node.released[i] = True
                    
                    # we do not expand the end symbol
                    if node.left_level > 1 and i < node.size - 1:
                        child = tree.getChild(node, i)
                        child_markovian_neighbor = tree.getReleasedMarkovianParent(child)
                        p_max = markovian_neighbor.histogram.normalize().max()

                        #print("i", i, "h", node.histogram[i], "t", theta, "p", p_max)
                        if p_max == 1:
                            child.left_level = n_max - node.level
                        else:
                            child.left_level = int(min(n_max - node.level, math.ceil(math.log(theta / node.histogram[i], p_max)))) 
                        child.eps = (budget - sum(map(lambda x: x.eps, tree.getAllParents(child)))) / child.left_level
                        child.laplace(sensitivity / child.eps)
            
            if not node.hasReleasedItem() or tree.isRoot(node):
                continue

            # Now, we normalize the whole histo based on the noisy counts computed before
            # If there are unreleased bins, approximate them based on Markov property
            # Note: root is generally a bad markovian approximation
            # Finally, we recompute the noisy count using this normalized histo. and the count of
            # the parent node. This step results in better utility and provides
            # consistency

            ### Approximating the non-released bins
            parent_count = tree.getParentCount(node)

            norm_hist = node.histogram.normalize()
            released_items = list(compress(norm_hist, node.released))

            # Approximation
            released_sum = sum(list(compress(node.histogram, node.released)), 0.0)
            released_markov_sum = sum(list(compress(markovian_neighbor.histogram, node.released)), 0.0)

            # Markov neighbor is not unigrams, so Markov neighbor is a good approximator
            if markovian_neighbor.level > 1:
                for i in range(node.size):
                    if not node.released[i]:
                        if released_markov_sum == 0:
                            node.histogram[i] = 0
                        else:
                            node.histogram[i] = released_sum * (markovian_neighbor.histogram[i] / released_markov_sum)

            # Markov neighbor is unigrams (which is a bad approximator), so
            # we uniformly divide the left probability mass among non-released items
            elif released_sum <= parent_count:
                for i in range(node.size):
                    if not node.released[i]:
                        node.histogram[i] = (parent_count - released_sum) / (len(norm_hist) - len(released_items)) 

            else:
                for i in range(node.size):
                    if not node.released[i]:
                        node.histogram[i] = 0


            # Renormalize the histogram to make it consistent
            node.histogram = node.histogram.normalize() * parent_count 

    return tree.createNGramSet()

