# -Python-YouTube-Web-
本專案為團隊共同開發之「YouTube 頻道數據爬蟲與視覺化 Web 應用」。使用者只需在網頁輸入 YouTube 頻道名稱或網址，系統便會透過 Selenium 自動化爬取該頻道的簡介、歷年影片觀看次數與按讚數等核心數據，並將資料結構化寫入 SQL Server 資料庫。最後，後端結合 Matplotlib 繪製出該頻道各年度的觀看與按讚趨勢折線圖，並透過 Flask 渲染至網頁前端，提供直觀的頻道經營成效分析。

【主要功能】
1. 頻道搜尋與定位：支援透過「頻道名稱」搜尋或直接輸入「頻道網址」。
2. 頻道基本資料擷取：自動抓取頻道加入日期、總影片數、總觀看次數與頻道簡介。
3. 影片數據爬取：模擬捲動載入，抓取頻道內所有影片的發布日期、按讚數與觀看次數。
4. 資料庫儲存：將爬取的原始數據（包含頻道資訊、影片數據）寫入 SQL Server 資料庫。
5. 數據視覺化：以「年份」為單位，使用 Matplotlib 自動繪製出該頻道歷年的「觀看數」與「按讚數」折線圖，並顯示於網頁上。

【技術架構】
* 後端框架：Python Flask
* 網頁爬蟲：Selenium (搭配 Chrome WebDriver)
* 資料庫：Microsoft SQL Server (透過 pyodbc 連線)
* 數據視覺化：Matplotlib
* 前端介面：HTML / CSS (Jinja2 模板引擎)

【環境建置與執行準備】
在執行本專案前，請確保您的開發環境已安裝以下套件與軟體：

1. 安裝 Python 依賴套件：
   pip install flask selenium webdriver-manager pyodbc matplotlib

2. 資料庫設定：
   * 本機需安裝 Microsoft SQL Server。
   * 需建立一個名為 `testdb` 的資料庫。
   * (註：程式執行時會自動 DROP 並 CREATE 所需的資料表 adata, bdata, cdata, tdata, vdata，請勿將重要資料與此資料庫共用)。

3. 路徑設定修改 (重要！)：
   在執行 `ytdata.py` 前，請務必將程式碼中的絕對路徑修改為您本機的實際路徑：
   * `ftpath`：請更改為存放模板與靜態資源的資料夾路徑 (例如：C:\Users\...\f_templates)
   * `font_path`：請確認 Windows 字體路徑 (C:\Windows\Fonts\kaiu.ttf) 是否正確，以免 Matplotlib 繪圖時中文顯示為亂碼。

【執行方式】
1. 啟動資料庫服務 (SQL Server)。
2. 在終端機執行：`python ytdata.py`
3. 打開瀏覽器，前往 `http://127.0.0.1:5000/` 即可開始使用。

【注意事項與已知限制】
* 爬蟲穩定性：本專案使用 Selenium 模擬瀏覽器行為，若 YouTube 網頁結構更新，或因網路延遲導致元素載入較慢，可能會造成程式抓不到資料 (XPath 失效)。
* 執行時間：頻道影片數量越多，爬取與繪圖所需的時間越長，請耐心等待網頁加載。
