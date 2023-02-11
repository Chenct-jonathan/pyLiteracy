#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from flask import Flask
from flask import render_template

#from Gua_Zai import Gua_Zai.execLoki

app = Flask(__name__)

@app.route("/")
def test():
    return render_template("template/homepage.html")

if __name__ == "__main__":
    app.run(debug=True)