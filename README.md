# Detect Circle Center

## 簡介
Detect Circle Center 是一個使用 OpenCV 來偵測圖像中圓心的 Python 專案。此專案提供兩個主要腳本：
1. `generate_circle_info.py`：生成帶有圓的測試圖像，並輸出圓心座標至 `output/circle_info.json`。
2. `compare_images.py`：對比兩張圖像中的圓心位置，並輸出對齊後的影像與差異影像至 `output/compare/` 目錄。

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
執行 `generate_circle_info.py` 來生成包含圓形的圖像，並儲存相關資訊：
```sh
python generate_circle_info.py
```
此步驟會：
- 讀取 `image/` 目錄內的影像，偵測並標記圓心。
- 生成處理後的影像，儲存至 `output/processed/`。
- 儲存邊緣檢測結果至 `output/`。
- 輸出圓心座標與統計資訊至 `output/circle_info.json`。

### 2. 圖像圓心比對
執行 `compare_images.py` 來對比兩張圖像的圓心：
```sh
python compare_images.py
```
此步驟會：
- 讀取 `output/circle_info.json` 內的圓心資訊。
- 讀取 `image/` 目錄內的影像，對比其圓心位置。
- 產生對齊後的影像與差異影像，儲存至 `output/compare/`。
- 計算 MSE、PSNR、差異百分比等指標，並輸出至 `output/complete_analysis.json`。

## 注意事項
- 請確保 `image/` 目錄內有影像檔案，並符合腳本格式要求。
- OpenCV 安裝版本為 `opencv-python`，若有需求可額外安裝 `opencv-python-headless`。
- `generate_circle_info.py` 必須先執行，產生 `circle_info.json` 供 `compare_images.py` 使用。

## 相關連結
GitHub Repo: [Detect_circle_center](https://github.com/dead53216/Detect_circle_center)

