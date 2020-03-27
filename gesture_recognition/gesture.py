import cv2

class Gesture:

    def filt_img(self,frame):
        frame = cv2.GaussianBlur(frame,(5,5),0)
        frame = cv2.bilateralFilter(frame,5,100,100)
        return frame

    def light_remove(self,frame):
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
        y,u,v=cv2.split(hsv)
        eqy=cv2.equalizeHist(y)
        yuv = cv2.merge([eqy,u,v])
        frame = cv2.cvtColor(yuv,cv2.COLOR_YUV2BGR)
        return frame
        
    def make_binary(self,frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        gray = self.filt_img(gray)
        _,frame=cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
        return frame

    def bgSubMasking(self,frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
        fgmask = self.bgSubtractor.apply(frame, learningRate=0)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=2)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=2)
        return cv2.bitwise_and(frame, frame, mask=fgmask)

    def VideoCapture(self):
        self.bgSubtractor = cv2.createBackgroundSubtractorMOG2(10,30,False)
        cap=cv2.VideoCapture(0)
        cap.set(3,512)
        cap.set(4,512)
        
        
        while True:
        
            _, frame = cap.read()
            frame = self.light_remove(frame)
            img = self.make_binary(frame)
            mask = self.bgSubMasking(img)
            frame = cv2.bitwise_and(frame,frame,mask=mask)
            
            
            cv2.imshow("video",frame)
            
            #break when esc press down
            if cv2.waitKey(1)&0xFF == 27:
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__=='__main__':
    Gesture().VideoCapture()