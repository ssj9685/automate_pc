import cv2
import numpy as np

def filtered_thresh(crop_image):
        blur = cv2.GaussianBlur(crop_image, (3, 3), 0)
        
        #Convert color to YCrCb
        imageYCrCb = cv2.cvtColor(blur, cv2.COLOR_BGR2YCR_CB)
        
        #Fix skin color range
        min_YCrCb = np.array([0,133,77],np.uint8)
        max_YCrCb = np.array([235,173,127],np.uint8)
        mask = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
        
        kernel = np.ones((5, 5))
        
        # Apply morphological transformations to filter out the background noise
        dilation = cv2.dilate(mask, kernel, iterations=1)
        erosion = cv2.erode(dilation, kernel, iterations=1)
        
        # Apply Gaussian Blur and Threshold
        filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
        ret, thresh = cv2.threshold(filtered, 127, 255, 0)
        
        return thresh

def cap_img():
    cap=cv2.VideoCapture(0)
    cnt=0
    while True:
        _,frame=cap.read()
        frame=cv2.flip(frame,1)
        crop = frame[200:400,400:600]
        crop = filtered_thresh(crop)
        cv2.rectangle(frame, (399, 199), (601, 401), (0, 255, 0), 1)      
        cv2.imshow("video",frame)
        cv2.imshow("crop",crop)
        
        key=cv2.waitKey(1)&0xFF
        
        if key == ord('0'):
            cv2.imwrite("C:/Users/shin/dataset/train/zero/0_"+str(cnt)+".png",crop)
            cnt+=1
            print("0")
        if key == ord('1'):
            cv2.imwrite("C:/Users/shin/dataset/train/one/1_"+str(cnt)+".png",crop)
            cnt+=1
            print("1")
        if key == ord('2'):
            cv2.imwrite("C:/Users/shin/dataset/train/two/2_"+str(cnt)+".png",crop)
            cnt+=1
            print("2")
        if key == ord('3'):
            cv2.imwrite("C:/Users/shin/dataset/train/three/3_"+str(cnt)+".png",crop)
            cnt+=1
            print("3")
        if key == ord('4'):
            cv2.imwrite("C:/Users/shin/dataset/train/four/4_"+str(cnt)+".png",crop)
            cnt+=1
            print("4")
        if key == ord('5'):
            cv2.imwrite("C:/Users/shin/dataset/train/five/5_"+str(cnt)+".png",crop)
            cnt+=1
            print("5")            
        if key == 27:
            break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    cap_img()