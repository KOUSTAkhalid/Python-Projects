from DataSaver import save_to_file
from tracker import *
import threading
import cv2
import sys

#  function called by trackbar, sets the threshold
def setThreshold(val):
    global threshold
    threshold = max(val,1)

def ApplyThresh(frame):
    # Convert frame to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply gaussian blur
    Gauss = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply threshold, any pixel value that is greater than 'threshold' is set to 0. Any value that is less than 'threshold' is set to 255.
    thresh = cv2.threshold(Gauss, threshold, 255, cv2.THRESH_BINARY_INV)[1]

    return thresh


# Create tracker object
tracker = EuclideanDistTracker()

if __name__ == '__main__' :
    
    # Read video
    cap = cv2.VideoCapture('Examples/Example 1.mp4')
    cv2.namedWindow("Foreground detection")

    if cap.isOpened():
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        dim = (width, height)
        
        print('Original Dimensions : ',dim)
        scale_percent = 70 # percent of original size
        width = int(width * scale_percent / 100)
        height = int(height * scale_percent / 100)
        dim = (width, height)
        
        print('Resized Dimensions : ',dim)

        # Get video duration
        fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        N_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = N_frames/fps
        frame_count = 0

    else:
        # Exit if video not opened.
        print("Could not open video")
        sys.exit()

    # set threshold
    threshold = 170
    # add trackbar
    cv2.createTrackbar("Threshold", "Foreground detection", threshold, 255, setThreshold)
    
    while cv2.getWindowProperty('Foreground detection', 0) >= 0:
        # Read a new frame
        ok, frame = cap.read()
        
        if not ok:
            break

        frame_count += 1
        
        # Resize the frame
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        # Apply thrshold to frame
        mask = ApplyThresh(frame)

        # Apply the Foreground detection algorithm to the frame

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 100:
                #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id

            # Calculate play time of video
            play_time = int((frame_count/ fps) * 1000)

            # Save data to a text file, this tasks runs simultaneously with the Main script
            save_to_txt = threading.Thread(target=save_to_file, args=(id, (x, y), (w, h), play_time,))
            save_to_txt.start()
            #save_to_txt.join()
            
            cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
        cv2.imshow('Foreground detection', frame)
        #cv2.imshow('Foreground detection', mask)

        k = cv2.waitKey(20) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.release()
