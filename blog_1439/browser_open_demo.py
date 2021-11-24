import webbrowser

search_list = ["buscar", "hacer"]
#chromeで開く場合はexeファイルのパスを指定
chrome = webbrowser.get('"c:\\program files\\Google\\Chrome\\Application\\chrome.exe" %s')

for word in search_list:
    spanishdict_trans = "https://www.spanishdict.com/translate/" + word
    spanishdict_conju = "https://www.spanishdict.com/conjugate/" + word
    DEL = "https://dle.rae.es/" + word +"?m=form"

    chrome.open(spanishdict_trans)
    chrome.open(spanishdict_conju)
    chrome.open(DEL)

#デフォルトで指定されているブラウザで開く場合(windowsだとIE)
#url = "~~~.co.jp"
#webbrowser.open(url)