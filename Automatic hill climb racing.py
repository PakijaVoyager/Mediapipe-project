import cv2 #Importing for real time computer vision
import mediapipe as mp #Importing for detecting hands and fingers
import time #Importing for using sleep function
from directKeys import PressKey, ReleaseKey #Importing for controlling whether the key is presssed or not
from directKeys import right_pressed,left_pressed #Importing for forward and backward motion

# These are two variables contain values for forward and backward motions
break_key_pressed = left_pressed
accelerato_key_pressed = right_pressed

time.sleep(2.0)
#Stores whether key is pressed or not
current_key_pressed = set()

# For capturing the frames
cap = cv2.VideoCapture(0)

# These lines of code contain the submodule (solutions) and method (hand,Hands(),drawing utils) for detection of hand and drawing landmark on it
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
tipsFinger = [4,8,12,16,20]
while True:
    # Initially all the values are False
    keyPressed = False
    break_pressed = False
    accelerator_pressed = False
    key_count = 0
    key_pressed = 0

    #Capturing the frames and converting into RGB
    ret,frame = cap.read()
    imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    #The processed RGB value is put on the result variable
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    lmList = []
    #Detecting multiple hand landmarks
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Iterating over the id and (x,y) values of each landmarks on hand
            for id,lm in enumerate(handLms.landmark):
                h,w,c = frame.shape #Storing the width,height,channel on hwc variable
                cX,cY = int(lm.x*w),int(lm.y*h) #Converting the floating value into actual height and width (in pixel format)
                lmList.append([id,cX,cY]) #Appending converted value in the empty list.

            mpDraw.draw_landmarks(frame,handLms,mpHands.HAND_CONNECTIONS) #Drawing landmark in real time in each pixel captured from the frame
    fingers = [] #It stores 1 and 0 value for determining the number of finger up
    if len(lmList) != 0:
        if lmList[tipsFinger[0]][1] > lmList[tipsFinger[0]-1][1]: #If hand's index number 4 x-coordinate is bigger than y-coordinate then finger is up  ---
            fingers.append(1)
        else:
            fingers.append(0) # else down
        for id in range(1,5):
            if lmList[tipsFinger[id]][2] < lmList[tipsFinger[id]-2][2]: #Similarly if hand's tip indexes y-coordinate is smaller tip-2 indexes y-coordinate then finger is up
                fingers.append(1)
            else: #else fingers is down
                fingers.append(0)
    total = fingers.count(1) #It counts the number of up finger
    if total == 0: #If no fingeres are up then automatically brake will be applied
        cv2.rectangle(frame, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 5)
        #Passing the parameter in order to apply break
        PressKey(break_key_pressed)
        break_pressed = True
        current_key_pressed.add(break_key_pressed)
        key_pressed = break_key_pressed
        keyPressed = True
        key_count = key_count + 1

    elif total == 5: #else gas will be applied
        cv2.rectangle(frame, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, "  GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
        #Passing the parameter to accelerate
        PressKey(accelerato_key_pressed)
        key_pressed = accelerato_key_pressed
        accelerator_pressed = True
        keyPressed = True
        current_key_pressed.add(accelerato_key_pressed)
        key_count = key_count + 1


    # These part of code is extracted from directKeys.python
#####################################################################################
    if not keyPressed and len(current_key_pressed) != 0:
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()
    elif key_count == 1 and len(current_key_pressed) == 2:
        for key in current_key_pressed:
            if key_pressed != key:
                ReleaseKey(key)
        current_key_pressed = set()
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()
######################################################################################
    print(total)
    cv2.imshow("Window",frame)
    # print(lmList)
    if cv2.waitKey(1) & 0xFF == 27:
        break
print(lmList)
hands.close()
cap.release()
cv2.destroyAllWindows()