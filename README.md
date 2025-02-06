# Detect Circle Center

## 簡介
Detect Circle Center 是一個使用 OpenCV 來偵測圖像中圓心的 Python 專案。此專案提供兩個主要腳本：
1. `generate_circle_info.py`：生成帶有圓的測試圖像並輸出圓心座標。
2. `compare_images.py`：對比兩張圖像中的圓心位置。

## 安裝方式
### 1. 安裝 Python
請確保你的系統已安裝 Python 3.7 以上的版本。

### 2. 安裝依賴套件
執行以下指令安裝所需的 Python 套件：
```sh
pip install opencv-python numpy
```

## 使用方式
### 1. 生成測試圖像
執行 `generate_circle_info.py` 來生成包含圓形的圖像：
```sh
python generate_circle_info.py
```
此步驟會產生測試圖像並輸出圓心座標。

### 2. 圖像圓心比對
執行 `compare_images.py` 來對比兩張圖像的圓心：
```sh
python compare_images.py
```
該腳本會讀取預先定義的圖片並輸出比對結果。

