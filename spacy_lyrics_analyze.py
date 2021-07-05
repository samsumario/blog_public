import sys
import glob
import json
import spacy
import matplotlib.pyplot as plt

def main(folder,save_file):
    nlp = spacy.load("es_core_news_sm")
    lyrics_word_dic = {}
    escape_list = ["{","}","(",")","[","]",",","'","’","\n"," ","!","¡","¿","?",".",":","\""]

    lyrics_files = glob.glob(folder+"/*.txt")

    for lyrics_file in lyrics_files:
        with open(lyrics_file, encoding="utf_8") as f:
            lyrics_list = f.readlines()

            for line in lyrics_list:
                if len(line) > 0:
                    for w in nlp(line):
                        
                        if w.text in escape_list:
                            pass
                        else:
                            lyrics_word_dic.setdefault(w.lemma_,[w.text]).append(w.text)
                            
    lyrics_word_sort_list = sorted(lyrics_word_dic.items(), key=lambda x:len(x[1]), reverse=True)
    show_frequency_graph(lyrics_word_sort_list)
    
    with open(save_file, 'w', encoding="utf-8") as f:
        for data in lyrics_word_sort_list:
            f.write("total : "+str(len(data[1])-1) + " times / " + "conjugation " + str(len(set(data[1]))) +" : " + str(data)+"\n")

def show_frequency_graph(lyrics_list):
    x = []
    y_total = []
    y_conj = []

    for idx,data in enumerate(lyrics_list):
        y_total.append(len(data[1])-1)
        y_conj.append(len(set(data[1])))
        x.append(idx)
    
    fig = plt.figure()
    plt.plot(x, y_total, label="total_num")
    plt.plot(x, y_conj, label="conj_num")
    plt.legend()
    plt.show()

#command example
#python ./test result.txt
if __name__ == '__main__':
    base_folder = sys.argv[1]
    save_file = sys.argv[2]
    main(base_folder,save_file)