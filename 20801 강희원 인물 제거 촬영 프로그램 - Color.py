import cv2                      #영상처리 라이브러리 OpenCV
import numpy as np
import sys
from collections import Counter #최빈값 추출 라이브러리

maxlen = 15                 #촬영할 동영상 프레임 수
cap = cv2.VideoCapture(0)   #웹캠 사용
_, initcam = cap.read()     
width, height, channel = initcam.shape  #웹캠 해상도
i=0             #촬영한 프레임 수 저장
FrameList = np.zeros((width, height, channel, maxlen))   #3채널(RGB)의 프레임을 담는 numpy 배열(초깃값 0)
MostCommon_Float = np.zeros((width, height, channel))          #최빈값을 모은 하나의 사진을 담는 numpy 배열(초깃값 0)

while cap.isOpened() :
    success, frame = cap.read()                     #반복하며 웹캠에서 영상 가져옴
    if success : 
        for j in range(height) :
            for k in range(width) :
                for l in range(3) :
                    FrameList[k, j, l, i] = frame[k, j, l]  #가져온 프레임 순서대로 저장
        i+=1
        cv2.imshow('Camera Window', frame)              #현재 프레임 화면에 보여줌

        key = cv2.waitKey(1) & 0xFF     #ESC 누르면 촬영 종료
        if (key == 27 or i >= maxlen): 
            break
cap.release()
cv2.destroyAllWindows()

if i <= 2 :                             #프레임 1장 이하면 프로그램 중단
    print("Frame Shortage Error")
    sys.exit()

for j in range(height) :
        for k in range(width) :
            for l in range(3) :
                cnt = Counter(FrameList[k, j, l])        #프레임 각 픽셀을 돌며 최빈값 추출
                temp = cnt.most_common()[0][0]
                
                if temp != 0 :
                    MostCommon_Float[k, j, l] = float(temp)    #최빈값이 0이 아닌 경우 해당 최빈값으로 설정
                else :
                    
                    MostCommon_Float[k, j, l] = float(cnt.most_common()[1][0]) #최빈값이 0인 경우 두번째로 많이 나온 값으로 설정
                    
MostCommon_Int=MostCommon_Float.astype(np.uint8)    #실수->정수 형 변환
cv2.imshow("People Subtract Image", MostCommon_Int)         #최빈값 모은 최종 이미지 출력

while True :
    key = cv2.waitKey(1) & 0xFF
    if (key == 27):             #ESC 누르면 이미지 저장과 함께 프로그램 종료
        break

cv2.destroyAllWindows()
cv2.imwrite('PeopleSubtract.jpg', MostCommon_Int)
