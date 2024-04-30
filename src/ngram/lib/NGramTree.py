'''
Exploration Tree class.

@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., ViKtoriia Z., Ziming Y., Koyo A.
'''

'''
From Python 2 to 3:
    Replace the use of bitarray module with the bitarray class from the bitarray module.
    Update the print statements to use parentheses.
    Replace the use of the iteritems() method with the items() method in the for loops.
    Update the function calls to reversed to convert the resulting iterator into a list explicitly.
    Update the division operator / to use // and % for integer division and modulus operations, respectively.
    Remove the redundant parentheses from the while loop condition.
    Replace the use of xrange with range.
    Replace the use of iteritems() with items()
'''

import os
import sys
sys.path.append(os.path.abspath("lib"))
import numpy as np
from Utils import strToSeq
from Histogram import Histogram
from LaplaceMechanism import LaplaceMechanism
import math
from bitarray import bitarray
from collections import Counter


class Node:
    #a node is an ngram
    def __init__(self, start_id, size, parent_id, histogram, level = None):
        #constructor
        self.start_id = start_id
        self.histogram = histogram
        self.parent_id = parent_id
        self.childrens = np.array([None] * size)
        self.released = bitarray([False] * size)
        self.size = size
        self.level = level
        self.left_level = None
        self.eps = None

    def laplace(self, b):
        #apply laplace mechanism to the ngram with the scale b
        self.histogram = LaplaceMechanism(self.histogram, b)

    def releaseAll(self):
        #release all items of the ngrams
        # python 2.7: self.released = bitarray([True] * self.size)
        self.released.setall(True)

    def hasReleasedItem(self):
        #check if the ngram has released any items
        return self.released.any()

    def areAllItemsReleased(self):
        #check if the ngram has released all the items
        return self.released.all()

    def __repr__(self):
        #return a string representation of the ngram
        return self.histogram.__repr__()

    def __len__(self):
        #return the length of the ngram
        return len(self.histogram)

class NGramTree:
    #ngram tree class
    def __init__(self, ngram_set):
        #constructor
        self.nodes = {}
        self.size = ngram_set.alphabet_size + 1 # with the end symbol
        self.ngram_set = ngram_set
        self.start_id = 0
        self.levels = None

    def isRoot(self, node):
        #check if an ngram is a root
        return node == self.nodes[0]

    def __len__(self):
        #return the amount of ngrams
        return len(self.nodes)

    def getMarkovianParentByGram(self, gram):
        if len(gram) == 1:
            return self.getRoot()
        else:
            node = None
            while node is None and len(gram) > 0:
                gram.pop()
                try:
                    node = self.getNodeByGram(gram)
                # If a children is set to None we jump to the next markovian
                # neighbor (we got Typerror or KeyError)
                except KeyError as exception:
                    if exception.args[0] is None:
                        node = None
                    else:
                        raise exception
                except TypeError as exception:
                    node = None
            return node

    def getMarkovianParent(self, node):
        return self.getMarkovianParentByGram(self.idToGram(node.parent_id))

    def getParentCount(self, node):
        #return the amount of parents
        return self.getCountById(node.parent_id)

    def getReleasedMarkovianParent(self, node):
        #return a markovian parent that has released any items
        if node.parent_id == -1:
            return node

        released = False
        #id = node.parent_id % self.size
        while not released:
            node = self.getMarkovianParent(node)
            released = node.hasReleasedItem()
            #released = node.released[id]

        return node

    # Calling this function also expands the tree
    def getChild(self, node, id):
        #return the nodes children, and if there's none, create some from the ngram set
        if node.childrens[id] is None:
            parent_id = node.start_id + id
            histogram = self.getOriginalHistogram(parent_id)
            
            self.nodes[self.start_id] = Node(self.start_id, self.size, parent_id, histogram, node.level + 1)
            node.childrens[id] = self.start_id  
            self.start_id += self.size

        return self.nodes[node.childrens[id]]

    def getOriginalHistogram(self, parent_id):
        #restore the original histogram from the ngram set
        parent_gram = self.idToGram(parent_id)
        bins = np.zeros(self.size)
        # Fetching real counts from NGramSet
        for i in range(self.size):
            seq = strToSeq(reversed(parent_gram)) + chr(i)
            bins[i] = self.ngram_set[seq]

        return Histogram(bins)

    def getOriginalHistogramByNode(self, node):
        #call the method above knowing only the node
        return self.getOriginalHistogram(node.parent_id)

    def isParentReleased(self, node):
        #check if the parent has released any items
        start_id = (node.parent_id // self.size) * self.size
        return self.nodes[start_id].released[node.parent_id % self.size]

    def createRoot(self):
        #create a root
        self.getRoot()

    def getRoot(self):
        #create a root of the ngram tree
        if not 0 in self.nodes:
            bins = np.zeros(self.size)
            # termination is always 0
            for i in range(self.size - 1):
                bins[i] = self.ngram_set[chr(i)]
            
            self.nodes[0] = Node(0, self.size, -1, Histogram(bins), 1)
            self.start_id += self.size

        return self.nodes[0]

    def createNGramSet(self):
        #create the ngram set of the tree
        # naive 
        self.ngram_set.clear()
        # for (id, node) in self.nodes.iteritems():
        for id, node in self.nodes.items():
            if node.hasReleasedItem():
                for i in range(self.size):
                    self.ngram_set[strToSeq(list(reversed(self.idToGram(node.parent_id))) + [i])] = node.histogram[i]

        return self.ngram_set

    def getAllParents(self, node):
        #returns all the parents of the given node
        parent_id = node.parent_id
        parents = []
        while parent_id != -1:
            start_id = (parent_id // self.size) * self.size
            parents.append(self.nodes[start_id])
            parent_id = self.nodes[start_id].parent_id

        return parents

    def getProbById(self, id):
        start_id = (id // self.size) * self.size
        return self.nodes[start_id].histogram.normalize()[id % self.size]

    def getCountById(self, id):
        #return the amount of bins from the ngram
        start_id = (id // self.size) * self.size
        return self.nodes[start_id].histogram[id % self.size]

    def idToGram(self, parent_id):
        #create an ngram by using a parent id 
        gram = []
        while parent_id != -1:
            gram.append(parent_id % self.size)
            start_id = (parent_id // self.size) * self.size
            parent_id = self.nodes[start_id].parent_id

        return gram[::-1]

    def gramToId(self, gram):
        #return id of the ngram
        start_id = 0
        gram_cpy = list(gram)
        while len(gram_cpy) > 1:
            item = gram_cpy.pop(0)
            start_id = self.nodes[start_id].childrens[item] 
        
        return start_id + gram_cpy.pop(0) if gram_cpy else start_id

    def getNodeGram(self, node):
        return self.idToGram(node.parent_id)

    def getNodeByGram(self, gram):
        return self.getNodeById(self.gramToId(gram))

    def getNodeById(self, id):
        start_id = (id // self.size) * self.size
        return self.nodes[self.nodes[start_id].childrens[id % self.size]]

    def iternodes(self):
        #iterate through the grams
        i = 0
        # python 2.7: gram = []
        while i in self.nodes:
            yield (self.idToGram(self.nodes[i].parent_id), self.nodes[i])
            i += self.size

    def getProbByGram(self, gram): 
        return self.getProbById(self.gramToId(gram))

    def getCountByGram(self, gram): 
        return self.getCountById(self.gramToId(gram))

