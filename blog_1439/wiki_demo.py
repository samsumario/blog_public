import wikipedia as wiki

search_list = ["Fútbol", "python"]

wiki.set_lang("es")

for word in search_list:
    result = wiki.search(word)

    if not result:
        print("not found ")
    else:
        print("result list : {} ".format(result))
        print("show first hit page")
        print("-----------")
        try:
            page = wiki.page(result[0] , auto_suggest=False)
            print("page url : " + page.url)
            print("page title : " + page.title)
            print("----- page summary -----")
            line = str(wiki.summary(result[0] , auto_suggest=False))
            print(line)

        except wiki.DisambiguationError as e:
            print("error search word")
            print(e.option)