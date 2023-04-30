import math
import pickle
from nltk import word_tokenize

# Corpus
doc_list = ['LifeBlood and its Implications.txt', 'Collab HK lore analysis.txt', 'The Vessels.txt', "King's Pass tablets.txt", 'Spells.txt', 'Unn_ The Greenmother.txt', 'Godmaster lore analysis.txt', 'Seals and Shields.txt', 'Charms.txt', 'Weapons of Hallownest.txt', 'Focus.txt', 'Sapience (Hollow Knight).txt', 'Relations of Crystals within Crystal Peak and Soul.txt', 'Trilobite Statue.txt', 'Quirrel’s fate.txt', 'Zote the Mighty Overview.txt', 'The Snail Shamans.txt', 'The Void.txt', 'The Stages of Infection.txt', 'Masks of Hallownest.txt', 'Kingsoul and Void Heart.txt', 'Stasis Theroy.txt', 'Path of Pain analysis.txt', 'Hornet is not made of Void.txt', 'The Dream Realm.txt', 'What defines a "God"?.txt', 'Mantis Tribe Lore.txt', "The Hunter's Origins.txt", 'Mind In A Vessel.txt', 'Grubs.txt', "Wyrm's foresight.txt", 'The Grimm Troupe_ Revised.txt', "The Shade respawn system and why it doesn't check out.txt", 'Theory on The Collector.txt']

# Term Frequency Creation
def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc)

    stop = []

    with open("Resources/stopwords-en.txt", "r") as file:
        content = file.read()
        stop = content.split("\n")

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
for doc in doc_list:
    with open("Resources/" + doc, encoding="utf8", errors='ignore') as f:
        d = f.read().lower().replace('\n', ' ')
        tf_dict_list.append(create_tf_dict(d))

for keys in tf_dict_list:
    vocab = vocab.union(set(keys.keys()))

print("number of unique words:", len(vocab))
#with open("Resources/ignore.txt", 'w') as f:
    #for word in vocab:
        #f.write(word + "\n")



# Idf
idf_dict = {}

vocab_by_topic = [keys.keys() for keys in tf_dict_list]

for term in vocab:
    temp = ['x' for voc in vocab_by_topic if term in voc]
    idf_dict[term] = math.log((1+len(vocab_by_topic)) / (1+len(temp))) 

# Tf Idf creation
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        if(tf[t] * idf[t] > .005):
            tf_idf[t] = tf[t] * idf[t]

    return tf_idf

tfidf_list = []

for tf in tf_dict_list:
    tfidf_list.append(create_tfidf(tf, idf_dict))

## Fix Plural Words
for d in tfidf_list:
    delete_list = []
    for key in d.keys():
        if key != "us":
            if (key + "s") in d.keys():
                d[key] = d.get(key) + d.get(key + "s")
                delete_list.append(key + "s")
            elif (key + "es") in d.keys():
                d[key] = d.get(key) + d.get(key + "es")
                delete_list.append(key + "es")
    
    for l in delete_list:
        d.pop(l)
        
# save the pickle file
pickle.dump(tfidf_list, open('tfidf_list', 'wb'))  # write binary