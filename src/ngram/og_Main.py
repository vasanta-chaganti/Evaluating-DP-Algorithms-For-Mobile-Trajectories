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
    """
    Given a dataset, 1) creates variable length ngrams, 2) creates extended version of the ngrams,
    3) reconstructs the synthetic database.
    Inputs
        epsilon: the privacy loss budget parameter
        n_max: The max length of ngrams
        l_max: the max number of previous steps we consider in the Markov model
        dataset: the original dataset
    Outputs
        -original-grams.dat: the original set of variable len ngrams
        -extended.dat: the extended set of ngrams
        -reconstructed.dat: the reconstructed synthetic database from the extended database
    """

    # Input parameters
    epsilon = 10
    n_max = 20
    l_max = 20
    # OG DATASET: dataset = "input/msnbc-noisy-n_max_5-l_max_20-eps_0.1-reconstructed"
    dataset = "/home/zyuan1/research/KTH-traces/Ziming/fall23/231117/data/kth_dropped_aps"

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
        

