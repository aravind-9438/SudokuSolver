import cv2
import numpy as np 
# from tensorflow.keras.models import load_model

 

def preprocess(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgthreshold = cv2.adaptiveThreshold(imgBlur,255,1,1,11,2)
    return imgthreshold


def biggestContour(contours):
    biggest = np.array([])
    maxArea = 0
    for i in contours:
        area = cv2.contourArea(i)
        if(area>50):
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            if(area>maxArea and len(approx)==4):
                biggest = approx
                maxArea = area
    return biggest,maxArea


def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    newmyPoints = np.zeros((4,1,2), dtype=np.int32)
    add = myPoints.sum(1)
    newmyPoints[0] = myPoints[np.argmin(add)]
    newmyPoints[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    newmyPoints[1] = myPoints[np.argmin(diff)]
    newmyPoints[2] = myPoints[np.argmax(diff)]
    return newmyPoints
 


def splitBoxes(img):
    rows = np.vsplit(img,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        for box in cols:
            boxes.append(box)
    return boxes

# def intializemodel():
#     model = load_model("MyModel.h5")
#     return model

def getPrediction(boxes,model):
    result = []
    for i in boxes:
        img = np.asarray(i)
        img = img[4:img.shape[0]-4,4:img.shape[1]-4]
        img = cv2.resize(img,(28,28))
        img = img/255
        img = img.reshape(1,28,28,1)
        
        predictions = model.predict(img)
        
        idx = np.argmax(predictions, axis=-1)
        prob = np.amax(predictions)
        
        if(prob>0.8):
            result.append(idx[0])
        else:
            result.append(0)
    
    return result
 
def displayNumbers(img,numbers,color = (255, 102, 0)):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for x in range (0,9):
        for y in range (0,9):
            if numbers[(y*9)+x] != 0 :
                 cv2.putText(img, str(numbers[(y*9)+x]),
                               (x*secW+int(secW/2)-10, int((y+0.8)*secH)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            2, color, 2, cv2.LINE_AA)
    return img

def drawGrid(img):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (0, 255, 0),2)
        cv2.line(img, pt3, pt4, (0, 255, 0),2)
    return img
