import Sanitizer
from Reconstruction import *
import os
import sys
sys.path.append(os.path.abspath("n-gram_sanitizer"))
from lib import NGramSetEdited as NGramSet
import argparse

# This is the entry point
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process inputs')
    parser.add_argument('epsilon', type=float, help='Epsilon')
    parser.add_argument('n_max', type=int, help='N Max')
    parser.add_argument('l_max', type=int, help='L Max')
    parser.add_argument('dataset', type=str, help='Dataset')

    args = parser.parse_args()

    # Input parameters
    epsilon = args.epsilon
    n_max = args.n_max
    l_max = args.l_max
    dataset = args.dataset

    # You can run the program as:
    # python3 kth_analysis.py 5 8 20 "kth_og_analysis/03-03-1"

    # Count original 20 grams; l_max 20, n_max 20; Output to 
    # og_ngram_set = NGramSet.NGramSet(l_max, n_max)
    # og_ngram_set.load_dataset(dataset + ".dat", dataset + "-original-20grams.dat")

    # Load the dataset again; l_max 20, n_max 5
    ngram_set = NGramSet.NGramSet(l_max, n_max)
    ngram_set.load_dataset(dataset + ".dat", dataset + "-original-epsilon_" + str(epsilon) + '-'+ str(n_max) + "grams.dat")

    # Sanitize the dataset
    ngram_set = Sanitizer.ngram(ngram_set, n_max, budget=epsilon, sensitivity=l_max)

    # Reconstruction
    factory = Reconstruction(ngram_set, 20) 
    # Reconstruct longer grams from shorter ones using the Markov approach
    factory.extend()
    factory.reconstruct(dataset + "-reconstructed.dat")

    dataset += "-reconstructed"

    # Count constructed 20 grams; l_max 20, n_max 20; Output to 
    ngram_set = NGramSet.NGramSet(l_max, n_max)
    ngram_set.load_dataset(dataset + ".dat", dataset + '-epsilon_' + str(epsilon) + '-' + str(n_max) +"grams.dat")

    # Delete files
    if os.path.isfile(dataset + '.dat'):
        os.remove(dataset + '.dat')

    

