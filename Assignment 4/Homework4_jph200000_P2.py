import os
import pickle

import nltk
from nltk import word_tokenize
from nltk.util import ngrams

def find_accuracy(filepath, filepath2):
    file = open(os.path.join(os.getcwd(), filepath), 'r')
    file2 = open(os.path.join(os.getcwd(), filepath2), 'r')

    total = 0
    correct = 0
    incorrect = list()

    while True:
        line1 = file.readline()
        line2 = file2.readline()
        total += 1


        if not line1:
            break

        if line1 == line2:
            correct += 1
        else:
            incorrect.append(line1.split()[0])

    file.close()
    file2.close()

    acc = correct / total

    print("accuracy %.2f" % acc)
    print("incorrect line numbers", incorrect)

def find_most_likely(filepath, u_eng, b_eng, u_fre, b_fre, u_ita, b_ita):
     with open(os.path.join(os.getcwd(), filepath), 'r') as file:
        
        count = 1

        with open('results.txt', 'w') as f:
            for sentence in file:
                most_likely = get_lang(sentence, u_eng, b_eng, u_fre, b_fre, u_ita, b_ita)
                f.write(str(count) + " " + most_likely + "\n")
                count += 1

def get_lang(sentence, u_eng, b_eng, u_fre, b_fre, u_ita, b_ita):
     eng = compute_prob(sentence, u_eng, b_eng, len(u_eng), len(b_eng))
     fre = compute_prob(sentence, u_fre, b_fre, len(u_fre), len(b_fre))
     ita = compute_prob(sentence, u_ita, b_ita, len(u_ita), len(b_ita))

     biggest = max(eng, fre, ita)

     if eng == biggest:
        return "English"
     elif fre == biggest:
        return "French"
     else:
         return "Italian"


def compute_prob(text, unigram_dict, bigram_dict, N, V):
    # N is the number of tokens in the training data
    # V is the vocabulary size in the training data (unique tokens)

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    
    p_laplace = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace

if __name__ == '__main__':

        # read the pickle files
        unidict_eng = pickle.load(open('unidict_eng.p', 'rb'))  # read binary
        bidict_eng = pickle.load(open('bidict_eng.p', 'rb'))  # read binary


        # read the pickle files
        unidict_fre = pickle.load(open('unidict_fre.p', 'rb'))  # read binary
        bidict_fre = pickle.load(open('bidict_fre.p', 'rb'))  # read binary

        # read the pickle files
        unidict_ita = pickle.load(open('unidict_ita.p', 'rb'))  # read binary
        bidict_ita = pickle.load(open('bidict_ita.p', 'rb'))  # read binary

        find_most_likely("data/LangId.test", unidict_eng, bidict_eng, unidict_fre, bidict_fre, unidict_ita, bidict_ita)
        find_accuracy("data/LangId.sol", "results.txt")