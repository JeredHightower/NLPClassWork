import pickle
import os

import nltk
from nltk import word_tokenize
from nltk.util import ngrams

def method1(filepath):

    with open(os.path.join(os.getcwd(), filepath), 'r') as file:

        # Read text file and tokenize to find lexical diversity
        sentences = file.read()

        unigrams = word_tokenize(sentences)

        bigrams = list(ngrams(unigrams, 2))

        unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}

        bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

        return unigram_dict, bigram_dict

if __name__ == '__main__':
        values = method1("data/LangId.train.English")

        unigram_dict = values[0]
        bigram_dict = values[1]

        # save the pickle files
        pickle.dump(unigram_dict, open('unidict_eng.p', 'wb'))  # write binary
        pickle.dump(bigram_dict, open('bidict_eng.p', 'wb'))  # write binary


        values = method1("data/LangId.train.French")

        unigram_dict = values[0]
        bigram_dict = values[1]

        # save the pickle files
        pickle.dump(unigram_dict, open('unidict_fre.p', 'wb'))  # write binary
        pickle.dump(bigram_dict, open('bidict_fre.p', 'wb'))  # write binary


        values = method1("data/LangId.train.Italian")

        unigram_dict = values[0]
        bigram_dict = values[1]

        # save the pickle files
        pickle.dump(unigram_dict, open('unidict_ita.p', 'wb'))  # write binary
        pickle.dump(bigram_dict, open('bidict_ita.p', 'wb'))  # write binary