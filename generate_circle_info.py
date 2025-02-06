import cv2
import numpy as np
import os
import json
from datetime import datetime

def find_circle_from_edges(edges):
    height, width = edges.shape
    
    # 從四個方向找第一個邊緣點
    top_point = None
    bottom_point = None
    left_point = None
    right_point = None
    
    # 從上往下找
    for y in range(height):
        for x in range(width):
            if edges[y, x] == 255:
                top_point = (x, y)
                break
        if top_point is not None:
            break
    
    # 從下往上找
    for y in range(height-1, -1, -1):
        for x in range(width):
            if edges[y, x] == 255:
                bottom_point = (x, y)
                break
        if bottom_point is not None:
            break
    
    # 從左往右找
    for x in range(width):
        for y in range(height):
            if edges[y, x] == 255:
                left_point = (x, y)
                break
        if left_point is not None:
            break
    
    # 從右往左找
    for x in range(width-1, -1, -1):
        for y in range(height):
            if edges[y, x] == 255:
                right_point = (x, y)
                break
        if right_point is not None:
            break
    
    if all(point is not None for point in [top_point, bottom_point, left_point, right_point]):
        center_x = (left_point[0] + right_point[0]) // 2
        center_y = (top_point[1] + bottom_point[1]) // 2
        radius1 = (right_point[0] - left_point[0]) // 2
        radius2 = (bottom_point[1] - top_point[1]) // 2
        radius = (radius1 + radius2) // 2
        
        return (center_x, center_y), radius
    return None, None

def process_image(frame):
    # 轉換成灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Canny 邊緣檢測
    edges = cv2.Canny(blurred, 50, 150)
    
    # 找圓心和半徑
    center_radius = find_circle_from_edges(edges)
    
    # 建立處理後的彩色影像
    processed = frame.copy()
    
    if center_radius[0] is not None:
        center, radius = center_radius
        # 畫出圓形
        cv2.circle(processed, center, radius, (0, 255, 0), 2)
        # 畫出圓心
        cv2.circle(processed, center, 3, (0, 0, 255), -1)
        # 加入文字標註
        cv2.putText(processed, f"Center: ({center[0]}, {center[1]})", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(processed, f"Radius: {radius}", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return center_radius, edges, processed

def main():
    # 記錄時間和使用者
    timestamp = "2025-01-22 11:03:55"
    user = "dead53216"
    
    print(f"開始處理...")
    print(f"時間：{timestamp}")
    print(f"使用者：{user}")
    
    if not os.path.exists('image'):
        print("找不到 image 資料夾")
        return
        
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 建立處理後圖片的資料夾
    processed_dir = os.path.join(output_dir, "processed")
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    # 讀取圖片並取得圓心資訊
    image_files = sorted([f for f in os.listdir('image') if f.endswith(('.png', '.jpg', '.jpeg'))])
    circle_info = {}
    
    # 用於計算平均值的列表
    centers_x = []
    centers_y = []
    radiuses = []
    
    print("\n處理圖片並找尋圓心...")
    for img_file in image_files:
        frame = cv2.imread(os.path.join('image', img_file))
        if frame is None:
            print(f"無法讀取影像：{img_file}")
            continue
        
        print(f"處理：{img_file}")
        (center, radius), edges, processed = process_image(frame)
        
        if center is not None:
            circle_info[img_file] = {
                'center': {'x': center[0], 'y': center[1]},
                'radius': radius
            }
            print(f"圓心座標：({center[0]}, {center[1]})")
            print(f"半徑：{radius}")
            
            # 收集數據以計算平均值
            centers_x.append(center[0])
            centers_y.append(center[1])
            radiuses.append(radius)
            
            # 儲存邊緣檢測結果
            cv2.imwrite(os.path.join(output_dir, f"edges_{img_file}"), edges)
            
            # 儲存處理後的圖片
            cv2.imwrite(os.path.join(processed_dir, img_file), processed)
        else:
            print(f"無法在 {img_file} 中找到圓形")
    
    # 計算平均值
    if centers_x and centers_y and radiuses:
        avg_center_x = sum(centers_x) / len(centers_x)
        avg_center_y = sum(centers_y) / len(centers_y)
        avg_radius = sum(radiuses) / len(radiuses)
        
        # 計算標準差
        std_center_x = np.std(centers_x)
        std_center_y = np.std(centers_y)
        std_radius = np.std(radiuses)
        
        # 將平均值和標準差加入到 circle_info
        circle_info['statistics'] = {
            'average_center': {
                'x': float(avg_center_x),
                'y': float(avg_center_y)
            },
            'average_radius': float(avg_radius),
            'std_center': {
                'x': float(std_center_x),
                'y': float(std_center_y)
            },
            'std_radius': float(std_radius)
        }
        
        print("\n統計資訊：")
        print(f"平均圓心座標：({avg_center_x:.2f}, {avg_center_y:.2f})")
        print(f"圓心座標標準差：({std_center_x:.2f}, {std_center_y:.2f})")
        print(f"平均半徑：{avg_radius:.2f}")
        print(f"半徑標準差：{std_radius:.2f}")
    
    # 儲存圓形資訊
    with open(os.path.join(output_dir, 'circle_info.json'), 'w') as f:
        json.dump(circle_info, f, indent=4)
    
    print("\n圓形資訊已儲存至 circle_info.json")
    print(f"處理後的圖片已儲存至 {processed_dir}")
    print(f"邊緣檢測結果已儲存至 {output_dir}")

if __name__ == "__main__":
    main()