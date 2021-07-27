import sys
import shutil
import ssl
import random
import spacy
import requests
import bs4
#you need lxml for bs4

ssl._create_default_https_context = ssl._create_unverified_context

def text_to_word_list(data_file):
    nlp = spacy.load("es_core_news_sm")
    word_list = []
    escape_list = ["{","}","(",")","[","]",",","'","’","\n"," ","!","¡","¿","?",".",":","\""]
   
    with open(data_file, encoding = "utf_8") as f:
        lines = f.readlines()

        for line in lines:
            if len(line) > 0:
                for w in nlp(line):
                    
                    if w.text in escape_list:
                        pass

                    else:
                        result = []

                        if(w.pos_ == "VERB"):
                            result.append("Verb") #add Order
                            result.append(w.lemma_) #add Noun
                        
                            if(len(w.morph.get("Person")) > 0):
                                result.append(w.morph.get("Person")[0]) #add Person analyze
                            else:
                                result.append("-")
                            
                            if(len(w.morph.get("Tense")) > 0):
                                result.append(w.morph.get("Tense")[0]) #add Tense analyze
                            else:
                                result.append("-")
                        
                            word_list.append(result)
                        
                        elif(w.pos_ == "NOUN") or (w.pos_ == "PROPN"):
                            result.append("Noun") #add Order
                            result.append(w.text) #add Noun
                            result.append("-") #動詞との長さ合わせ
                            result.append("-") #動詞との長さ合わせ
                            word_list.append(result)
                        
                        else:
                            pass

    return word_list


def search_image(data):
    request = requests.get("https://www.google.com/search?hl=es&q=" + data + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
    html = request.text
    soup = bs4.BeautifulSoup(html,"lxml")
    links = soup.find_all("img")

    #検索結果ページの何個目の画像からが結果なのか分からないのでとりあえずランダムで3個取得
    links_src = []
    for i in range(0,3):
        links_src.append(random.choice(links).get("src"))

    return links_src


def save_html_data(html_file, soup):
    #write result html
    with open(html_file, "w", encoding = "utf-8") as file:
        file.write( str(soup) )
        print("\nsave file " + html_file)


def list_to_html(search_word_list, template_html):
    
    with open(template_html, mode = "rt", encoding = "utf-8") as f:
    
        soup = bs4.BeautifulSoup(f.read(), "html.parser")
        
        #table header
        tr = soup.new_tag("tr")
        
        th = soup.new_tag("th")
        th.string = "Parte del discurso"
        
        soup.find("table").append(tr)
        tr.append(th)

        td_header_list = ["Palabra","Persona","Tense","Imagen1","Imagen2","Imagen3"]
        for td_txt in td_header_list:
            td = soup.new_tag("td")
            td.string = td_txt
            tr.append(td) 

        #table content
        for data in search_word_list:
            print("\r" + "search " + data[1][0:-1], end="")
            
            tr = soup.new_tag("tr")
            
            th = soup.new_tag("th")
            th.string = data[0]

            
            soup.find("table").append(tr)
            tr.append(th)

            for idx in range(1,4):
                td = soup.new_tag("td")
                td.string = data[idx]
                tr.append(td)

            #search image
            links = search_image(data[1])
            for link in links:
                td = soup.new_tag("td")
                img = soup.new_tag("img",src=link)
                td.append(img)
                tr.append(td)
        
        return soup


def main(data_file, output_html, template_html):
    word_list = text_to_word_list(data_file)
    html = list_to_html(word_list, template_html)
    save_html_data(output_html, html)

#python sentence_to_word_table_html.py ./word_data/sample.txt ./result/word_list.html
if __name__ == '__main__':
    data_file = sys.argv[1] #解析したい文章ファイル
    output_html = sys.argv[2] #出力ファイル
    template_html = "./simple_table_html/template.html" #テンプレートファイル
    
    list_data = []
    with open(data_file, encoding="utf_8") as f:
        list_data = f.readlines()
    
    main(data_file, output_html, template_html)
