import numpy as np
import cv2

#cap = cv2.VideoCapture('test_video/trimmed_movement.mkv')        #use 0 as parameter to select first webcam
#cap = cv2.VideoCapture('test_video/trimmed_courtyard_movement_midday.mkv')
cap = cv2.VideoCapture('test_video/night_training.mkv')
#cap = cv2.VideoCapture(0)

cap.set(3,1280);    #width
cap.set(4,720);     #height
cap.set(5,10);      #fps

#convKernel = np.ones((3,3), np.float32)/9
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
fgbg = cv2.BackgroundSubtractorMOG(history=150, nmixtures=5, backgroundRatio=0.01)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
frameCounter = 0
frameList = []

while 1:
    #Read newest frame from webcam
    ret, frame = cap.read()
    croppedFrame = frame[250:600, 700:1100]
    frame = croppedFrame

    #frame = cv2.medianBlur(frame,5)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    #Denoise
    cv2.fastNlMeansDenoising(frame,frame,7,7,9)

    #frame = clahe.apply(frame)

    #Histogram Equalize
    cv2.equalizeHist(frame, frame)

    frame = cv2.medianBlur(frame,9)

    #frame = cv2.GaussianBlur(frame,(5,5),0)
    #ret3,th3 = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #ret2,th2 = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #frame = th2
    #frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    #frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,7)

    frameCounter += 1

    #insert the current frame
    #frameList.append(frame)
    #Only Start denoising after the list if full
    #if (frameCounter > maxFramesToStore):
        #remove the oldest frame
        #frameList.pop(0)
        #frame = cv2.fastNlMeansDenoisingMulti(frameList, maxFramesToStore-1, maxFramesToStore, None, 4, 7, 35)



    #Crop frame in order to ignore noise from trees/lighting
    #croppedFrame = frame[250:400, 800:1000]

    #Convert to grayscale
    #bCrop = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2GRAY)



    #Blur
    #frame = cv2.GaussianBlur(frame,(13,13),0)
    #croppedFrame = cv2.dilate(croppedFrame,(9,9))



    #Background Subtraction
    fgmask = fgbg.apply(frame)
    #fgmask = cv2.dilate(fgmask,(13,13))
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    #Get position of person
    #hist = cv2.calcHist([fgmask],[0],None,[2],[0, 256])
    #minValue, maxValue, minPosition, maxPosition = cv2.GetMinMaxHistValue(hist)
    #print("Max Value:", maxValue, maxPosition)
    #print("Min value:", minValue, minPosition)

    #Minimize effect of shadow by eroding image
    #cv2.erode(fgmask, fgmask, (3,3), )

    #subFrame = fgmask
    #cv2.imshow('raw', rawFrame)
    #cv2.imshow('th3', th3)
    cv2.imshow('frame',frame)
    #cv2.imshow('proc', pCrop)
    cv2.imshow('background subtraction', fgmask)
    #cv2.imshow('bw crop', bCrop)
    #cv2.imshow('fgmask',fgmask)
    #cv2.imshow('thresh', thresh)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


    # def runSentences(self):
    #     self.sentence = ""
    #     deltaChars = 1
    #     self.sentenceSurface = self.makeSentence(self.sentence)
    #     loopCount = 0
    #     self.fps = 16
    #     self.running = True
    #     self.sentenceBuffer = ""
    #     self.crazyColorMode = False
    #     while self.running:
    #         for event in pygame.event.get():
    #             if hasattr(event, 'key') and event.key == 27:
    #                 self.running = False
    #             if event.type == pygame.KEYDOWN:
    #                 if (event.key == pygame.K_KP_MINUS):
    #                     self.fps -= 1
    #                     if (fps <= 0): fps = 1
    #                     print("Speed: " + self.fps)
    #                 elif (event.key == pygame.K_KP_PLUS):
    #                     self.fps += 1
    #                     print("Speed: " + self.fps)
    #                 else:
    #                     self.sentenceBuffer += chr(event.key)
    #         prevTime = pygame.time.get_ticks()
    #
    #         self.drawSurface(self.sentenceSurface)
    #
    #         self.sentenceSurface.scroll(dx=-deltaChars)
    #         loopCount += 1
    #         # If a char just passed by
    #         if (loopCount % 6 == 0):
    #             #if self.crazyColorMode:
    #                 #self.backgroundColor = self.randomColor() #Uncomment to make every character have a different background color
    #             self.sentence = self.sentence + self.sentenceBuffer
    #             self.sentence = self.sentence[deltaChars:]
    #             self.sentenceBuffer = ""
    #             self.sentenceSurface = self.makeSentence(self.sentence)
    #
    #         self.updatePreview()
    #        self.clock.tick(self.fps)





