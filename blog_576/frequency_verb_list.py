import sys
import spacy

def save_list_data(save_file,noun_list):
    with open(save_file, "w", encoding = "utf-8") as f:
        
        for data in noun_list:
            f.write('\t'.join([str(i) for i in data]) + "\n")
        
        print("\nsave list in " + save_file)


def main(data_file, save_file):
    nlp = spacy.load("es_core_news_sm")
    result_verv_list = []
    
    with open(data_file, encoding = "utf_8", errors = "ignore") as f:
            
        frequency_word_data = f.readlines()
        read_header = False

        for line in frequency_word_data:
            if(read_header == False):
                read_header = True
            else:
                line_list = line.split("\t")
                print("\r" + "read line" + line_list[0], end="")
                
                word = line_list[1]

                if len(word) > 0:
                    result = []
                    w = nlp(word)
                
                    if(w[0].pos_ == "VERB"):
                        result.append(line_list[0].replace(" ", "").replace(".", "")) #add Order
                        result.append(w[0].lemma_) #add Noun
                        
                        if(len(w[0].morph.get("Person")) > 0):
                            result.append(w[0].morph.get("Person")[0]) #add Person analyze
                        else:
                            result.append("-")
                        
                        if(len(w[0].morph.get("Tense")) > 0):
                            result.append(w[0].morph.get("Tense")[0]) #add Tense analyze
                        else:
                            result.append("-")
                        
                        result_verv_list.append(result)
                                
    save_list_data(save_file, result_verv_list)

                    
#command example
#python frequency_verb_list.py ./word_data/10000_formas.txt ./result/verb_list.txt
if __name__ == '__main__':
    list_data = sys.argv[1]
    save_file = sys.argv[2]
    main(list_data, save_file)