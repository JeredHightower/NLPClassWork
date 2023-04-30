# A chatbot designed to answer questions regarding Hollow Knight lore
import pickle
import gradio as gr
import openai

import spacy
import en_core_web_sm

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

openai.api_key = "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"

def findRelevantDocument(list_of_words, doc_list, tfidf_list):
    ## find document with highest tfidf containing word
    word_in_doc_list = {}
    for i in range(len(doc_list)):
        word_in_doc_list[doc_list[i]] = 0

    for word in list_of_words:
        for i in range(len(doc_list)):
            found_value = tfidf_list[i].get(word.lower())

            if found_value != None:
                word_in_doc_list[doc_list[i]] = found_value + word_in_doc_list.get(doc_list[i])

        s = sorted(word_in_doc_list.items(), key=lambda x:x[1], reverse=True)

        if s[0][1] == 0:
            return []
        elif s[1][1] > 0:
            return [s[0][0], s[1][0]]
        else:
            return [s[0][0]]

def getNouns(sentence):
    spacy_model = en_core_web_sm.load()

    doc = spacy_model(sentence)

    return [token.lemma_ for token in doc if token.pos_ == "NOUN"] + [entity.text for entity in doc.ents]

def getName(sentence):
    spacy_model = en_core_web_sm.load()

    doc = spacy_model(sentence)

    return [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

def getTopic(input):
    input = input.lower()

    noun_list = getNouns(input)

    list_of_words = []

    if noun_list:
        list_of_words = noun_list
    else:
        stop = []

        with open("Resources/stopwords-en.txt", "r") as file:
            content = file.read()
            stop = content.split("\n")

        list_of_words = word_tokenize(input)
        list_of_words = [w for w in list_of_words if w.isalpha() and w not in stop]
    
    return " ".join(list_of_words)


def getCorpusInfo(input):
    ## Corpus List
    doc_list = ['LifeBlood and its Implications.txt', 'Collab HK lore analysis.txt', 'The Vessels.txt', "King's Pass tablets.txt", 'Spells.txt', 'Unn_ The Greenmother.txt', 'Godmaster lore analysis.txt', 'Seals and Shields.txt', 'Charms.txt', 'Weapons of Hallownest.txt', 'Focus.txt', 'Sapience (Hollow Knight).txt', 'Relations of Crystals within Crystal Peak and Soul.txt', 'Trilobite Statue.txt', 'Quirrel’s fate.txt', 'Zote the Mighty Overview.txt', 'The Snail Shamans.txt', 'The Void.txt', 'The Stages of Infection.txt', 'Masks of Hallownest.txt', 'Kingsoul and Void Heart.txt', 'Stasis Theroy.txt', 'Path of Pain analysis.txt', 'Hornet is not made of Void.txt', 'The Dream Realm.txt', 'What defines a "God"?.txt', 'Mantis Tribe Lore.txt', "The Hunter's Origins.txt", 'Mind In A Vessel.txt', 'Grubs.txt', "Wyrm's foresight.txt", 'The Grimm Troupe_ Revised.txt', "The Shade respawn system and why it doesn't check out.txt", 'Theory on The Collector.txt']
    ## read pickle file
    tfidf_list = pickle.load(open('tfidf_list', 'rb'))  # read binary


    ## MAKE SURE TO LOWERCASE INPUT
    input = input.lower()

    noun_list = getNouns(input)

    list_of_words = []

    if noun_list:
        list_of_words = noun_list
    else:
        stop = []

        with open("Resources/stopwords-en.txt", "r") as file:
            content = file.read()
            stop = content.split("\n")

        list_of_words = word_tokenize(input)
        list_of_words = [w for w in list_of_words if w.isalpha() and w not in stop]


    ## Words used to search documents
    print(list_of_words)

    rel_docs = findRelevantDocument(list_of_words, doc_list, tfidf_list)

    relevant_sentences = []
    if rel_docs:
        for rel_doc in rel_docs:
            with open('Resources/' + rel_doc, "r") as f:
                sentences = f.read()
                tokens = sent_tokenize(sentences)

                for x in range(len(tokens)):
                    if any(word in tokens[x] for word in list_of_words):    
                        relevant_sentences.append(tokens[x].replace('\n', ' '))

                        if(x+2 < len(tokens) - 1):
                            relevant_sentences.append(tokens[x+1].replace('\n', ' '))
                            relevant_sentences.append(tokens[x+2].replace('\n', ' '))
    else:
        print('No available response')

    relevant_sentences = list(dict.fromkeys(relevant_sentences))
    
    return relevant_sentences


role = "You are a Hollow Knight Expert, Do not answer anything other than Hollow Knight related queries unless it's about the user. "

name = ""
last_topic = ""
got_name = False

user_dict = pickle.load(open('user_dict', 'rb'))  # read binary
print(user_dict)

def chatbot(input):
    global name
    global last_topic
    global got_name
    global user_dict

    ignore_relevant = False

    input = input.lower()

    intro = 'Using the information below, summarize it in your own words to give a short answer to the following: '
    info = '\n'.join(getCorpusInfo(input))

    context = word_tokenize(info)[0:3000]
    info = " ".join(context)

    name_prompt = ""
    name_remark = ""
    if name:
        name_prompt = "My name is " + name + " "
        name_remark = "\nWhat else would you like to know " + name + "?"

    if input:
        messages = []

        if info:
            messages = [({"role": "user", "content": name_prompt + role + intro + input + info})]
            
            if got_name:
                # Save user information
                last_topic = getTopic(input)

                if last_topic:
                    user_dict[name] = last_topic
                else:
                    user_dict[name] = input
                # save the pickle file
                pickle.dump(user_dict, open('user_dict', 'wb'))  # write binary

                print(user_dict)

        else:
            messages = [({"role": "user", "content": name_prompt + role + input})]

            ignore_relevant = True
            
            if getName(input) and not got_name:
                name = getName(input)[0]
                got_name = True

                ## I see you were interested in [topic last time]
                # check if name exist and talk about last topic
                if name not in user_dict:
                    messages = [({"role": "user", "content": 'Say hi to ' + name})]
                else:
                    messages = [({"role": "user", "content": 'Say welcome back to ' + name + ' and say we talked about ' + user_dict[name] + ' from Hollow Knight last time'})]
        
        print(messages[0])

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=200)
        reply = chat.choices[0].message.content

        relevant = ""

        stop = []

        with open("Resources/stopwords-en.txt", "r") as file:
            content = file.read()
            stop = content.split("\n")

        list_of_words = word_tokenize(input)
        list_of_words = [w.lower() for w in list_of_words if w.isalpha() and w not in stop]

        tokens = sent_tokenize(reply)
        for tok in tokens:
            if any(word in tok.lower() for word in list_of_words):
                relevant += tok + " "

        # messages.append({"role": "assistant", "content": relevant})
        if relevant and not ignore_relevant:
            return relevant + name_remark
        
        return reply + name_remark

inputs = gr.inputs.Textbox(lines=7, label="Chat with HollowBot")
outputs = gr.outputs.Textbox(label="Reply")

gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="Hollow Knight LoreBot",
             description="Ask anything you want about Hollow Knight Characters and Lore",
             theme="compact").launch(share=True)