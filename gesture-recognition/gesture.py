import cv2

def VideoCapture():
    cap=cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)
    
    while True:
        not_err, frame = cap.read()
        
        if not_err:
            cv2.imshow("images",frame)
            
            #break when esc press down
            if cv2.waitKey(1)&0xFF == 27:
                break
            
    cap.release()
    cv2.destroyAllWindows()

def main():
    VideoCapture()

if __name__=='__main__':
    main()