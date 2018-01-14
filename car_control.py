import RPi.GPIO as GPIO
import time


backInput1 = 7
backInput2 = 11

frontInput1 = 13
frontInput2 = 15

change = 12

change2 = 16

speed = 15

GPIO.setmode(GPIO.BOARD)

GPIO.setup(backInput1,GPIO.OUT)
GPIO.setup(backInput2,GPIO.OUT)
GPIO.setup(change,GPIO.OUT)
GPIO.setup(change2,GPIO.OUT)


GPIO.setup(frontInput1,GPIO.OUT)
GPIO.setup(frontInput2,GPIO.OUT)

backMotorPwm = GPIO.PWM(change,100)
backMotorPwm.start(0)

def carStop():
    GPIO.output(backInput1,GPIO.LOW)
    GPIO.output(backInput2,GPIO.LOW)

def carMoveForward():
    carStraight()
    GPIO.output(backInput1,GPIO.LOW)
    GPIO.output(backInput2,GPIO.HIGH)
    
    backMotorPwm.ChangeDutyCycle(speed)
    
def carMoveBack():
    GPIO.output(backInput1,GPIO.HIGH)
    GPIO.output(backInput2,GPIO.LOW)
    backMotorPwm.ChangeDutyCycle(speed)


def carStraight():
    GPIO.output(change2,GPIO.LOW)

def carRight():
    GPIO.output(change2,GPIO.HIGH)
    GPIO.output(frontInput1,GPIO.LOW)
    GPIO.output(frontInput2,GPIO.HIGH)

def carLeft():
    GPIO.output(change2,GPIO.HIGH)
    GPIO.output(frontInput1,GPIO.HIGH)
    GPIO.output(frontInput2,GPIO.LOW)
    
    
def clean():
    GPIO.cleanup()
    backMotorPwm.stop()

if __name__ == '__main__':
    carMoveForward()
    
    time.sleep(2)
    
    carStop()
    
    carStraight()
    carLeft()
    time.sleep(2)
    carStraight()
    
    clean()
