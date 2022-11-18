
def textpurger(filename):
    with open (filename,"r", encoding = "utf-8") as f:
        tagInputSTR = f.read()
        tagInputSTR = tagInputSTR.replace(" ", "").replace("&gt","").replace("&lt","").replace("<s>","").replace("</s>","")
    return tagInputSTR
