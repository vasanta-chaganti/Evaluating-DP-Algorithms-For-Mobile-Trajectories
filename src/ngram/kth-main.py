''' 
Usage: python Main.py

Input parameters:
epsilon, n_max, l_max, dataset

@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A.
'''

import Sanitizer
from Reconstruction import *
import os
import sys
sys.path.append(os.path.abspath("lib"))
from lib import NGramSet
#from lib.NGramSet import *

# This is the entry point
if __name__ == "__main__":
    # Input parameters
    n_max = 5
    l_max = 20

    dates = ['03-03', '04-28', '09-15', '12-08']
    epsilons = [1, 5, 10, 20]
    for date in dates:
        for epsilon in epsilons:
            dataset = "/home/zyuan1/research/KTH-traces/n-gram_sanitizer/kth-output/" + date # Path to the input dataset

            print("\n*** Dataset:", dataset) 
            print("*** n_max:",n_max)
            print("*** l_max:",l_max)
            print("*** Privacy budget (epsilon):",epsilon)

            file_id = "-noisy-n_max_" + str(n_max) + "-l_max_" + str(l_max) + "-eps_" + str(epsilon)

            print("\n=== Phase 1: Decomposing input dataset to n-grams (%d <= n <= %d)\n" % (1,n_max))
            ngram_set = NGramSet.NGramSet(int(l_max), n_max)
            ngram_set.load_dataset(dataset + ".dat", dataset + "-original-" + str(n_max) + "grams.dat")

            print("\n=== Phase 2: Sanitizing n-grams\n")
            ngram_set = Sanitizer.ngram(ngram_set, n_max, budget=epsilon, sensitivity=l_max) 

            ngram_set.dump(dataset + file_id + ".dat")

            print("\n=== Phase 3: Synthetic sequential database generation from sanitized n-grams\n")
            factory = Reconstruction(ngram_set, l_max) 

            # Reconstruct longer grams from shorter ones using the Markov approach
            factory.extend()

            # Saving the extended ngramset
            factory.ngramset.dump(dataset + file_id + "-extended.dat")

            # Generating dataset
            factory.reconstruct(dataset + file_id + "-reconstructed.dat")
            

