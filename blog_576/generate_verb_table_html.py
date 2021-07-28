import sys
import shutil
import ssl
import random
import requests
import bs4
#you need lxml for bs4

ssl._create_default_https_context = ssl._create_unverified_context

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


def main(search_word_list, html_file, template_file):
    
    with open(template_file, mode = "rt", encoding = "utf-8") as f:
    
        soup = bs4.BeautifulSoup(f.read(), "html.parser")
        
        #table header
        tr = soup.new_tag("tr")
        
        th = soup.new_tag("th")
        th.string = "Orden"
        
        soup.find("table").append(tr)
        tr.append(th)

        td_header_list = ["Palabra","Persona","Tense","Imagen1","Imagen2","Imagen3"]
        for td_txt in td_header_list:
            td = soup.new_tag("td")
            td.string = td_txt
            tr.append(td) 

        #table content
        for data in search_word_list:
            data = data.split("\t")
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
        
        save_html_data(html_file, soup)

#command example
#python generate_verb_table_html.py ./result/verb_list.txt ./result/verb_list.html
if __name__ == '__main__':
    data_file = sys.argv[1] #単語帳のファイル
    write_html = sys.argv[2] #出力ファイル
    template_html = "./simple_table_html/template.html" #テンプレートファイル
    
    list_data = []
    with open(data_file, encoding="utf_8") as f:
        list_data = f.readlines()
    
    main(list_data[0:100], write_html, template_html)
