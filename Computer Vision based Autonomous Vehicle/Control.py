import RPi.GPIO as GPIO

def Forward(spd):
    pwm1.ChangeDutyCycle(spd)
    pwm2.ChangeDutyCycle(spd)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)
    
def Backward(spd):
    pwm1.ChangeDutyCycle(spd)
    pwm2.ChangeDutyCycle(spd)
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)
    
def Left(spd):
    pwm1.ChangeDutyCycle(spd)
    pwm2.ChangeDutyCycle(spd)
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)
    
def Right(spd):
    pwm1.ChangeDutyCycle(spd)
    pwm2.ChangeDutyCycle(spd)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)
    
def Stop():
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

EnA = 2
in1 = 3
in2 = 4

EnB = 14
in3 = 15
in4 = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(EnA, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(EnB, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

Stop()

speed = 25

pwm1 = GPIO.PWM(EnA, 1000)
pwm2 = GPIO.PWM(EnB, 1000)

pwm1.start(speed)
pwm2.start(speed)
