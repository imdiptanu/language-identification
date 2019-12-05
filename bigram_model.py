"""
Description: Bigram model for Language identification
Authors: Diptanu Sarkar, ds9297@rit.edu, Saral Nyathawada, sn5409@rit.edu
"""

# Importing python3 libraries for the project
import codecs
from nltk.collocations import BigramCollocationFinder
import math
import numpy as np
import csv

def main():
    #Filename for training the data
    filename = "wiki_data_10Kwords_allURLs.csv"

    #Dictionary to store the data
    data_dict = {}

    #Read the file line by line
    with codecs.open(filename,"r","utf-8") as f:

        #Read and ignore the header
        reader = csv.reader(f)
        next(reader)

        #For each language append the respective data
        for line in reader:
            language = line[1]
            if language in data_dict:
                data_dict[language].append(line[0])
            else:
                if language is "":
                    continue
            data_dict[language] = []

    #For each language get a character sequence list
    for lang in data_dict:

        text_corpus = "".join(data_dict[lang])
        char_sequence = []
        for char in text_corpus:
            char_sequence.append(char)

        #Use BigramCollocationFinder from nltk
        finder = BigramCollocationFinder.from_words(char_sequence)

        #Ignore bigrams which occur less than 5 times
        finder.apply_freq_filter(5)

        #Sort the model
        bigram_model = sorted(finder.ngram_fd.items(), key=lambda item: item[1], reverse=True)

        #Save the model
        np.save(lang+".npy",bigram_model)



# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()