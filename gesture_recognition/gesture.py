import cv2
import numpy
import matplotlib.pyplot as plt

class Gesture:

    def f(self,t):
        sig=6/29
        t[t>sig**3]=t[t>sig**3]**(1/3)
        t[t<=sig**3]=t[t<=sig**3]/(3*sig**2)+4/29
        
        return t
    
    def filt_img(self,frame):
        frame = cv2.bilateralFilter(frame,5,100,100)
        return frame
        
    def equal_img(self,frame):
        '''
        r,g,b=cv2.split(frame)
        r=cv2.equalizeHist(r)
        g=cv2.equalizeHist(g)
        b=cv2.equalizeHist(b)
        rgb=cv2.merge([r,g,b])
        '''
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        frame = cv2.equalizeHist(frame)
        return frame
        
    def make_hsv(self,frame):
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
        return frame
        
    
    def make_binary(self,frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        _,frame=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        return frame

    def bgSubMask(self,frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        fgmask = self.bgSubtractor.apply(frame,0)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=1)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=1)
        #frame = cv2.bitwise_and(frame,frame,mask=mask)
        return fgmask    
    
    def VideoCapture(self):
        #self.bgSubtractor = cv2.createBackgroundSubtractorMOG2(700,30,False)
        cap=cv2.VideoCapture(0)
        
        
        #XYZ=M*RGB reference
        M=numpy.array([[0.4887180,0.3106803,0.2006017],
                       [0.1762044,0.8129847,0.0108109],
                       [0.0000000,0.0102048,0.9897952]])
        while True:
        
            _, frame = cap.read()
            frame = cv2.flip(frame,1)
         
            bgr = frame
            b,g,r = cv2.split(bgr)
            
            x=M[0][0]*r+M[0][1]*g+M[0][2]*b
            y=M[1][0]*r+M[1][1]*g+M[1][2]*b
            z=M[2][0]*r+M[2][1]*g+M[2][2]*b
            
            l=116*self.f(y/100)-16
            a=500*(self.f(x/95.0489)-self.f(y/100))
            b=200*(self.f(y/100)-self.f(z/108.8840))
            
            
            #this is float64 uint8? how to convert
            #how to normalization
            lab=cv2.merge([l,a,b])
            
            
            
            #cv2.imshow("video0",lab)
            
            #break when esc press down
            if cv2.waitKey(1)&0xFF == 27:
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__=='__main__':
    Gesture().VideoCapture()