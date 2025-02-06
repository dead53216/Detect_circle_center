import cv2
import numpy as np
import os
import json

def align_and_subtract(base_img, compare_img, base_center, compare_center):
    shift_x = base_center[0] - compare_center[0]
    shift_y = base_center[1] - compare_center[1]
    
    M = np.float32([[1, 0, shift_x],
                    [0, 1, shift_y]])
    
    aligned_img = cv2.warpAffine(compare_img, M, (base_img.shape[1], base_img.shape[0]))
    diff = cv2.absdiff(base_img, aligned_img)
    
    return diff, aligned_img

def calculate_metrics(base_img, aligned_img, diff):
    mse = float(np.mean((base_img - aligned_img) ** 2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(base_img - aligned_img)))
    
    if mse != 0:
        psnr = float(20 * np.log10(255.0 / np.sqrt(mse)))
    else:
        psnr = float('inf')
    
    total_pixels = base_img.shape[0] * base_img.shape[1] * base_img.shape[2]
    different_pixels = int(np.count_nonzero(diff))
    diff_percentage = float((different_pixels / total_pixels) * 100)
    
    diff_channels = cv2.mean(diff)[:3]  # BGR channels
    
    return {
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'psnr': psnr,
        'diff_percentage': diff_percentage,
        'channel_diff': {
            'blue': float(diff_channels[0]),
            'green': float(diff_channels[1]),
            'red': float(diff_channels[2])
        }
    }

def main():
    output_dir = "output/compare"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 讀取圓形資訊
    try:
        with open(os.path.join("output", 'circle_info.json'), 'r') as f:
            circle_info = json.load(f)
    except FileNotFoundError:
        print("找不到 circle_info.json，請先執行 generate_circle_info.py")
        return
    
    image_files = sorted(list(circle_info.keys())[:-1])
    all_comparisons = {}
    
    # 對每張圖片進行比較
    print("進行圖片比較...")
    for base_file in image_files:
        base_img = cv2.imread(os.path.join('image', base_file))
        base_center = (circle_info[base_file]['center']['x'], 
                      circle_info[base_file]['center']['y'])
        
        comparisons = {}
        for compare_file in image_files:
            if compare_file == base_file:
                continue
                
            compare_img = cv2.imread(os.path.join('image', compare_file))
            compare_center = (circle_info[compare_file]['center']['x'],
                            circle_info[compare_file]['center']['y'])
            
            diff, aligned_img = align_and_subtract(base_img, compare_img, base_center, compare_center)
            metrics = calculate_metrics(base_img, aligned_img, diff)
            
            # 儲存對齊後的圖片和差異圖片
            aligned_filename = f"aligned_{os.path.splitext(base_file)[0]}_{os.path.splitext(compare_file)[0]}.png"
            diff_filename = f"diff_{os.path.splitext(base_file)[0]}_{os.path.splitext(compare_file)[0]}.png"
            
            cv2.imwrite(os.path.join(output_dir, aligned_filename), aligned_img)
            cv2.imwrite(os.path.join(output_dir, diff_filename), diff)
            
            comparisons[compare_file] = {
                'metrics': metrics,
                'aligned_image': aligned_filename,
                'diff_image': diff_filename
            }
        
        # 計算平均指標
        avg_mse = float(np.mean([comp['metrics']['mse'] for comp in comparisons.values()]))
        avg_psnr = float(np.mean([comp['metrics']['psnr'] for comp in comparisons.values()]))
        avg_diff = float(np.mean([comp['metrics']['diff_percentage'] for comp in comparisons.values()]))
        
        all_comparisons[base_file] = {
            'average_metrics': {
                'mse': avg_mse,
                'psnr': avg_psnr,
                'diff_percentage': avg_diff
            },
            'comparisons': comparisons
        }
    
    # 找出最佳基準圖片
    best_image = min(all_comparisons.items(), key=lambda x: x[1]['average_metrics']['mse'])[0]
    
    # 輸出結果
    print("\n每張圖片作為基準的平均指標：")
    print("\n{:<8} {:<12} {:<12} {:<12}".format("圖片", "平均MSE", "平均PSNR", "平均差異%"))
    print("-" * 50)
    
    # 根據 MSE 排序並顯示結果
    sorted_results = sorted(all_comparisons.items(), key=lambda x: x[1]['average_metrics']['mse'])
    
    for img, data in sorted_results:
        metrics = data['average_metrics']
        print("{:<8} {:<12.2f} {:<12.2f} {:<12.2f}".format(
            img,
            metrics['mse'],
            metrics['psnr'],
            metrics['diff_percentage']
        ))
    
    print(f"\n最佳基準圖片：{best_image}")
    best_metrics = all_comparisons[best_image]['average_metrics']
    print(f"平均 MSE：{best_metrics['mse']:.2f}")
    print(f"平均 PSNR：{best_metrics['psnr']:.2f}")
    print(f"平均差異百分比：{best_metrics['diff_percentage']:.2f}%")
    
    # 儲存分析結果
    results = {
        'best_reference_image': best_image,
        'all_comparisons': all_comparisons
    }
    
    with open(os.path.join("output", 'complete_analysis.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    print("\n完整分析結果已儲存至：complete_analysis.json")

if __name__ == "__main__":
    main()