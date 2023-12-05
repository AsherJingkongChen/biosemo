## 專案概要

### 專案組成
- **前端 (FE):** 使用 Vue.js 構建的 Web 介面。
- **後端 (BE):** 使用 FastAPI 框架搭建的 Python 後端，整合了機器學習 (ML) 模型。
- **機器學習 (ML):** 使用 PyCaret 函式庫進行模型訓練和部署。
- **工具箱 (Utils):** 存儲了用於心率變異性 (HRV) 特徵提取的 Python 模塊。

## 專案檔案結構

### 主要檔案

- **analyze.ipynb:** 用於數據分析的 Jupyter Notebook。

- **preprocess.ipynb:** 用於數據預處理的 Jupyter Notebook。

- **deploy.py:** 主要的部署腳本，配置 FastAPI 和模型部署。

- **requirements.txt:** 存儲專案的相依套件清單。

- **logs.log:** 日誌檔案，記錄應用程式運行時的事件和錯誤。

- **utils/:** 存放各種工具和輔助功能的目錄。

### 工具模組

- **hrv_feature_extraction.py:** 用於從心率數據中提取特徵的 Python 模組。

## 使用者操作

### 機器學習 (ML)
- 使用 **analyze.ipynb** 進行數據分析。
- 使用 **preprocess.ipynb** 預處理數據。
- 透過 **deploy.py** 部署機器學習模型。

### 前端 (FE)
- 使用 Vue.js 建構 Web 介面。

### 後端 (BE)
- 使用 FastAPI 框架建構 Python 後端。

### DevOps
- 透過 **requirements.txt** 管理專案相依套件。

## 資料流程

1. **數據分析：**
   - 使用 **analyze.ipynb** 對數據進行分析。

2. **數據預處理：**
   - 使用 **preprocess.ipynb** 進行數據預處理。

3. **機器學習模型訓練：**
   - 使用 **deploy.py** 進行機器學習模型的訓練和部署。

4. **Web 介面建構：**
   - 使用 Vue.js 構建 Web 介面。

5. **應用程式部署和運行：**
   - 部署 FastAPI 後端應用程式，運行整個系統。

## 結論
此專案以機器學習、前端、後端的整合方式建構一個包含數據分析和機器學習功能的 Web 應用程式。使用者可以透過操作相應的檔案和腳本執行數據流程、訓練模型以及部署應用程式。
