'''
Histogram class.

@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A.
'''

'''
From Python 2 to 3:
    Replace the use of the map function with list comprehension where necessary.
    Update the print statements to use parentheses.
    Replace the types long and float with int and float, respectively.
    Replace the division operator / with // for integer division, or / if floating-point division is intended.
    Import the required modules at the beginning of the code.
    Update the function calls to zip, enumerate, and other functions that return iterators to convert them into lists explicitly.
'''

import os
import sys
sys.path.append(os.path.abspath("lib"))
import Utils
import numpy as np
import math
import heapq

class Histogram:

    def __init__(self, bins = [], normalized=False, bin_num=None):
        """
        This initializer creates a histogram with a given number of bins that is not 
        normalized, unless inputted otherwise.
        Inputs
            bins: the bins of the histogram to be constructed
            normalized: this parameter can be set to true to normalize the histogram
            bin_num: number of bins in the histogram
        """
        if bin_num is not None:
            self.bins = np.zeros(bin_num)
        if len(bins) > 0:
            self.bins = np.array([max(x, 0) for x in bins])
            # python 2.7: self.bins = np.array(map(lambda x: max(x, 0), bins))
            
        self.normalized = normalized

    def loadFromFile(self, filename, normalized = False,  lines = []):
        """
        ** This function is not used **
        This file loads data from a file into a histogram that is not normalized, 
        unless inputted otherwise.
        Inputs
            filename: the name of the file that contains data to be imported
            normalized: this parameter can be set to true to normalize the histogram
            lines: a collection of lines from the file? (unsure)
        """
        file = open(filename)
        bins = []
        i = 0
        for line in file:
            if not lines or i in lines:
                line = line.strip()
                # python 2.7: str = line.strip()
                if line.startswith('#') or line.startswith('//') or line.startswith('%'):
                    continue
                for val in line.split():
                    if Utils.is_int(val):
                        bins.append(int(val)) 
            i += 1

        self.bins = np.array(bins)
        self.normalized = normalized

        file.close()

    def sort(self):
        """
        ** Not used **
        Sorts the bins of the histogram in ascending order by size
        """
        return Histogram(sorted(self.bins, reverse=True)) 

    def max(self):
        """

        Returns the bin with the largest size (the most amount of data falls within that bin)
        """
        
        return np.max(self.bins)
        # python 2.7: return max(self.bins)

    def clone(self):
        """
        Created a new copy of an existing histogram (duplicates)
        """
        return Histogram(np.array(self.bins), normalized=self.normalized) 

    def update(self, bins):
        """
        Updates an existing histogram with new bin values
        Inputs
            bins: the new bins to be input into a histogram
        """
        self.bins = np.array([max(x, 0) for x in bins])
        # python 2.7: self.bins = np.array(map(lambda x: max(x, 0), bins))

    def __getitem__(self,key):
        """
        Returns an item from the bins array at a given index
        Inputs
            key: the index of the desired item
        """
        return self.bins[key]

    def __setitem__(self,key,val):
        """
        Sets the value of a bin at a given index
        Inputs
            key: the index of the desired item
            val: the new value of the desired item
        """
        self.bins[key] = val

    def count(self):
        """
        Returns the sum of all the bins in the Histogram
        """
        return np.sum(self.bins)
        # python 2.7: return sum(self.bins)

    def sum(self):
        """
        Returns the sum of all the bins in the Histogram by calling self.count()
        """
        return self.count()

    def nullifyNaN(self):
        """
        If the histogram is not normalized, replaces all NaN's with 0.
        Otherwise, throws an assertion error.
        """
        assert not self.normalized
        self.bins = [0 if math.isnan(x) else x for x in self.bins]
        # python 2.7: self.bins = map(lambda x: 0 if math.isnan(x) else x, self.bins)

    def quantile(self, p):
        """
        Returns the bin before which the (sum of all values up to that bin) / (sum of all values) is greater than
        a given proportion p. If the sum of no bins exceed the given proportion p, returns 0.
        Inputs
            p: the inputted proportion (a threshold)
        """
        count = self.count()
        s = 0

        for i in range(len(self)):
            s += self.bins[i]
            if count > 0 and float(s) / count > p:
                return i - 1

        return 0
        

    def __add__(self,other):
        """
        If other is an int or a float, then adds other to all bin values (adds same "other" value to all bins). 
        Else if other is an array, then adds the respective values to the respective bins (adds different other values
        to different bins).
        Input
            other: the value to be added to the bins
        """
        if isinstance(other, (int, float)):
            return Histogram([x + other for x in self.bins])
        # python 2.7: if isinstance(other,  (int, int, float)):
        # python 2.7:  return Histogram(map(lambda x: x + other, self.bins)) 
        else:
            return Histogram([sum(x) for x in zip(self.bins, other.bins)])
            # python 2.7: return Histogram(map(sum, zip(self.bins, other.bins)))

    def __mul__(self,other):
        """
        Multiples every value in a bin with a given value
        Inputs
            other: the given value
        """
        if isinstance(other, (int, float)):
            return Histogram([x * other for x in self.bins])
        # python 2.7: if isinstance(other,  (int, int, float)):
        # python 2.7:    return Histogram(map(lambda x: x * other, self.bins))  
        else:
            raise NameError('NotImplemented')

    def __imul__(self, other):
        """
        Multiples every value in a bin with a given value and sets the histogram
        such that it is not normalized.
        Inputs
            other: the given value
        """
        if isinstance(other, (int, float)):
            self.bins = [x * other for x in self.bins]
        # python 2.7: if isinstance(other, (int, int, float)):
        # python 2.7    self.bins = map(lambda x: x * other, self.bins)
            self.normalized = False
        else:
            raise NameError('NotImplemented')

        return self

    def __iadd__(self, other):
        """
        If other is an int or a float, then adds other to all bin values (adds same "other" value to all bins). 
        Else if other is an array, then adds the respective values to the respective bins (adds different other values
        to different bins).
        Input
            other: the value to be added to the bins
        """
        if isinstance(other, (int, float)):
            self.bins = [x + other for x in self.bins]

        self.bins = [sum(x) for x in zip(self.bins, other.bins)]

        # python 2.7: if isinstance(other, (int, int, float)):
        # python 2.7:     self.bins = map(lambda x: x + other, self.bins)
        # python 2.7: self.bins = map(sum, zip(self.bins, other.bins)

        return self

    def __truediv__(self,other):
        """
        Divides every value in a bin by a given value.
        Inputs
            other: the given value
        """
        if isinstance(other, (int, float)):
            return Histogram([float(x) / other for x in self.bins])
        # python 2.7: if isinstance(other,  (int, int, float)):
        # python 2.7:    return Histogram(map(lambda x: float(x) / other, self.bins))
        else:
            raise NameError('NotImplemented')

    def getTop(self, T):
        """
        Returns the first T largest bin value in a histogram
        Inputs
            T: number of bins to be returned
        """
        return list(map(lambda x: tuple(reversed(x)), heapq.nlargest(T, list(map(lambda x: tuple(reversed(x)), list(enumerate(self.bins)))))))
        # python 2.7: return map(lambda x: tuple(reversed(x)), heapq.nlargest(T, map(lambda x: tuple(reversed(x)), list(enumerate(self.bins)))))
    
    def getFirst(self, T):
        """
        Returns the value of the first T bins in a histogram
        Inputs
            T: number of bins to be returned
        """
        return list(enumerate(self.bins))[:T]

    def normalize(self, sanitize = False):
        """
        Normalized the bins in a histogram
        Inputs:
            sanitize: set to true if the bins should be sanitized first
        """
        # python 2.7: if self.normalized:
        #    python 2.7: return self

        h = self.bins
        if sanitize:
            h = Utils.sanitize(h)

        h = Utils.normalize(h)

        return Histogram(h, True) 

    def stat_dist(self, histogram):
        """
        If both histograms are normalized, this function calculated the sum 
        of the differences between the bins of the two histograms.
        Otherwise, throws an assertion error.
        Inputs
            histogram: second histogram for comparison
        """
        assert self.normalized and histogram.normalized
        return Utils.stat_dist(self.bins, histogram.bins)

    def l1distance(self, histogram):
        """
        First computer the sum of one bin from self and respective bin
        from histogram. Then, calculates the absolute difference of the
        two digits of this sum and sums all of the abs values for every
        bin pair.  
        Inputs
            histogram: the second histogram for comparison
        """
        return np.sum(list(map(lambda x: math.fabs(x[0] - x[1]), list(zip(self.bins, histogram.bins)))))

        # python 2.7: return np.sum(map(lambda x: math.fabs(x[0] - x[1]),zip(self.bins, histogram.bins)))

    def l2distance(self, histogram):
        """
        First computer the sum of one bin from self and respective bin
        from histogram. Then, calculates the absolute difference of the
        two digits of this sum and squares this value. Then, sums all 
        of the squared abs values for every bin pair. 
        Inputs
            histogram: the second histogram for comparison
        """
        return math.sqrt(np.sum(list(map(lambda x: (x[0] - x[1])**2, list(zip(self.bins, histogram.bins))))))
        
        # python 2.7: return math.sqrt(np.sum(map(lambda x: (x[0] - x[1])**2,zip(self.bins, histogram.bins))))

    def kl_div(self, histogram):
        """
        If both of the histograms are normalized, calculates
        the sum of all bins in self that have value > 0. Before
        summing the values multiples each value by the log of 
        (self[i]/histogram[i]).
        Otherwise, throws an assertion error.
        Inputs
            histogram: the second histogram from comparison
        """
        assert self.normalized and histogram.normalized
        return Utils.KL_div(self.bins, histogram.bins) 

    def __repr__(self):
        """
        Returns a string representation of the object
        """
        return self.bins.__repr__()

    def __len__(self):
        """
        Returns the number of bins in a histogram
        """
        return self.bins.__len__()

