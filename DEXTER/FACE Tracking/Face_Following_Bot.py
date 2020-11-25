import cv2
import serial
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)

ser = serial.Serial('COM5', 9600)
time.sleep(1)

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def ArduinoComm(difference, axis, axisWidth, rectangle):

    speed = bytes(str(int(map(difference, 0, axisWidth / 2, 170, 220))), 'utf-8')

    if axisWidth/2 - axis > 50:
        ser.write(b'#L' + speed + b'n')
    elif axisWidth/2 - axis < -50:
        ser.write(b'#R' + speed + b'n')
    else:
        speed = b'120'
        if rectangle > 6000:
            ser.write(b'#B' + speed + b'n')
        elif rectangle < 5000:
            ser.write(b'#F' + speed + b'n')
        else:
            ser.write(b'#B0n')





def faceDetFoll():
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 4)
        height, width, channels = frame.shape
        cv2.line(frame, (0, int(height / 2)), (int(width), int(height / 2)), (255, 255, 255), 1)
        cv2.line(frame, (int(width / 2), 0), (int(width / 2), int(height)), (255, 255, 255), 1)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            x_axis = int(x + (w / 2))
            y_axis = int(y + (h / 2))

            rectsize = w*h
            print(rectsize)
            cv2.circle(frame, (x_axis, y_axis), 5, (0, 0, 255), -1)

        cv2.imshow('Face detection', frame)

        if len(faces):
            xDef = abs(int(width/2) - x_axis)
            #print(xDef)

            ArduinoComm(xDef, x_axis, width, rectsize)

            #print(x_axis, end=' ')
            #print(y_axis)
        else:
            ser.write(b'#R0n')

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
