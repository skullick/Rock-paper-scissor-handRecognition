import cv2
import cvzone 
import random
import time
from cvzone.HandTrackingModule import HandDetector

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

timer = 0
resultState = False
startGame = False
score = [0,0] 

model = HandDetector(maxHands=1)

while True:
    bg = cv2.imread("./BG.png")
    success, img = cam.read()
    resized_img = cv2.resize(img, (0,0), None, 0.875, 0.875)
    resized_img = resized_img[:,80:480]

    hands, hand_img = model.findHands(resized_img)
    if startGame:
        if resultState is False:
            timer = time.time() - initialTime
            cv2.putText(bg, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

            if timer>3:
                resultState = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = model.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1 #ROCK
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2 #PAPER
                    if fingers == [0,1,1,0,0] or fingers== [0,0,1,1,0]:
                        playerMove = 3 #SCISSORS

                    comMove = random.randint(1,3)
                    comImg = cv2.imread(f"./{comMove}.png", cv2.IMREAD_UNCHANGED)
                    bg = cvzone.overlayPNG(bg, comImg)

                    if(playerMove==1 and comMove==3) \
                        or (playerMove==2 and comMove==1) \
                        or (playerMove==3 and comMove==2):
                            score[0]+=1

                    if(playerMove==1 and comMove==2) \
                        or (playerMove==2 and comMove==3) \
                        or (playerMove==3 and comMove==1):
                            score[1]+=1

    bg[234:654,795:1195]=resized_img

    if resultState:
        bg=cvzone.overlayPNG(bg,comImg,(149,310))

    cv2.putText(bg, str(score[1]), (410,215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)
    cv2.putText(bg, str(score[0]), (1112,215), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 6)
    cv2.imshow("Rock Paper Scicssors", bg)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        resultState = False
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

        

