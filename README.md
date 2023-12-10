# [PyLiteracy: A Linguistics-Based Mandarin Grammar Checker](https://github.com/Chenct-jonathan/pyLiteracy)

無論是否為母語者，在繁體中文的使用上，諸如近義詞、錯別字的錯誤使用是常見的，此問題也間接導致訓練資料多來自網路的大型語言模型 (LLM)無法在中文文法檢查任務上扮演可靠的角色。然而從語言學的角度來看，僅針對正確及錯誤句的對照進行模型訓練並非最有效的方式，其實此類型錯誤與詞類和句型結構有著直接關係，若將正確的詞類及句型結構規則分析化簡之後以程式碼撰寫成模型，此類以語言學規則為本的模型即能以和人類兒童依類似方式掌握語言的使用，實現以少量語料完成高效率中文文法檢查的任務。

檔案總覽
-------------
```
│  pyLiteracy.py
│  pyproject.toml
│  README.md
│  
├─dist
│      pyLiteracy-0.0.1-py3-none-any.whl
│      pyLiteracy-0.0.1.tar.gz
│      
├─pyLiteracy
│  │  pyLiteracy.py
│  │  __init__.py
│  │  
│  ├─discord_bot
│  │      pyLiteracy_discord.py
│  │      
│  ├─loki_models
│  │  │  __init__.py
│  │  │  
│  │  ├─bing_jian_zhi
│  │  │  │  bing_jian_zhi.py
│  │  │  │  
│  │  │  └─intent
│  │  │          Loki_human_bing.py
│  │  │          Updater.py
│  │  │          USER_DEFINED.json
│  │  │          
│  │  ├─Gua_Zai
│  │  │  │  Gua_Zai.py
│  │  │  │  utteranceChecker.py
│  │  │  │  __init__.py
│  │  │  │  
│  │  │  ├─intent
│  │  │  │  │  Loki_Zai_Aspect.py
│  │  │  │  │  Loki_Zai_idiom.py
│  │  │  │  │  Loki_Zai_Loc.py
│  │  │  │  │  Loki_Zai_QMarker.py
│  │  │  │  │  Loki_Zai_Range.py
│  │  │  │  │  Loki_Zai_State.py
│  │  │  │  │  Loki_Zai_verbP.py
│  │  │  │  │  Updater.py
│  │  │  │  │  USER_DEFINED.json
│  │  │  │  │  __init__.py
│  │  │  │  │  
│  │  │  │  └─__pycache__
│  │  │             Loki_Zai_Aspect.cpython-310.pyc
│  │  │             Loki_Zai_idiom.cpython-310.pyc
│  │  │             Loki_Zai_Loc.cpython-310.pyc
│  │  │             Loki_Zai_QMarker.cpython-310.pyc
│  │  │             Loki_Zai_Range.cpython-310.pyc
│  │  │             Loki_Zai_State.cpython-310.pyc
│  │  │             Loki_Zai_verbP.cpython-310.pyc
│  │  │             __init__.cpython-310.pyc
│  │  │          
│  │  ├─gwan_ta_de
│  │  │  │  gwan_ta_de.py
│  │  │  │  
│  │  │  └─intent
│  │  │          Loki_gwan_ta_de.py
│  │  │          Updater.py
│  │  │          USER_DEFINED.json
│  │  
│  │          
│  └─webpage
│      ├─static
│      │  ├─css
│      │  │      main.css
│      │  │      
│      │  ├─js
│      │  │      main.js
│      │  │      
│      │  └─media
│      │          android-chrome-192x192.png
│      │          android-chrome-512x512.png
│      │          apple-touch-icon.png
│      │          background.png
│      │          favicon-16x16.png
│      │          favicon-32x32.png
│      │          favicon.ico
│      │          person-man.gif
│      │          site.webmanifest
│      │          
│      ├─templates
│      │      homepage.html
│      │      pyLiteracy.html
│      │      
│      └─UI
│          │  naive_typo.py
│          │  UI_main.py
│          │  
│          ├─static
│          │  ├─css
│          │  │      main.css
│          │  │      
│          │  ├─js
│          │  │      main.js
│          │  │      
│          │  └─media
│          │          android-chrome-192x192.png
│          │          android-chrome-512x512.png
│          │          apple-touch-icon.png
│          │          background.png
│          │          favicon-16x16.png
│          │          favicon-32x32.png
│          │          favicon.ico
│          │          person-man.gif
│          │          site.webmanifest
│          │          
│          └─templates
│                 homepage.html
│                 pyLiteracy.html
│                                   
├─raw_data
│  └─Corpus
│      ├─purged
│      │      loc_zai_purged.json
│      │      loc_zai_purged.txt
│      │      
│      └─raw
│              sketch engine 再.txt
│              sketch engine 在.txt
│              
├─src
│  ├─pyLiteracy
│  │  │  
│  │  └─loki models
│  │      └─Gua_Zai
│  │          ├─intent
│  │             └─__pycache__
│  │                     Loki_Zai_Aspect.cpython-310.pyc
│  │                     Loki_Zai_idiom.cpython-310.pyc
│  │                     Loki_Zai_Loc.cpython-310.pyc
│  │                     Loki_Zai_QMarker.cpython-310.pyc
│  │                     Loki_Zai_Range.cpython-310.pyc
│  │                     Loki_Zai_State.cpython-310.pyc
│  │                     Loki_Zai_verbP.cpython-310.pyc
│  │                     __init__.cpython-310.pyc
│  │          
│  │                  
│  └─pyLiteracy.egg-info
│          dependency_links.txt
│          PKG-INFO
│          SOURCES.txt
│          top_level.txt
│          
├─tool
│          
└─workspace
    ├─log
    │      log file.txt
    │      missing_zai_0-5000.json
    │      missing_zai_1301-2300_revised.json
    │      missing_zai_2301-3301_revised.json
    │      missing_zai_301-1300_revised.json
    │      missing_zai_3301-4301.json
    │      missing_zai_5001-.json
    │      
    ├─ref_files
    │  ├─bing_jian_zhi_ref
    │  │      human_bing.ref
    │  │      
    │  ├─gwan_ta_de_ref
    │  │      gwan_ta_de.ref
    │  │      
    │  └─zai_ref
    │          Zai_Aspect.ref
    │          Zai_idiom.ref
    │          Zai_Loc.ref
    │          Zai_QMarker.ref
    │          Zai_Range.ref
    │          Zai_State.ref
    │          Zai_verbP.ref
    │          
    └─tool
            corpus_pos.py
            LokiTool.md
            LokiTool.py
            text_tool.py
            USER_DEFINED.json
```

設置環境
-------------
- 環境需求
    - Python 3.6 or above
    - pip or pip3 is installed
- 安裝相關套件
    - 執行指令：`$ pip install -r requirements.txt`

啟用 Loki 服務
-------------
1. 登入後進入 [Loki 控制台](https://api.droidtown.co/loki/)
2. 輸入專案名稱，點選 `建立專案`
3. 點選剛建立完成的專案名稱以進入專案
4. 點選 `選擇檔案` > 選擇所有 ref 內的檔案 > 點選 `讀取意圖`
5. 點選左上角房子圖示，回到 [Loki 控制台](https://api.droidtown.co/loki/)，點選 `複製` 專案金鑰
6. 將複製下來的金鑰貼上到檔案 account.info 中：
```
{
    "username" : " ***輸入 USERNAME (註冊信箱)*** ",
    "api-key" : " ***將 Articut 金鑰貼到這裡*** ",
    "loki-key" : " ***將專案金鑰貼到這裡*** ",
}
```

開始使用
-------------
- 執行指令：`$ python .\Loki\UI_main.py`
- 在瀏覽器開啟 http://127.0.0.1:5000


聯絡資訊
-------------
若您還有其他任何的疑問，歡迎透過E-mail聯繫我們，謝謝。 

Jonathan Chen：[chenjonathan901210@gmail.com](mailto:chenjonathan901210@gmail.com)

Joe Huang：[joehuangx@gmail.com](mailto:joehuangx@gmail.com)      

PeterWolf：[peter.w@droidtown.co](mailto:peter.w@droidtown.co)

Lisi Yang：[lisi16810@gmail.com](mailto:lisi16810@gmail.com)

Spec : https://docs.google.com/document/d/1QGHcbVy7gJJZVTW6DK2HHFGLnOvNRLaBPIwmPiWWSv4/edit?usp=sharing
