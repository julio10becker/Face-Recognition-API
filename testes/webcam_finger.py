import numpy as np
import cv2
from keras.models import model_from_json
from keras.preprocessing import image

#loading the model
json_file = open('count_fingers.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("count_fingers.h5")
print("Loaded model from disk")

#defining the list of all the numbers in order which they are trained

numbers = ['FIVE', 'FOUR', 'NONE', 'ONE', 'THREE', 'TWO']

#Turning on the camera for live feed

cap = cv2.VideoCapture(0)
while True:
    _,frame = cap.read()
    frame = cv2.flip(frame,1)
    altura = frame.shape[0]
    comprimento = frame.shape[1]
    
    #Converting the frame to Gray scale    
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #Drawing a rectangle for taking in the image in roi
    cv2.rectangle(frame,(0,0), (int(comprimento/2), int(altura/2)),(0,255,0),3)
 
    #creating the roi
    roi = frame_gray[0:int(altura/2), 0:int(comprimento/2)]  
    #Resizing the image
    roi = cv2.resize(roi,(64,64))
    
    #Processing the image before making the predictions from the model
    blur = cv2.GaussianBlur(roi, (7,7), 3)
    ad_thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    ret, thres = cv2.threshold(ad_thres, 25, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    #Converting the image into array
    image_array = image.img_to_array(thres)
    
    #Converting the image from (64,64,1) to (64,64,3)
    image_array = cv2.cvtColor(image_array,cv2.COLOR_GRAY2BGR)
    image_array = np.expand_dims(image_array,axis =0)
    
    #Making predictions with the model
    predictions =loaded_model.predict(image_array)
    
    #Printing the predcitions on the screen
    cv2.putText(frame,numbers[np.argmax(predictions)],(1,450), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2)
    cv2.imshow('Frame',frame)
    
    k =cv2.waitKey(15)
    if k ==27:
        break
cap.release()
cv2.destroyAllWindows()
