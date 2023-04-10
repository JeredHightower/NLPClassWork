import requests
from bs4 import BeautifulSoup

from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

import math
import pickle

URL = 'https://en.wikipedia.org/wiki/The_Incredibles'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')

web_list = [URL]

sub_strings = [URL, 'wiki','archive','php', 'metacritic', 'tomatoes', 'html', 'rollingstone', 'star', 'disney', 'ign']

for p in soup.find_all('a', href=True):
    if 'https://' in p.get('href') and 'incredibles' in p.get('href') and not any(x in p.get('href') for x in sub_strings):
        web_list.append(p['href'])

file_list = []

for web in web_list:
    page = requests.get(web)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    w = web.replace('/', '') + ".txt"
    file_list.append(w)

    with open(w, 'w') as f:

        for p in soup.select('p'):
            if len(p.get_text()) > 150:
                f.write(p.get_text())

output_list = []

for file in file_list:
    with open(file, "r") as f:
        sentences = f.read()

        sentences = sentences.replace("Mr.", "Mr")
        
        tokens = sent_tokenize(sentences)

        output = "output_" + file
        output_list.append(output)

        with open(output, 'w') as o:
            for tok in tokens:
                if tok:
                    tok = tok.replace("Mr", "Mr.")
                    o.write(tok.strip() + "\n")


def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc)
    stop = stopwords.words('english')

    tokens = [w for w in tokens if w.isalpha() and w not in stop]
            
    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tf_dict = {t:tokens.count(t) for t in token_set}
    
    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
        
    return tf_dict



vocab = set()
tf_dict_list = []

for out in output_list:
    with open(out, 'r') as f:
        doc = f.read().lower().replace('\n', ' ')
        tf_dict_list.append(create_tf_dict(doc))

for keys in tf_dict_list:
    vocab = vocab.union(set(keys.keys()))

print("number of unique words:", len(vocab))


idf_dict = {}

vocab_by_topic = [keys.keys() for keys in tf_dict_list]

for term in vocab:
    temp = ['x' for voc in vocab_by_topic if term in voc]
    idf_dict[term] = math.log((1+len(vocab_by_topic)) / (1+len(temp))) 


def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t] 
        
    return tf_idf

tfidf_list = []

for tf in tf_dict_list:
    tfidf_list.append(create_tfidf(tf, idf_dict))

print("Top 3 Words in each Website:")
for d in tfidf_list:
    doc_term_weights = sorted(d.items(), key=lambda x:x[1], reverse=True)

    print(doc_term_weights[0][0])
    print(doc_term_weights[1][0])
    print(doc_term_weights[2][0])
    print()

terms = ['bob', 'edna', 'superhero', 'underminer', 'incredible', 'award', 'bird', 'fans', 'fantastic', 'million']
print("Top 10 Terms:")
print("bob")
print("edna")
print("superhero")
print("underminer")
print("incredible")
print("award")
print("bird")
print("fans")
print("fantastic")
print("million")

knowledge_base = {}

for term in terms:
    relevant = []
    for out in output_list:
        with open(out, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if term in line.lower():
                    relevant.append(line)
    
    knowledge_base[term] = relevant

# save the pickle file
pickle.dump(knowledge_base, open('knowledge_base', 'wb'))  # write binary


print(knowledge_base)