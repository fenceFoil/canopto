import cv2
import threading


class PersonTracker(threading.Thread):
    def __init__(self):
        #Setup threading
        threading.Thread.__init__ ( self )

        #Person location
        self.personLocation = [0, 0]

        self.initialROI = [88, 20, 136, 20]
        self.trackWindow = []

        #crop out trees...
        self.crop_y = [300, 525]
        self.crop_x = [805, 1050]

        #Video capture mode
        self.cap = cv2.VideoCapture(0)
        # Testing videos at different times of the day (lighting was primary problem)
        #cap = cv2.VideoCapture('test_video/trimmed_movement.mkv')  # use 0 as parameter to select first webcam
        # cap = cv2.VideoCapture('test_video/trimmed_courtyard_movement_midday.mkv')
        # cap = cv2.VideoCapture('test_video/night_training.mkv')

        # Webcam Settings
        self.cap.set(3, 1280);  # width
        self.cap.set(4, 720);  # height
        self.cap.set(5, 10);  # fps

        # Used to estimate frames per second
        self.frameCounter = 0

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
        self.trackWindow = [x, y, w, h]

    def setTrackingPosition(self):
        """
        Reset the Tracker to the initial default position
        :return: None
        """
        self.trackWindow = self.initialROI

    def reportPosition(self):
        return self.personLocation

    def run(self):
        # take first frame of the video
        ret, frame = self.cap.read()

        # Crop
        frame = frame[self.crop_y[0]:self.crop_y[1], self.crop_x[0]:self.crop_x[1]]

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
        # cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        while self.running:
            # Read newest frame from webcam
            ret, frame = self.cap.read()
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # cv2.fastNlMeansDenoising(frame,frame,7,7,9)
            # cv2.equalizeHist(frame, frame)
            self.frameCounter += 1

            # Crop
            frame = frame[self.crop_y[0]:self.crop_y[1], self.crop_x[0]:self.crop_x[1]]

            if ret == True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

                # apply meanshift to get the new location
                ret, track_window = cv2.meanShift(dst, track_window, term_crit)

                # Draw it on image
                if len(self.trackWindow) == 0:
                    x, y, w, h = track_window
                else:
                    x, y, w, h = self.trackWindow

                img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
                cv2.imshow('img2', frame)

                self.personLocation = [x, y]

                # Close when escape key is pressed
                k = cv2.waitKey(60) & 0xff
                if k == 27:
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
    #time.sleep(2)
    #tracker.setTrackingPosition(10,10,10,10)