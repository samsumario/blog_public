#正規表現##############################################################
import re
word = "<<IOÍúáñ;"
#アルファベット&アクセント符号付きアルファベットの取得
result1 = re.findall(r"[^\W]+", word, re.UNICODE)
#記号文字のみ取得
result2 = re.findall(r"[^\w]+", word, re.UNICODE)

#文字操作##############################################################
word = "IOÍúáñar"
#小文字化
result3 = word.lower()
#OをBに変える
result4 = word.replace("O","B")
#末尾の2文字を取り出す
word[-2::]  #"ar","er","ir","se"

#リスト・辞書##########################################################
#辞書のvalueからkeyを取り出す
myDictionary = {"a":1, "b":2}
keys = [k for k, v in myDictionary.items() if v == "1"]
#リストの重複を消す
mylist = ["a","a","b"]
unique = list(set(mylist)))
#リスト内の最大値(文字列の場合は長さの最大値)
max_value = max(mylist)
#リスト内の最大値のインデックス取得
mylist = mylist.index(max(mylist))
#下記のリストでは文字列の長さの最大値が取り出せなかったので、
#各要素をlenで入れ直した
my_test_list = [' to try ', ' to try\t', ' to try, attempt',\
                 ' try', ' to try, attempt', ' to try, attempt']

#ファイル##############################################################
#utf-8のエンコードでファイルを開く
with open("test.txt", mode="r", encoding="utf_8") as f:
    #1行ごとにリストで取得
    line_list = f.readlines()
    #文字列全部取得
    all_text = f.read()


