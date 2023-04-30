import nltk
from nltk import sent_tokenize

file_list = ['LifeBlood and its Implications.txt', 'Collab HK lore analysis.txt', 'The Vessels.txt', "King's Pass tablets.txt", 'Spells.txt', 'Unn_ The Greenmother.txt', 'Godmaster lore analysis.txt', 'Seals and Shields.txt', 'Charms.txt', 'Weapons of Hallownest.txt', 'Focus.txt', 'Sapience (Hollow Knight).txt', 'Relations of Crystals within Crystal Peak and Soul.txt', 'Trilobite Statue.txt', 'Quirrel’s fate.txt', 'Zote the Mighty Overview.txt', 'The Snail Shamans.txt', 'The Void.txt', 'The Stages of Infection.txt', 'Masks of Hallownest.txt', 'Kingsoul and Void Heart.txt', 'Stasis Theroy.txt', 'Path of Pain analysis.txt', 'Hornet is not made of Void.txt', 'The Dream Realm.txt', 'What defines a "God"?.txt', 'Mantis Tribe Lore.txt', "The Hunter's Origins.txt", 'Mind In A Vessel.txt', 'Grubs.txt', "Wyrm's foresight.txt", 'The Grimm Troupe_ Revised.txt', "The Shade respawn system and why it doesn't check out.txt", 'Theory on The Collector.txt']


for file in file_list:
    with open('Resources/' + file, "r") as f:
        sentences = f.read()
        
        tokens = sent_tokenize(sentences)

        output = file

        with open('Resources/' + output, 'w') as o:
            for tok in tokens:
                if tok:
                    o.write(tok.strip().lower() + "\n")