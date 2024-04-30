'''
Reconstructing sequential dataset from N-Grams

@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A.
'''

'''
From Python 2 to 3:
    Update the import statements to import the required modules correctly.
    Update the use of the print function to use parentheses.
    Replace the use of the keys() method on dictionaries with the list() function to convert the keys to a list explicitly.
    Update the class initialization of MyProgressBar to use the updated class name ProgressBar.
    Update the method names update and finish of MyProgressBar to update_progress and finish_progress, respectively.
    Replace the use of the cmp function to a custom comparison function using the cmp_to_key function from the functools module.
    Replace the use of the keys() method on dictionaries with the list() function to convert the keys to a list explicitly.
    Update the use of the range function to use parentheses.
    Replace the use of the dict.iterkeys() method with the dict.keys() method to iterate over keys.
    Replace the use of the dict.iteritems() method with the dict.items() method to iterate over key-value pairs.
    Replace the use of the print statement to use the print function and parentheses.
    Update the use of the Counter class to be imported directly from the collections module.
    Replace the use of the cmp function to a custom comparison function using the cmp_to_key function from the functools module.
    Replace the use of the dict.iteritems() method with the dict.items() method to iterate over key-value pairs.
    Replace the use of the cmp_to_key function with a lambda function for the comparison.
'''

import ngram
import os
import sys
sys.path.append(os.path.abspath("lib"))
from lib.ProgressBar import MyProgressBar
import math
import random as rnd
import numpy as np
import functools
from collections import defaultdict, Counter
from functools import cmp_to_key

def compare_grams(x, y):
    """
        This function compares two "grams" (could be lists, strings, or tuples) in lexicographical order 
        if they are the same length, otherwise it compares them by length.

        Parameters:
        x (Sequence): The first "gram" to compare.
        y (Sequence): The second "gram" to compare.

        Returns:
        int: -1 if x < y, 0 if x == y, 1 if x > y, or the difference in length if the lengths of x and y are not the same.
    """
    """
    Python 2.7:
        if len(x) == len(y):
        return cmp(x, y)
    """
    if len(x) == len(y):
        return (x > y) - (x < y)
    return len(x) - len(y)

class Reconstruction:

    def __init__(self, ngramset, l_max):
        """
            Constructor for the Reconstruction class.

            Parameters:
            ngramset (Dict): A dictionary representing the ngramset.
            l_max (int): Maximum length of ngram.

            Returns:
            None
        """
        self.ngramset = ngramset
        self.l_max = l_max

    # join two grams 
    def join(self, g1, g2, new_grams):
        """
            Joins two grams.

            Parameters:
            g1: The first gram.
            g2: The second gram.
            new_grams (List): A list to add the new joined gram.

            Returns:
            None
        """
        # new_count = int(float(self.ngramset[g1] * self.ngramset[g2]) / self.ngramset[g2[:-1]])
        try:
            new_count = int(float(self.ngramset[g1] * self.ngramset[g2]) / self.ngramset[g2[:-1]])
        except ZeroDivisionError:
            print("ZeroDivisionError occurred, exiting with status code 1.")
            raise SystemExit(1)
        if new_count >= 1:
            new_grams.append(g1 + g2[-1])
            self.ngramset[new_grams[-1]] = new_count 

    def create_prefix_set(self, grams):
        """
            Creates a set of prefixes.

            Parameters:
            grams (List): A list of grams.

            Returns:
            prefixes (defaultdict): A defaultdict of prefixes.
        """
        prefixes = defaultdict(set)

        for gram in self.ngramset.keys():
            prefixes[gram[:-1]].add(gram[-1])

        return prefixes

    def floor(self):
        """
            Rounds down all the ngram counts to their floor values.

            Returns:
            None
        """
        # Python 2.7: for i in self.ngramset.keys():
        for i in list(self.ngramset.keys()):
            self.ngramset[i] = int(self.ngramset[i])
            if self.ngramset[i] <= 0:
                del self.ngramset[i]

    def extend(self):
        """
            Extends the ngram set.

            Returns:
            None
        """
        max_len = 1
        max_grams = []

        self.floor()

        # This loop is to select the longest grams in a single scanning of
        # the gram set
        for i in self.ngramset.keys():
            if len(i) >= max_len:
                if len(i) > max_len:
                    max_grams = []
                    max_len = len(i)
                
                max_grams.append(i)

        # This loop is to join only the joinable longest grams (we do it until
        # there are no more grams that can be joined)
        # print("Generating longer grams...")
        while len(max_grams) > 1 and len(max_grams[0]) < self.l_max:
            new_grams = []

            # print("Num. of %d-grams: %d" % (len(max_grams[0]), len(max_grams)))

            # Creating hashmap to speed up computation (at the cost of memory)
            prefixes = self.create_prefix_set(max_grams)

            # pbar = MyProgressBar('Generating %d-grams' % (len(max_grams[0])+1), len(max_grams))

            for (i, g1) in enumerate(max_grams):
                k = g1[1:]
                if k in prefixes.keys():
                    for suffix in prefixes[k]:
                        self.join(g1, k + suffix, new_grams)

                # pbar.update(i)
                # GPT suggestion: pbar.update(i+1)

            # pbar.finish()

            max_grams = new_grams

    
    # Rounding floats to integers, and remove terminated grams for the reconstruction step
    def clean(self):
        """
            Cleans the ngramset by rounding floats to integers and removing terminated grams.

            Returns:
            None
        """
        for gram in list(self.ngramset.keys()):
            if ord(gram[-1]) == self.ngramset.TERM or self.ngramset[gram] <= 0:
                del self.ngramset[gram]


    def reconstruct(self, filename):
        """
            Reconstructs the ngramset.

            Parameters:
            filename (str): The name of the file to write the reconstructed ngram set.

            Returns:
            None
        """
        # Extracting sequences from the extended gram set
        self.clean()

        grams = sorted(self.ngramset.keys(), key=cmp_to_key(compare_grams), reverse=True)

        # pbar = MyProgressBar('Reconstructing', len(grams))

        file = open(filename, 'w')

        for (j, gram) in enumerate(grams):
            occurences = self.ngramset[gram]

            if occurences <= 0:
                del self.ngramset[gram]
                continue

            cnt = Counter()
            for i in range(1, len(gram)):
                G = ngram.NGram(N=i)
                cnt.update(G.ngrams(gram))
            
            # Optimization: we do not add the gram if its addition would
            # cause negative counts
            skip = False
            for i in cnt:
                cnt[i] *= occurences

                if self.ngramset[i] - cnt[i] < 0:
                    skip = True
                    break

            if skip:
                continue

            # Write sequence to file
            sequence = " ".join(map(lambda x: str(ord(x) + 1), gram))

            ## Input compliant:
            file.write((sequence + '\n') * occurences)
            # Compact format:
            #file.write(sequence + " : " + str(occurences) + "\n")

            self.ngramset.subtract(cnt)

            # pbar.update(j + 1)

        # pbar.finish()
        file.close()
