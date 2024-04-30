'''
Utility functions.

@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A.

'''

'''
From Python 2 to 3:
    wrap map inside list
    directly import reduce from functools
'''

import math
import random as rnd
import numpy as np
from functools import reduce

def strToSeq(str, dec=0):
    """
    Converts a given string to a dict object
    Inputs
        str: the given string
        dec: an int value 
    """
    # Python 2.7: return functools.reduce(lambda x,y: x + y, map(lambda x: chr(int(x)-dec), str))
    return reduce(lambda x, y: x + y, map(lambda x: chr(int(x) - dec), str))

def seqToStr(sequence, inc=0):
    """
    Converts a map object to a string
    Inputs
        sequence: the given map object
        inc: an int value
    """
    return " ".join(map(lambda x: str(ord(x)+inc), sequence))

def KL_div(p, q):
    """
    Calculates the sum of all bins in p that have value > 0. 
    Before summing the values multiples each value by the log of 
    (p[i]/q[i]).
    Inputs
        p: the first given histogram
        q: the second given histogram
    """
    s = 0
    for i in range(len(p)):
        if p[i] > 0:
            s += p[i] * math.log(float(p[i]) / q[i])
    return s

def sanitize(hist):
    """
    Iterates over the bins in a histogram and replaces any value below
    1 with 1.
    Inputs
        hist: the given histogram
    """
    # Python 2.7: return map(lambda x: max(1, x), hist)
    return list(map(lambda x: max(1, x), hist))

def l2norm(values):
    """
    Squares the absolute value of each bin and sums these values up. Then,
    return the square root of the sum.
    Input
        values: the values to iterate over
    """
    # Python 2.7: return math.sqrt(functools.reduce(lambda x,y: x + abs(y)**2, values))
    return math.sqrt(reduce(lambda x, y: x + abs(y)**2, values))

def is_int(s):
    """
    Checks to see if a given value is an integer.
    Inputs
        s: the given value
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

def laplace(p_lambda):
    """
    Creates a random amount of laplace noise
    Inputs
        p_lambda: the epsilon value - amount of noise to be generated
    """
    return np.random.laplace(0, p_lambda, 1)[0]

def normalize(vec):
    """
    Takes in a list of values and normalizes each bin in the list.
    Inputs
        vec: the vector to be normalizes
    """
    s = sum(vec)
    # Python 2.7: return vec if s <= 0 else map((lambda x: x/float(s)), vec)
    return vec if s <= 0 else list(map(lambda x: x / float(s), vec))

def stat_dist(d1, d2):
    """
    Given two arrays/lists of the same length, calculates the abs value 
    differences between respective indeces and returns the sum of these 
    differences.
    Inputs
        d1: a given list
        d2: a given list
    """
    return sum((abs(d1[i] - d2[i]) for i in range(len(d1))))


