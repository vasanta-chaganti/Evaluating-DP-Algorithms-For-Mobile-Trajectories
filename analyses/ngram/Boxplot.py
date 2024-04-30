'''
Generates 100 rounds of data for each epsilon
'''

import Sanitizer
from Reconstruction import *
import os
import sys
sys.path.append(os.path.abspath("lib"))
from lib import NGramSet

if __name__ == "__main__":

# Input parameters
    epsilons = [0.1, 1, 5, 10, 20, 50]
    n_max = 5
    l_max = 5
    dataset = "input/small_example"
    output = 'output/small_example'

    # For each epsilon value
    for epsilon in epsilons:
        # For each round
        for i in range(1,101):

            file_id = "-eps_" + str(epsilon) + "-round_" + str(i)
            
            # Decomposing data
            ngram_set = NGramSet.NGramSet(int(l_max), n_max)
            ngram_set.load_dataset(dataset + ".dat", dataset + "-original-" + str(n_max) + "grams.dat")

            # Get noisy counts
            ngram_set = Sanitizer.ngram(ngram_set, n_max, budget=epsilon, sensitivity=l_max) 
            ngram_set.dump_bp(output + file_id + ".dat")