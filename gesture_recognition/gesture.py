import cv2

def VideoCapture():
    bgsub = cv2.createBackgroundSubtractorKNN()
    cap=cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)
    
    while True:
        _, frame = cap.read()
        cv2.imshow("bgsub",bgsub.apply(frame))
        
        #break when esc press down
        if cv2.waitKey(1)&0xFF == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()

def main():
    VideoCapture()

if __name__=='__main__':
    main()