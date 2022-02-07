import cv2
import numpy as np

def define_region(image):
	### black region
	if (len(image.shape) == 3): 
		height, length, _ = image.shape
	else:
		height, length = image.shape

	# Vertices array of the unwanted area --> bottom 1/3 of the picture
	region = [np.array([(0, height), (0, height//3), (length, height//3), (length, height)])]

	return region

def crop_frame(image):
	if (len(image.shape) == 3): 
		height, length, _ = image.shape
	else:
		height, length = image.shape
	return image[0: height//3*2, 0: length]

def mask_image(image, vertices):
	# fill unwanted area with zeros
	cv2.fillPoly(image, vertices, 0)
	return image

def detect_sign(image):
        sign_detected = False
        # load classifier
        stop_sign_ENG_cascade = cv2.CascadeClassifier('stop_sign_classifier_ENG.xml')
        stop_sign_ARB_cascade = cv2.CascadeClassifier('stop_sign_classifier_ARB.xml')

        img_filter = cv2.GaussianBlur(image, (5, 5), 0)
        gray_filered = cv2.cvtColor(img_filter, cv2.COLOR_BGR2GRAY)

        #stop_signs_ENG = stop_sign_ENG_cascade.detectMultiScale(gray_filered, scaleFactor=1.05, minNeighbors=30, minSize=(30, 30))
        stop_signs_ARB = stop_sign_ENG_cascade.detectMultiScale(gray_filered, scaleFactor=1.05, minNeighbors=25, minSize=(25, 25))

        #if len(stop_signs_ENG):
         #       print("ENGLISH STOP sign Detected")
          #      for (x,y,w,h) in stop_signs_ENG:
           #             image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 3)
            #            sign_detected = True
                
        if len(stop_signs_ARB):
                print("ARABIC STOP sign Detected")
                for (x,y,w,h) in stop_signs_ARB:
                        image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 3)
                        sign_detected = True

        if sign_detected:
                return True, image
        else:
                return False, image
    
