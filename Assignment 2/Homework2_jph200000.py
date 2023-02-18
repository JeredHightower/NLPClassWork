import sys
import os

import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords

from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

from random import seed
from random import randint

def method1(filepath):

    with open(os.path.join(os.getcwd(), filepath), 'r') as file:

        # Read text file and tokenize to find lexical diversity
        sentences = file.read()

        tokens = word_tokenize(sentences)

        print("The lexical diversity is", f'{len(set(tokens)) / len(tokens) :.2f}')

        # Remove stopwords, lowercase tokens, only use alpha and len > 5
        stop = stopwords.words('english')
        tokens = [t.lower() for t in tokens if (t.isalpha() and len(t) > 5 and t not in stop)]

        # Lemmatize tokens
        wnl = WordNetLemmatizer()
        lemmatized = set([wnl.lemmatize(t) for t in tokens])

        tags = nltk.pos_tag(lemmatized)
        print('\ntagged tokens:\n', tags[:20])

        # Find all nouns
        nouns = [t[0] for t in tags if (t[1] == "NN" or t[1] == "NNS" or t[1] == "NNP")]

    return tokens, nouns
            
def guessing_game(top):
    seed(1234)
    txt = "begin"
    score = 5

    # Choose random word
    word = top[randint(0, 50)]

    guessed_letters = []
    word_guess = underscores(word, guessed_letters)

    # Game loop
    while True:
        print(word_guess)
        txt = input("Guess a letter: ")
        
        if txt == "!":
            print("Exiting...")
            break

        guessed_letters.append(txt)

        new_guess = underscores(word, guessed_letters)

        if word_guess == new_guess:
            score -= 1
            print("Sorry, guess again. Score is", score)
        elif new_guess == word:
            print("You solved it!")
            print(new_guess)
            print("\nCurrent score is:", score)
            print("\nGuess another word")

            word = top[randint(0, 50)]
            guessed_letters = []
            word_guess = underscores(word, guessed_letters)
        else:
            score += 1
            print("Right! Score is", score)
            word_guess = new_guess
        
        if score == 0:
            print("\nYou failed... try again")
            word = top[randint(0, 50)]
            guessed_letters = []
            word_guess = underscores(word, guessed_letters)
            score = 5

def underscores(word, guess):
    under = ""

    # show letters if guessed, otherwise show underscore
    for letter in word:
        if guess.count(letter) > 0:
            under += letter
        else:
            under += "_"
    
    return under

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        values = method1(fp)
        tokens = values[0]
        nouns = values[1]

        noun_dict = {word:tokens.count(word) for word in nouns}

        # Sort dict by count
        top = sorted(noun_dict, key=noun_dict.get, reverse=True)[:50]

        guessing_game(top)