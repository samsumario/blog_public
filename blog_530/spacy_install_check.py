import sys
import spacy

def main(file_name):
    nlp = spacy.load("es_core_news_sm")
    lyrics_dic = {}

    with open("Despacito.txt", encoding="utf_8") as f:
        lyrics_list = f.readlines()

        for line in lyrics_list:
            for w in nlp(line):
                lyrics_dic.setdefault(w.lemma_,w.tag_)

    print(lyrics_dic) #for check

serach_word = sys.argv[1] #utf-8に明示キャストしないとだめかも
es = nlp(serach_word) #複数単語除け
lyrics_dic[es.lemma_] #やりたいのは存在の有無じゃなくて、センテンスを引っ張ってくること。