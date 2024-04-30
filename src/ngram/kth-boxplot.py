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
    epsilons = [0.1, 1, 5, 10]
    n_max = 5
    l_max = 20
    dataset = "/home/zyuan1/research/KTH-traces/KTH_data/kth_ngram_others/03-03"
    output = '/home/zyuan1/research/KTH-traces/KTH_data/kth_ngram_others/output/03-03'

    # For each epsilon value
    for epsilon in epsilons:
        # For each round
        for i in range(1,101):

            file_id = "-eps_" + str(epsilon) + "-round_" + str(i)
            
            # Decomposing data - obtain the -original-5grams.dat file
            ngram_set = NGramSet.NGramSet(int(l_max), n_max)
            ngram_set.load_dataset(dataset + ".dat", dataset + "-original-" + str(n_max) + "grams.dat")

            # Get noisy counts
            ngram_set = Sanitizer.ngram(ngram_set, n_max, budget=epsilon, sensitivity=l_max) 
            ngram_set.dump_dp(output + file_id + ".dat")
            # dump_dp write the first line as Seq:Counts instead of number of counts for boxplot analysis
             