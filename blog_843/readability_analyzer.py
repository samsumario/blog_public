import sys
import configparser

import spacy
import re
import emoji

from util import reading_time_estimator as rte
from util import fernandez
from util import szigriszt_pazos

def read_file(file_name):
    result = ""
    with open(file_name, encoding = "utf_8") as f:
        txt = f.read()
        txt = ''.join(['' if emoji.is_emoji(c) else c for c in txt])
        result = txt.replace("\n","")
    return result

def open_list(config):
    adjective_file_path = config.get("File","folder_name") +"\\"+ config.get("File","adjective")
    verb_easy_file_path = config.get("File","folder_name") +"\\"+ config.get("File","verb_easy")
    verb_plus_file_path = config.get("File","folder_name") +"\\"+ config.get("File","verb_plus")

    adjective_list = []
    with open(adjective_file_path, encoding = "utf_8", errors = "ignore") as f:
        all_txt = f.readlines()
        
        for line in all_txt:
            ad = line.split()
            adjective_list.append(ad[1])
            
            if(len(ad[3]) > 1):#for fem form
                adjective_list.append(ad[3])
    
    verb_easy_list = []
    with open(verb_easy_file_path, encoding = "utf_8", errors = "ignore") as f:
        all_txt = f.readlines()
        
        for line in all_txt:
            verb = line.split()
            v = verb[1]
            
            if v[-2::] == "se":
                v = v[:-2]
            
            verb_easy_list.append(v)

    verb_plus_list = []
    with open(verb_plus_file_path, encoding = "utf_8", errors = "ignore") as f:
        all_txt = f.readlines()
        
        for line in all_txt:
            verb = line.split()
            v = verb[1]

            if v[-2::] == "se":
                v = v[:-2]

            verb_plus_list.append(v)

    return adjective_list,verb_easy_list,verb_plus_list

def count_basic_words(txt, adj_list, verb_list, verb_p_list):
    nlp = spacy.load("es_core_news_sm")
    sentences = txt.split(".")

    total_words = []

    total_verb = 0
    listed_verb = 0
    listed_verb_p = 0

    Lem = 0
    Pres = 0
    Past = 0
    Imp = 0
    Fut = 0
    
    total_adj = 0
    listed_adj = 0

    else_verb = []
    else_adj = []

    for sentence in sentences:
        if(len(sentence) > 0):

            #clean sentence
            p = re.compile(r"[^\W]+")
            m = p.search(sentence)
            sentence = sentence[m.start():] + "."

            #tokenize spacy            
            token_list = nlp(sentence)
            
            #count loop
            for token in token_list:
                total_words.append(token.text)

                if(token.pos_ == "VERB"):
                    total_verb = total_verb + 1
                    if( token.lemma_ in verb_list ):
                        listed_verb = listed_verb + 1
                    elif( token.lemma_ in verb_p_list):
                        listed_verb_p = listed_verb_p + 1
                    else:
                        else_verb.append(token.text)
                    
                    tense = token.morph.get("Tense")
                    if(len(tense) > 0):
                        tense = tense[0]
                        if(tense == "Pres"):
                            Pres = Pres + 1
                        elif(tense == "Past"):
                            Past = Past + 1
                        elif(tense == "Imp"):
                            Imp = Imp + 1
                        elif(tense == "Fut"):
                            Fut = Fut + 1
                        else:
                            pass
                    else:
                        if(token.text == token.lemma_):
                            Lem = Lem + 1
                        else:
                            pass

                elif(token.pos_ == "ADJ"):
                    total_adj = total_adj + 1

                    if( token.lemma_ in adj_list):
                        listed_adj = listed_adj + 1
                    else:
                        else_adj.append(token.text)
                else:
                    pass

    # output result at command line
    print("---result---")
    print("total words = {}".format(len(total_words)))
    print("total verb = {}".format(total_verb))
    print("total adj = {}".format(total_adj))

    print("basic verb 380 / total verb = {} % ".format( round((listed_verb/total_verb * 100), 2)))
    print("basic verb plus 530 / total verb = {} % ".format( round((listed_verb_p/total_verb * 100), 2)))
    print("basic adj 470 / total adj = {} % ".format( round((listed_adj/total_adj * 100), 2)))
    
    print("verb tense Original = {0} % Pres = {1} % Past = {2} % Imp = {3} % Fut = {4} % ".format(\
        round((Lem/total_verb * 100), 2),round((Pres/total_verb * 100), 2), round((Past/total_verb * 100), 2),\
        round((Imp/total_verb * 100), 2), round((Fut/total_verb * 100), 2)))

    return total_words, else_verb, else_adj

def main(file_name, config):
    txt = read_file(file_name)
    adj,verb_e,verb_p = open_list(config)
    token_text_list, n_verb_list, n_adj_list = count_basic_words(txt,adj,verb_e,verb_p)
    
    reading_time = rte.count_time(token_text_list,config)
    print("reading time : {}".format(reading_time))
    
    score, judge = fernandez.fernandez_huerta(txt)
    print("Fernández score : {0} {1}".format(score, judge))

    score, judge = szigriszt_pazos.szigriszt_pazos(txt)
    print("szigriszt score : {0} {1}".format(score, judge))
    
    with open("verb_adj_list.txt", "w", encoding = "utf-8") as file:
        for verb in n_verb_list:
            file.write("verb: "+verb+"\n")
        for adj in n_adj_list:
            file.write("adj: "+adj+"\n")
        print("finish to write word list")

#command example
#python readability_analyzer.py sample.txt
if __name__ == '__main__':
    file_name = sys.argv[1]
    config = configparser.ConfigParser()
    config.read("util\conf.ini")
    main(file_name,config)