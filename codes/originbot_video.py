# reading Video
import cv2
import numpy as np
h1=50   #修改高度值
h2=498
file='./record.avi'  #车道线视频文件
def main():  
    # 打开视频文件
    cap = cv2.VideoCapture(file)  #修改成车道线视频文件所在位置
    ret = cap.isOpened()
    # 检查视频是否成功打开
    if not ret :
        print("Error: Could not open video.")
        exit()  
   
    while(ret):
        ret, frame = cap.read()
        if ret == True:            
            # 创建一个与帧相同大小的黑色屏幕，用于混合以实现透明度
            black_screen = np.zeros_like(frame) 
            # 复制本色显示的部分
            non_transparent_area = frame[h1:h2, :, :].copy() 
            # 将非透明区域放置到黑色屏幕上
            black_screen[h1:h2, :, :] = non_transparent_area 
            # 将当前帧与黑色屏幕混合，以实现50%透明度（仅对非本色显示部分）
            alpha = 0.3  # 透明度因子
            mask = np.ones_like(frame, dtype=np.float32)
            mask[h1:h2, :, :] = 0  # 本色显示部分不混合 
            # 使用掩码进行混合
            blended_frame = cv2.addWeighted(frame, alpha, black_screen, 1 - alpha, 0, mask)
            # 显示混合后的帧
            cv2.imshow('blended_frame', blended_frame)                
            k = cv2.waitKey(500)
            if( k == ord('q')):
                break 
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()