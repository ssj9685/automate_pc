import numpy as np
import cv2
import math
import pyautogui as pg

class Gesture:
    
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 200
        self.color = (0, 255, 0)
        self.thick = 1
        self.mx = 50
        self.my = 50
    
    def filtered_thresh(self, crop_image):
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
        
    def calculateAngle(self, far, start, end):
        """Cosine rule"""
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = (math.acos((b**2 + c**2 - a**2) / (2*b*c)) * 180) / 3
        return angle
    
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y
    
    #Key classification for ROI location
    def keyClass(self, key):
        if key == ord('a'):
            self.x = self.x - 20
        if key == ord('d'):
            self.x = self.x + 20
        if key == ord('w'):
            self.y = self.y - 20
        if key == ord('s'):
            self.y = self.y + 20
        if key == ord('q'):
            self.size = self.size - 20
        if key == ord('e'):
            self.size = self.size + 20
            
                
    def main(self):
        webcam = cv2.VideoCapture(0)
        while True:
        
            _,frame = webcam.read()
            frame = cv2.flip(frame,1)
            
            crop_image = frame[self.y : self.y + self.size , self.x : self.x + self.size]
            cv2.rectangle(frame, (self.x, self.y), (self.x + self.size, self.y + self.size), self.color, self.thick)
            
            cv2.namedWindow('video')
            cv2.setMouseCallback('video',self.mouse_callback)
            
            thresh = self.filtered_thresh(crop_image)
            
            cv2.imshow("thresh", thresh)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            
            if(contours):
                # Find contour with maximum area
                contour = max(contours, key = lambda x: cv2.contourArea(x))
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)
                
                # Find convex hull
                hull = cv2.convexHull(contour)

                # Draw contour
                drawing = np.zeros(crop_image.shape, np.uint8)
                
                cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
                cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

                # Find convexity defects
                hull = cv2.convexHull(contour, returnPoints=False)
                defects = cv2.convexityDefects(contour, hull)

                count_defects = 0
                if(defects is not None):
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(contour[s][0])
                        end = tuple(contour[e][0])
                        far = tuple(contour[f][0])
                        angle = self.calculateAngle(far, start, end)

                        # if angle > 90 draw a circle at the far point
                        if angle < 90:
                            count_defects += 1
                            cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

                        cv2.line(crop_image, start, end, [0, 255, 0], 2)

                # Print number of fingers
                if count_defects == 0:
                    cv2.putText(frame, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
                    self.mx = self.mx + 1
                    pg.moveTo(self.mx, self.my)
                if count_defects == 1:
                    cv2.putText(frame, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    self.my = self.my + 1
                    pg.moveTo(self.mx, self.my)
                if count_defects == 2:
                    cv2.putText(frame, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    self.mx = self.mx - 1
                    pg.moveTo(self.mx, self.my)
                if count_defects == 3:
                    cv2.putText(frame, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    self.my = self.my - 1
                    pg.moveTo(self.mx, self.my)
                if count_defects == 4:
                    cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    pg.click()
            
            cv2.imshow("video", frame)
            
            key = cv2.waitKey(1)&0xFF
            if key == 27:
                break
                
            self.keyClass(key)

        webcam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    Gesture().main()