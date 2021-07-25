import cv2 , time
from datetime import datetime
import pandas

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=['Baslat','Bitir'])

video=cv2.VideoCapture(0) 

while True:
    check , frame = video.read()
    status=0

#print(check) #boolean : videonun çalışıp çalışmadığını kontrol etme
#print(frame) #numpy dizisi : videonun yakaladığı ilk görüntü

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0) 

    if first_frame is None :
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray) 

    thresh_frame=cv2.threshold(delta_frame, 30 , 255 , cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)  

    (cnts,_)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 15000:
            continue
        status=1

        (x,y,w,h)= cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y) , (x+w , y+h) , (255,0,0) , 3)

    status_list.append(status) 

    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0: 
        times.append(datetime.now())

    if status_list[-1]==0 and status_list[-2]==1: 
        times.append(datetime.now())



    cv2.imshow("Gri Cerceve",gray)
    cv2.imshow("Delta Cerceve",delta_frame)
    cv2.imshow("Esik Cerceve",thresh_frame)
    cv2.imshow("Renkli Cerceve",frame)

    key=cv2.waitKey(1)

    

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

#print(status_list)
print(times)

for i in range(0,len(times),2): 
    df=df.append({'Baslat':times[i], 'Bitir':times[i+1]} , ignore_index= True)

df.to_csv("Kaydet.csv")    #CSV olarak kaydet

video.release()
cv2.destroyAllWindows()
