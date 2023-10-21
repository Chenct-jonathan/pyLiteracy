# LokiTool 使用說明

- LokiTool 可以協助您：
    1. 在特定專案的某個意圖中新增 utterance
    2. 列出特定專案中某個意圖裡所有的 utterance


使用方式說明
---

- 準備工作：在 account.info 中填上您的註冊信箱、專案金鑰
    ```
    {
        "username" : " ***輸入USERNAME(註冊信箱)*** ",
        "loki_key" : " ***輸入專案金鑰*** ",
        "intent" : []
    }
    ```

- 使用方式：
    1. 如果你想要 "在特定專案的某個意圖中新增 json 檔裡的 utterance "
        - e.g. 專案中的意圖名稱為 loc，json 檔位置在 ./purged corpus/loc_zai_purged.json
        - 執行指令：`$ python3 LokiTool.py au -intent loc -jsonfile ./purged corpus/loc_zai_purged.json`
    
    2. 如果你想要 "列出特定專案中某個意圖裡所有的 utterance "
        - e.g. 專案中的意圖名稱為 loc
        - 執行指令：`$ python3 LokiTool.py lu -intent loc`
     