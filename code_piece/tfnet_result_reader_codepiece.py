import cv2
import time
import screeninfo
from PIL import ImageGrab
import os, sys

#------------------------------------#
#Selection of RoI - maplestory select#
#------------------------------------#

screen_id = 0
DIVIDE_CONSTANT = 2

from mss import mss
with mss() as sct :
    filename = sct.shot(mon=-1, output='JanghooModule_RunWithMapleGUI/tmpfolder/fullscreen.png')
    print(filename)


img = cv2.imread('JanghooModule_RunWithMapleGUI/tmpfolder/fullscreen.png')
window_name = '*left-top ~ right-bottom* ! Drag your Maple Screen! space key + enter key : exit!'
screen = screeninfo.get_monitors()[screen_id]
print(int(screen.width / DIVIDE_CONSTANT) , int(screen.height / DIVIDE_CONSTANT))
img = cv2.resize(img, dsize=(int(screen.width / DIVIDE_CONSTANT), int(screen.height / DIVIDE_CONSTANT)), interpolation=cv2.INTER_AREA)


print(screen.width, screen.height)
cv2.putText(img, window_name,
            (80, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255,255,133),
            thickness=2,
            lineType=cv2.LINE_AA)

cv2.imshow(window_name, img)

bbox = cv2.selectROI(window_name, img)

cv2.waitKey()
cv2.destroyAllWindows()
print('Selected bounding box : xmin / ymin / width / height : {}'.format(bbox))



#------------------------------------#
#Load Trained Model, !option careful!#
#------------------------------------#

# 1. model : loading Classification Model
import tensorflow as tf
from keras.preprocessing import image
print('now model loading')
model = tf.keras.models.load_model('JanghooModule_RunWithMapleGUI/Janghoo_Model/Janghoo_model.h5')
label = ['elinia', 'henesis', 'kerningcity', 'perion']


# 2. model : loading YOLO
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Darkflow'))
currentPath = os.getcwd()
print('path before import TFNet : ', currentPath, "\n", sys.path)
from darkflow.net.build import TFNet
#from MAiEye.Project.darkflow.net.build import TFNet
options = {"model": "Darkflow/cfg/tiny-yolo-maple.cfg",
           "pbLoad": "Darkflow/built_graph/tiny-yolo-maple.pb",
           "metaLoad": "Darkflow/built_graph/tiny-yolo-maple.meta",
           "labels" : "Darkflow/labels-maple.txt",
           "threshold": 0.05}
tfnet = TFNet(options)




#------------#
#Run program!#
#------------#

while True :

    # 전체 delay 설정
    time.sleep(0.3)

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break

    # ImageGrab.grab 함수는 화면 특정 좌표의 영역을 캡쳐한 이미지를 return 한다.
    # Divide constant 는 처음에 roi 를 선택할때 축소된 비율로, 다시 확대시켜 주는 작업일 뿐임.
    mapleimage_original = ImageGrab.grab((bbox[0]*DIVIDE_CONSTANT, bbox[1]*DIVIDE_CONSTANT,
                                        bbox[0]*DIVIDE_CONSTANT + bbox[2]*DIVIDE_CONSTANT,
                                        bbox[1]*DIVIDE_CONSTANT + bbox[3]*DIVIDE_CONSTANT))
    mapleimage_original.save('JanghooModule_RunWithMapleGUI/tmpmaplescreenshot/maple_current.jpg')
    mapleimage_original = cv2.imread('JanghooModule_RunWithMapleGUI/tmpmaplescreenshot/maple_current.jpg')

    inputimage = mapleimage_original.copy()
    inputimage = cv2.resize(inputimage, dsize=(80,80))
    inputimage = image.img_to_array(inputimage)
    inputimage = inputimage.reshape((1,) + inputimage.shape)

#    test_num = test_num[:, :, 0]
#    test_num = (test_num > 125) * test_num
#    test_num = test_num.astype('float32') / 255.
#    test_num = test_num.reshape((1, 28, 28, 1))


    # Classification Model Answer
    answer = label[int(model.predict_classes(inputimage))]
    print('The Answer is ', answer)

    # Yolo Model Answer
    imgcv = cv2.imread('JanghooModule_RunWithMapleGUI/tmpmaplescreenshot/maple_current.jpg')
    result = tfnet.return_predict(imgcv)
    print('mob location :' ,result)
    for objects_in_result in result :
        #p1 = (int((objects_in_result['topleft'])['x']),int((objects_in_result['bottomright'])['y']))
        #p2 = (int((objects_in_result['bottomright'])['x']),int((objects_in_result['topleft'])['y']))
        #이 주석은 뭐냐면... json return 의 레이블이 잘못돼있어서 뻘짓한거 버리기 아까운 코드
        p1 = (int(objects_in_result['topleft']['x']),int(objects_in_result['topleft']['y']))
        p2 = (int(objects_in_result['bottomright']['x']), int(objects_in_result['bottomright']['y']))
        print(p1, p2)
        #p1 : bottomleft x , bottomleft y
        #p2 : topright x, topright y
        imgcv = cv2.rectangle(imgcv, p1, p2, (255,255,255), 2, 1)
        imgcv = cv2.putText(imgcv, objects_in_result['label'],
                    (int((objects_in_result['topleft'])['x']), int((objects_in_result['topleft'])['y'])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.6,
                    color=(255,255,200),
                    thickness=1,
                    lineType=cv2.LINE_AA)
        cv2.imshow('model output', imgcv)

    output = cv2.putText(imgcv, 'Town : ' + answer,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=2,
                color=(255, 255, 255),
                thickness=3,
                lineType=cv2.LINE_AA)

    cv2.imshow('model output', output)



print('session end')

