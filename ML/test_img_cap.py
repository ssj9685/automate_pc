import cv2

def cap_img():
    cap=cv2.VideoCapture(0)
    cnt=0
    while True:
        _,frame=cap.read()
        frame=cv2.flip(frame,1)
        frame_copy = frame
        cv2.rectangle(frame_copy, (400, 200), (600, 400), (0, 255, 0), 3)
        cv2.imshow("video",frame_copy)
        
        key=cv2.waitKey(1)&0xFF
        
        if key == ord('0'):
            cv2.imwrite("C:/Users/shin/dataset/test/zero/0_"+str(cnt)+".png",frame[200:400,400:600])
            cnt+=1
            print("1")
        if key == ord('1'):
            cv2.imwrite("C:/Users/shin/dataset/test/one/1_"+str(cnt)+".png",frame[200:400,400:600])
            cnt+=1
            print("1")
        if key == ord('2'):
            cv2.imwrite("C:/Users/shin/dataset/test/two/2_"+str(cnt)+".png",frame[200:400,400:600])
            print("2")
        if key == ord('3'):
            cv2.imwrite("C:/Users/shin/dataset/test/three/3_"+str(cnt)+".png",frame[200:400,400:600])
            print("3")
        if key == ord('4'):
            cv2.imwrite("C:/Users/shin/dataset/test/four/4_"+str(cnt)+".png",frame[200:400,400:600])
            print("4")
        if key == ord('5'):
            cv2.imwrite("C:/Users/shin/dataset/test/five/5_"+str(cnt)+".png",frame[200:400,400:600])
            print("5")            
        if key == 27:
            break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    cap_img()