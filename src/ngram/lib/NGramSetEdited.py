'''
This module does sequence parsing,
stores and writes the n-gram set 
to file.

@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Viktoriia Z., Ziming Y., Koyo A.
'''

'''
From Python 2 to 3:
    Update the print statements to use parentheses.
    Replace the use of file as a variable name with a different name, as file is a built-in function in Python 3.
    Replace the use of unichr with chr for Python 3 compatibility.
    Update the function calls to map, filter, and sorted to explicitly convert them into lists.
    Update the import statements to import modules, classes, or functions explicitly.
'''


import ngram
import os
import sys
sys.path.append(os.path.abspath("lib"))
from Utils import strToSeq 
from collections import Counter
from ProgressBar import MyProgressBar
from functools import cmp_to_key

def compare_grams(x, y):
    """
    Compares the length of 2 n-grams. If they are equal in length,
    compares their values. Else, returns their length difference.
    """
    """
    python2.7:
    if len(x) == len(y):
        #return cmp(x, y)
        if x < y:
            return -1
        if x == y:
            return 0
        if x > y:
            return 1
        
    return len(x) - len(y)
    """
    if len(x) == len(y):
        return (x > y) - (x < y)
    return len(x) - len(y)

class NGramSet(Counter):
    """
    Creates an NGram set
    """
    def __init__(self, max_len, N_max = 5):
        #Counter.__init__(self) - py2
        super().__init__()
        self.N_max = N_max
        self.alphabet_size = 0
        self.max_len = max_len
        self.all_record_num = 0
        self.TERM = 0

    def load_dataset(self, in_file, dump_file):
        """
        :param in_file: file with raw data
        :param dump_file: file to dump ngrams into
        :if ngram file doesn't exist, create one, load data from raw data file into an ngram set,
        dump the ngram set into a newly created file. If it exists, dump ngram data into it.
        """
        if not os.path.isfile(dump_file):
            # print("File " + dump_file + " does not exist!\n")
            # print("Creating " + dump_file)
            self.parse_sequences(in_file)
            self.dump(dump_file)
        else:
            self.load_dump(dump_file)
            

    def load_dump(self, filename):
        """
        :param filename: path to the dump file
        :loads items from the files into the ngram set and sets the alphabet size
        """
        # python 2.7: file = open(filename)
        with open(filename) as file:
            # count = file.readline().strip() #skips the first line with word "counts". comment out if necessary
            ngram_num = int(file.readline().strip())
            # python 2.7: self.alphabet_size = int(file.readline().strip())

            # print("NGrams: ", ngram_num)
            # print("Loading NGram file (%s, N=%d)..." % (filename, self.N_max))

            # pbar = MyProgressBar('Loading dump', ngram_num)

            for line_num, line in enumerate(file):
                parts = line.strip().partition(':')
                tokens = parts[0].strip().split()
                ### NOTE: it is needed only if the file contains longer grams than N_max!!!!
                #if len(seq) > self.N_max:
                #    continue
                #####self[strToSeq(seq)] = float(parts[2].strip()) 
                # self[strToSeq(tokens)] = float(parts[2].strip())
                # og: self[strToSeq(tokens, dec=1)] = float(parts[2].strip())
                self[strToSeq(tokens, dec=1)] = float(parts[2].strip())

                max_item = max(map(int, tokens)) - 1
                if self.alphabet_size < max_item:
                    self.alphabet_size = max_item

                # pbar.update(line_num + 1)

            # pbar.finish()

        self.TERM = self.alphabet_size 

        # print("Alphabet size:", self.alphabet_size)

    # we assume that locations are numbered from 1 .. max (so we decrease each
    # location id with one)
    def parse_sequences(self, filename):
        """
        :param filename: file with data to be parsed
        :parses data, gets general stats about the ngram set, updates the ngram set records, populates the set
        """
        # print("Parsing sequence file (%s, N=%d)..." % (filename, self.N_max))
        # python 2.7: file = open(filename)

        with open(filename) as file:
            self.all_record_num = 0
            lines = []
            # First we check the alphabet
            for line in file:
                if line.startswith('#') or line.startswith('//') or line.startswith('%'):
                    continue
                lines.append(line.strip().split()[:self.max_len])
                max_item = max(map(int, lines[-1]))
                if self.alphabet_size < max_item:
                    self.alphabet_size = max_item

                self.all_record_num += 1

            self.TERM = self.alphabet_size 
            # print("Alphabet size:", self.alphabet_size)
            # print("Termination code:", self.TERM)
            # print("Number of sequences:", self.all_record_num)

            # pbar = MyProgressBar('Parsing', self.all_record_num + 1)

            for record, line in enumerate(lines):
                # seq = strToSeq(line) + chr(self.TERM)
                # og: seq = strToSeq(line, dec=1) + chr(self.TERM)
                seq = strToSeq(line, dec=1) + chr(self.TERM)
                for i in range(1, self.N_max+1):
                    G = ngram.NGram(N=i)
                    self.update(G.ngrams(seq))

                # pbar.update(record + 1)
            # pbar.finish()

        # python 2.7: file.close()

    def dump(self, filename):
        """
        :param filename: filename to be created and written into
        :dumps existing Ngram set into a newly created file
        """
        # print("Creating ngram file (%s, N=%d)..." % (filename, self.N_max))

        # python 2.7: file = open(filename, 'w')
        with open(filename, 'w') as file:
            file.write(str(len(self)) + "\n")
            # python 2.7: file.write(str(self.alphabet_size) + "\n")

            # pbar = MyProgressBar('Dumping', len(self))

            # i = 0
            for gram in sorted(self.keys(), key=cmp_to_key(compare_grams)):
                ###file.write("%s : %f\n" % (" ".join(map(lambda x: str(ord(x)), gram)),self[gram]))
                ## NOTE: ord(x) + 1 should be in order to remain compatible with the input format
            
                file.write("%s : %f\n" % (" ".join(map(lambda x: str(ord(x)+1), gram)),self[gram]))
                # i += 1
                # pbar.update(i)

            # pbar.finish()
        # python 2.7 - file.close()
        # python 2.7 - pickle.dump(self.ngrams, file)


    def dump_bp(self, filename):
        print("Creating ngram file (%s, N=%d)..." % (filename, self.N_max))

        with open(filename, 'w') as file:
            file.write("Seq:Counts" + "\n")
            # python 2.7: file.write(str(self.alphabet_size) + "\n")

            pbar = MyProgressBar('Dumping', len(self))

            i = 0
            for gram in sorted(self.keys(), key=cmp_to_key(compare_grams)):
                ###file.write("%s : %f\n" % (" ".join(map(lambda x: str(ord(x)), gram)),self[gram]))
                ## NOTE: ord(x) + 1 should be in order to remain compatible with the input format
            
                file.write("%s : %f\n" % (" ".join(map(lambda x: str(ord(x)+1), gram)),self[gram]))
                i += 1
                pbar.update(i)

            pbar.finish() 

        

