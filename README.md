#  Python YouTube Web Analyzer

一個使用 Python 建立的 YouTube 資料分析網站，透過爬蟲技術抓取頻道與影片數據，並以網頁方式呈現與視覺化分析。

---

##  專案特色

*  搜尋 YouTube 頻道
*  抓取頻道基本資訊（訂閱數、影片數、建立時間等）
*  擷取所有影片資料（觀看數、按讚數、發布日期）
*  自動生成數據圖表（按讚數 / 觀看數趨勢）
*  使用 Flask 建立 Web 介面

---

## 🛠️ 技術架構

### Backend

* Python
* Flask（Web Framework）
* Selenium（爬蟲）
* pyodbc（資料庫連線）
* Matplotlib（資料視覺化）

### Frontend

* HTML (Jinja2 Template)
* CSS（靜態樣式）

### Database

* SQL Server

---

##  專案結構

```
.
├── ytdata.py              # 主程式（Flask + 爬蟲邏輯）
├── templates/             # HTML 頁面
│   ├── index.html
│   ├── s1.html
│   ├── s2.html
│   ├── f1.html
│   ├── f2.html
│   └── ff.html
├── static/
│   └── img*/              # 自動生成圖表
```

---

##  功能說明

###  搜尋頻道

輸入關鍵字，系統會：

* 搜尋 YouTube 頻道
* 顯示頻道列表

---

###  頻道分析

選擇頻道後可查看：

* 訂閱數
* 建立日期
* 影片總數
* 頻道描述
* 外部連結

---

###  影片資料抓取

系統會：

* 自動滾動載入所有影片
* 擷取每部影片：

  * 按讚數 
  * 觀看數 
  * 發布日期 

---

###  數據視覺化

自動產生：

*  每年「按讚數趨勢圖」
*  每年「觀看數趨勢圖」

---

##  執行方式

###  安裝套件

```bash
pip install flask selenium webdriver-manager pyodbc matplotlib
```

---

###  設定環境

請修改 `ytdata.py` 中以下設定：

```python
# Template 路徑
ftpath = "你的 templates 路徑"

# SQL Server 連線
conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=你的伺服器;'
    'Database=你的資料庫;'
    'Trusted_Connection=yes;'
)
```

---

###  執行專案

```bash
python ytdata.py
```

開啟瀏覽器：

```
http://127.0.0.1:5000
```

---

## 注意事項

* 需安裝 Google Chrome
* Selenium 會自動下載 ChromeDriver
* 此專案使用「爬蟲」，可能受 YouTube 改版影響
* 執行速度較慢（需等待資料抓取）

---

##  專案限制

*  無 API（純爬蟲）
*  無前後端分離
*  資料庫結構較簡單
*  未部署（本地運行）

---

##  未來優化方向

*  改用 YouTube Data API
*  使用 FastAPI 重構後端
*  前後端分離（Vue / React）
*  Docker 部署
*  加入使用者系統
*  優化爬蟲效率與穩定性

---

MIT License

---
