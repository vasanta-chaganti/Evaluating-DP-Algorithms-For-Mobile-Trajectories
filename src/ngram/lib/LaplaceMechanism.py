'''
@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A.
'''

'''
From Python 2 to 3:
    Import specific functions/classes from modules instead of using the * wildcard import.
    Update the function calls to map and lambda to explicitly convert them into lists.
'''

import os
import sys
sys.path.append(os.path.abspath("lib"))
import numpy as np
from Utils import laplace
from Histogram import Histogram

def LaplaceMechanism(hist, scale_p):
    """
    Adds laplace noise to all the bins in a given histogram
    Inputs
        hist: The histogram that noise will be added to
        scale_p: Epsilon parameter - how much noise to add
    """
    return Histogram([x + laplace(scale_p) for x in hist.bins])
    # python 2.7: return Histogram.Histogram(map(lambda x: x + Utils.laplace(scale_p), hist.bins))
