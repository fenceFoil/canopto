import cv2
import threading
import numpy as np
import time


class PersonTracker(threading.Thread):
    def __init__(self, display=None):
        #Setup threading
        threading.Thread.__init__ ( self )

        #Person location
        self.personLocation = [0, 0]

        self.display = display

        self.initialROI = (135, 40, 130, 40)
        self.trackWindow = []

        #crop out trees...
        self.crop_y = [300, 525]
        self.crop_x = [805, 1050]

        #Video capture mode
        self.cap = cv2.VideoCapture(0)
        #Testing videos at different times of the day (lighting was primary problem)
        #self.cap = cv2.VideoCapture('test_video/trimmed_movement.mkv')  # use 0 as parameter to select first webcam
        #self.cap = cv2.VideoCapture('test_video/trimmed_courtyard_movement_midday.mkv')
        self.cap = cv2.VideoCapture('test_video/night_training.mkv')
        #self.cap = cv2.VideoCapture('test_video/night_training_2.mp4')

        # Webcam Settings
        self.cap.set(3, 1280);  # width
        self.cap.set(4, 720);  # height
        self.cap.set(5, 10);  # fps

        # Used to estimate frames per second
        self.frameCounter = 0

        #Set to true to reorient the trackign window onto the section of the image that last moved
        self.resetToMotion = False
        self.resetBS = False

        self.running = True

    def setTrackingPosition(self, x, y, w, h):
        """
        Change the focus of the tracker to the given position and size
        :param x: x coordinate to focus on
        :param y: y coordinate to focus on
        :param w: width of the tracking box
        :param h: height of the tracking box
        :return: None
        """
        self.trackWindow = (x, y, w, h)

    def resetTrackingPosition(self):
        """
        Reset the Tracker to the initial default position
        :return: None
        """
        self.trackWindow = self.initialROI

    def reportPosition(self):
        return self.personLocation
    #
    # def setup(self):
    #     ret, frame = self.cap.read()
    #     fgbg = cv2.BackgroundSubtractorMOG2()
    #     frame = frame[self.crop_y[0]:self.crop_y[1], self.crop_x[0]:self.crop_x[1]]
    #     fgmask = fgbg.apply(frame)
    #     cv2.medianBlur(fgmask, 13, fgmask)
    #     frame = fgmask
    #     r, h, c, w = self.initialROI
    #     track_window = (c, r, w, h)
    #
    #
    def run(self):
        # take first frame of the video
        ret, frame = self.cap.read()
        fgbg = cv2.BackgroundSubtractorMOG2()

        # Crop
        frame = frame[self.crop_y[0]:self.crop_y[1], self.crop_x[0]:self.crop_x[1]]

        #Helps with detecing during daylight but causes excess noise
        #bFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.equalizeHist(bFrame, bFrame)
        #frame = bFrame
        #frame = cv2.cvtColor(frame,bFrame,cv2.COLOR_GRAY2BGR)

        #cv2.dilate(bFrame,(9,9),bFrame)
        fgmask = fgbg.apply(frame)
        cv2.medianBlur(fgmask, 13, fgmask)
        frame = fgmask
        #frame = cv2.normalize(frame,frame, alpha=0,norm_type=cv2.NORM_MINMAX, beta = 255)

        #Image Processing
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.fastNlMeansDenoising(frame,frame,7,7,9)
        #cv2.equalizeHist(frame, frame)

        # Region of interest(ROI) location
        # row, height, column, width
        r, h, c, w = self.initialROI
        track_window = (c, r, w, h)

        # set up the ROI for tracking
        roi = frame[r:r + h, c:c + w]
        # cv2.imshow('roi', roi)
        # hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([frame], [0], None, [180], [0, 180])
        # roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        #cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        #roi = frame[r:r+h, c:c+w]
        #hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        #roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        #cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


        while self.running:

            # Read newest frame from webcam
            ret, frame = self.cap.read()
            self.frameCounter += 1
            #cv2.fastNlMeansDenoising(frame,frame,7,7,9)

            # Crop
            frame = frame[self.crop_y[0]:self.crop_y[1], self.crop_x[0]:self.crop_x[1]]
            rawCrop = frame

            #cv2.dilate(bFrame,(9,9),bFrame)
            fgmask = fgbg.apply(frame)
            #cv2.GaussianBlur(fgmask,(9,9),2, fgmask)
            #frame = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)
            cv2.medianBlur(fgmask, 13, fgmask)
            #cv2.equalizeHist(fgmask, frame)
            frame = fgmask

            #bFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            #bFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.equalizeHist(bFrame, bFrame)
            #frame = bFrame
            frame = cv2.normalize(frame,frame, alpha=0,norm_type=cv2.NORM_MINMAX, beta = 255)

            #
            if self.resetBS:
                fgbg = cv2.BackgroundSubtractorMOG2()
                self.resetBS = False

            if self.resetToMotion:
                #print "PersonTracker file: Resetting to motion"
                points = [np.intersect1d(np.where((frame > 100))[0], np.where((frame < 150))[0]), np.intersect1d(np.where((frame > 100))[1], np.where((frame < 150))[1])]
                if (len(points[0]) > 0 and len(points[1]) > 0):
                    print points
                    self.resetToMotion = False
                    print "Now tracking:", points[0][1], points[1][1]
                    self.setTrackingPosition(points[1][1], points[0][1], 40, 40)



            if ret == True:
                #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                #dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
                dst = cv2.calcBackProject([frame], [0], roi_hist, [0, 180], 1)

                #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                #dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

                # apply meanshift to get the new location
                if len(self.trackWindow) == 0:
                    ret, track_window = cv2.meanShift(dst, track_window, term_crit)
                else:
                    print "Setting tracking window to new location:", self.trackWindow
                    ret, track_window = cv2.meanShift(dst, self.trackWindow, term_crit)
                    self.trackWindow = []

                # Draw it on image
                x, y, w, h = track_window


                img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
                cv2.imshow('img2', frame)
                #cv2.imshow('crop', rawCrop)
                #cv2.imshow('bframe', bFrame)
                #cv2.imshow('fgmask', fgmask)

                self.personLocation = [x, y]

                # Close when escape key is pressed
                k = cv2.waitKey(60) & 0xff
                if k == 27:
                    self.running = False
                    break
            else:
                break
        self.destroy()

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = PersonTracker()
    PersonTracker.start(tracker)
    time.sleep(2)
    tracker.resetToMotion = True
    #tracker.setTrackingPosition(10,10,10,10)