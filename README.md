# Python YouTube Web Analyzer

這是一個使用 Python 開發的 YouTube 資料分析網站，透過 Selenium 爬取頻道與影片資料，並使用 Flask 建立網頁介面呈現分析結果。

本專案主要用於練習爬蟲技術、後端開發以及基礎資料視覺化。

---

## 專案內容

使用者可以輸入關鍵字搜尋 YouTube 頻道，系統會列出相關頻道並顯示基本資訊。
選擇特定頻道後，會進一步抓取該頻道的影片資料，包含觀看數、按讚數與發布日期，並整理為圖表進行分析。

---

## 使用技術

後端：

* Python
* Flask
* Selenium
* pyodbc

資料處理與視覺化：

* Matplotlib

資料庫：

* SQL Server

前端：

* HTML（Jinja2 模板）

---

## 專案結構

```
f_templates/
├── ytdata.py              # 主程式（Flask + 爬蟲 + 資料分析）
├── ytdate.ipynb           # 開發過程中用於測試與分析的 Notebook
├── index.html             # 首頁
├── s1.html                # 頻道搜尋結果頁
├── s2.html                # 頻道詳細資訊頁
├── f1.html                # 搜尋失敗頁
├── f2.html                # 頻道載入失敗頁
├── ff.html                # 圖表結果頁
├── static/
│   └── img1/              # 圖表輸出資料夾（執行後產生）
```

---

## 功能說明

系統主要分為三個部分。

第一是頻道搜尋功能，使用者輸入關鍵字後，系統會從 YouTube 搜尋相關頻道並顯示結果。

第二是頻道資訊分析，可以查看頻道的訂閱數、影片數量、建立時間、觀看總數以及相關連結。

第三是影片資料分析，系統會抓取所有影片的觀看數與按讚數，依照年份整理，並生成折線圖呈現趨勢。

---

## 執行方式

### 1. 安裝套件

```
pip install flask selenium webdriver-manager pyodbc matplotlib
```

---

### 2. 修改設定

請在 `ytdata.py` 中設定以下內容：

* templates 路徑
* SQL Server 連線資訊

範例：

```
ftpath = "你的資料夾路徑"

conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=你的伺服器;'
    'Database=你的資料庫;'
    'Trusted_Connection=yes;'
)
```

---

### 3. 執行程式

```
python ytdata.py
```

開啟瀏覽器進入：

```
http://127.0.0.1:5000
```

---

## 補充說明

本專案使用 Selenium 進行網頁爬取，因此執行速度較慢，且可能受到 YouTube 網頁結構變動影響。

圖表會在執行過程中自動產生，並儲存在 `static` 資料夾中。

`ytdate.ipynb` 為開發過程中用於測試與資料分析的檔案，不影響主程式執行。

---

## 限制

目前專案為本地端應用，尚未部署至雲端。
未使用官方 API，資料來源依賴網頁結構。
專案結構較為集中，未進行模組化拆分。

---
