import lane_detection_module as ld
import sign_detection_module as sd
import cv2
import numpy as np
import serial
import sys
import time


class lane_detection(object):
    def __init__(self):
        """ Variables """
        self.latestImage = None
        self.cap = cv2.VideoCapture("https://192.168.43.243:8080/video")
        #self.cap = cv2.VideoCapture(0)

        # Serial port
        self.ser = serial.Serial('COM14', 9600)
        
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(3, 320)  # width=1920
        self.cap.set(4, 100)  # height=1080
        self.outputImage = None
        self.blurImage = None
        self.edgeImage = None

        self.sign_detected = False
        self.sign_nbr = 0
        
        self.kernel_size = 25
        self.low_threshold = 0
        self.high_threshold = 60
        self.rho = 1
        self.theta = np.pi/180
        self.threshold = 100
        self.min_line_len = 60
        self.max_line_gap = 80
        
        self.intersectionPoint = (0,  0)

        self.th = 50

    def ArduinoComm(self, axis, width):

        if width/2 - axis > self.th/2:
            print("left ")
            self.ser.write(b'L')
        elif width/2 - axis < -self.th/2:
            print("right " )
            self.ser.write(b'R')
        else:
            print("FORWARd ")
            self.ser.write(b'F')

        
    def run(self):
        time_start = 0
        lateral_search = 20 # number of pixels to search the line border
        start_height = 280 # Scan index row 235
        

        auto = True
        
        while True:
            # Only run loop if we have an image
            ret, self.latestImage = self.cap.read()
            if ret:
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('frame', 600, 640)
                # Rotate frame
                self.latestImage = cv2.rotate(self.latestImage, cv2.ROTATE_90_CLOCKWISE)
                # step 1: undistort image
                
                # step 2: perspective transform

                # step 3: detect Sign
                #self.sign_detected, self.latestImage = sd.detect_sign(self.latestImage)

                if self.sign_detected and time.time() > time_start + 5:
                    self.sign_nbr = self.sign_nbr + 1
                    print("SIGN NB : " + str(self.sign_nbr) + " STOP sign Detected")
                    time_start = time.time()
                    self.sign_detected = False
                    print("Stop " )
                    self.ser.write(b'S')
                
                # step 4: detect binary lane markings
                self.blurImage = ld.gaussian_blur(self.latestImage, self.kernel_size)
                self.edgeImage = ld.canny(self.blurImage, self.low_threshold, self.high_threshold)
                
                #Define region of interest for cropping
                height = self.latestImage.shape[0]
                width = self.latestImage.shape[1]
            
                vertices = np.array( [[
                        [4*width/6, 4*height/6],
                        [2*width/6, 4*height/6],
                        [20, height],
                        [width-20, height]
                ]], dtype=np.int32 )
            
                self.maskedImage = ld.region_of_interest(self.edgeImage, vertices)

                ret, thresh = cv2.threshold(self.maskedImage, 80, 255, cv2.THRESH_BINARY_INV)
                #thresh = 255-thresh
                signed_thresh = thresh[start_height].astype(np.int16)  # select only one row
                diff = np.diff(signed_thresh)  # The derivative of the start_height line

                points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative
                cv2.line(thresh,(0,start_height),(640,start_height),(0,255,0),1) # draw horizontal line where scanning

                if len(points) > 0 and len(points[0]) > 1: # if finds something like a black line
                    middle = np.mean(points[0])
                    print(middle)

                    cv2.circle(self.latestImage, (points[0][0], start_height), 10, (255,0,0), -1)
                    cv2.circle(self.latestImage, (points[0][1], start_height), 10, (255,0,0), -1)
                    cv2.circle(self.latestImage, (int(middle), int(start_height)), 2, (0,0,255), -1)

                    height, width, channels = self.latestImage.shape
                    cv2.line(self.latestImage, (int(width / 2)+self.th, 0), (int(width / 2)+self.th, int(height)), (0), 1)
                    cv2.line(self.latestImage, (int(width / 2)-self.th, 0), (int(width / 2)-self.th, int(height)), (0), 1)
 
                    if auto:
                        self.ArduinoComm(int(middle), width)
                    
                cv2.imshow('frame', self.latestImage)
                
        
            # press 'Q' if you want to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def main(args):
  Ld = lane_detection() 
  Ld.run() 
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
