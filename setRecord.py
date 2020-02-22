from darkflow.net.build import TFNet #경로 수정 필요
import datetime
import cv2
import sympy
import pyrebase
import time
import json
import os 
import numpy as np
from os.path import isfile, join

#사진to비디오
pathIn='/home/pi/darkboxflow/Darkflow/captured_img'
pathOut='/home/pi/darkboxflow/Darkflow/captured_video'
fps = 30

#사진 to 비디오 전처리 과정
frame_array = []
files=[f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
#for sorting the file names properly
files.sort(key=lambda x: x[5:-4])


#물체 인식을 위한 설정
opoptions = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}
tfnet=TFNet(options)

#Firebase와 연동을 위한 정보
config={
	"apiKey": "AIzaSyAkqWT-9ATys59Oz_Yrth-ZO-NB17fxpp4",    # webkey
	"authDomain": "kpmg-15f97.firebaseapp.com",             # 프로젝트ID
	"databaseURL": "https://kpmg-15f97.firebaseio.com",     # database url
	"storageBucket": "kpmg-15f97.appspot.com"               # storage
}
firebase=pyrebase.initialize_app(config)  #파이어베이스 연결 초기화


# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
capture=cv2.VideoCapture('..경로')#경로수정
fourcc=cv2.VideoWriter_fourcc(*'AVI')#인코딩방식
record=False
count=0
now=datetime.datetime.now().strftime("%d_%H-%M-%S")
fps=capture.get(cv2.CAP_PROP_FPS)#동영상 프레임 추출
length=int(capture.get(cv2.CAP_PROP_FRAME_COUNT))#동영상 길이
split=(fps*length)/(fps*3)




#로컬 파일 삭제 함수
def file_delete() :
    file='video.mp4'
    if os.path.isfile(file):
        os.remove(file)
#로컬 파일을 파이에어베이스에 업로드하는 함수
def file_upload() :
    # 업로드할 파일명 ("video.pm4")
    uploadfile="video.mp4"
    # 업로드할 파일의 확장자 구하기
    s=os.path.splitext(uploadfile)[1]
    # 업로드할 새로운 파일 이름 ("0000년00월00일_00시00분00초.확장자"로 설정)
    now=datetime.today().strftime("%Y%m%d_%H%M%S")
    filename=now
    # Upload files to Firebase
    storage=firebase.storage()
    storage.child("videos/"+filename).put(uploadfile)
    fileUrl=storage.child("videos/"+filename).get_url(1)  # 0 : 저장소 위치, 1 : 다운로드 url 경로
    # print(fileUrl)
    # 업로드한 파일과 다운로드 경로를 database에 저장 (나중에 사용하려고)
    db=firebase.database()
    d={}
    d[filename]=fileUrl
    data=json.dumps(d)
    results=db.child("files").push(data)
    return ("OK")


size_rate=[]

while(vidcap.isOpened()):
    ret,image=vidcap.read()
 
    if(int(vidcap.get(1))%split==0):
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("../images/frame%d.jpg" % count, image)
	imgcv=cv2.imread("../images/frame%d.jpg")
	result=tfnet.return_predict(imgcv) #JSON포맷으로 이미지정보결과 저장
        size_rate[0]=0
        for i in range(1, result.len()) :
          tlx=result[i]["topleft"]["x"]
          tly=result[i]["topleft"]["y"]
          brx=result[i]["bottomright"]["x"]
          bry=result[i]["bottomright"]["y"]
          size_rate.append((brx-tlx)*(bry-tly) - s[i-1])

#조건에 해당하지않은 프레임 삭제
for j in range(len(files)):
    if( size_rate[j] < 0 )
      if os.path.isfile(file):
          os.remove(file)

#사진 to 동영상 처리과정
for j in range(len(files)):
    filename=pathIn + files[j]
    #reading each files
    img=cv2.imread(filename)
    height,width,layers=img.shape
    size=(width,height)
    #inserting the frames into an image array
    frame_array.append(img)

fourcc=cv2.VideoWriter_fourcc(*'AVI')
out=cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'....mp4'),fourcc, fps, size)

for j in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[j])
out.release()
         

#get() 함수를 이용하여 전체 프레임 중 1/20의 프레임만 가져와 저장
#최대 30초 동영상이라고 가정.변화율 측정에 최소 3초가 필요하다고 가정.
#파이카메라의 제원이 1080p-30fps, 720p-60fps이므로
#30*30=900, 30*60=1800 -> 만약 30fps의 30초 동영상이면, split=10이 되어야함