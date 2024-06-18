[source code](https://www.crysys.hu/~acs/)

- DEPENDENCIES:
  numpy, bitarray, progressbar, ngram

- DESCRIPTION:
  These python scripts implement a differentially private sequential data
  sanitizer based on variable length n-grams. For more information, please
  refer to [1] which contains the full description of the implemented scheme.

- INPUT:

* dataset: name of the text file containing the sequential dataset, where lines
  correspond to distinct sequences drawn from a common alphabet. The alphabet
  MUST be integers in the range of [1,65534] (see input/msnbc.dat for an example)
* n_max: maximum depth of the exploration tree (i.e., maximal gram length)
* budget: privacy budget (epsilon)
* sensitivity: (l_max) the truncation size; each input sequence is truncated
  to the specified size before its n-gram decomposition

- OUTPUT:
  1.) sanitized (variable length) n-gram set of the (truncated) dataset, where

* the first line is the number of released grams
* the second line is the size of the alphabet
* all subsequent line corresponds to one gram and its noisy occurance count. The
  termination symbol is the number len(alphabet)+1. The name of the generated
  output file is "<dataset>-noisy-n*max*<n*max>-l_max*<sensitivity>-eps\_<budget>.dat"
  The maximum size of grams in this output is n_max.

  2.) Set of extended sanitized grams. This includes grams having size larger than
  n_max. This output can be used to frequent sequential pattern mining.

  3.) Synthetic dataset reconstructed from the sanitized set of n-grams.
  This output can be used to further analyses such as count queries.

The script first creates the set of all (non-noisy) n-grams up to size n*max by
parsing the dataset, and writes this set to a file a file named
"<dataset>*<n_max>grams.dat". This file will not be deleted, and is used in
subsequent executions to access the original (non-noisy) n-gram set. This
enables to speed up the sanitization as the parsing process (creation of all
n-grams) is slow.
Afterwards, it generates the sanitized (noisy) grams up to size n_max, which is
then used to approximate longer grams using the Markov approximation.

The synthetic database reconstruction mechanism (Output 2 and 3) are detailed
in Section 4.3.5 [1], while the n-gram sanitization (Output 1) is contained by
Sanitizer.py.

[1] R. Chen, G. Acs, C. Castelluccia Differentially Private Sequential Data
Publication via Variable-Length N-Grams In 19th ACM Conference on Computer and
Communications Security (CCS), 2012.

@author: Gergely Acs <acs@crysys.hu>
