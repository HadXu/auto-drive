import io
import car_control
import os
os.environ['SDL_VIDEODRIVER'] = 'x11'

import pygame
from time import ctime,sleep,time

import threading
import numpy as np
import picamera
import picamera.array

global train_labels, train_img, is_capture_running, key


class SplitFrames(object):
    def __init__(self):
        self.frame_num = 0
        self.output = None

    def write(self, buf):
    	global key
    	if buf.startswith(b'\xff\xd8'):
            # Start of new frame; close the old one (if any) and
            # open a new output
            if self.output:
                self.output.close()
            self.frame_num += 1
            self.output = io.open('images/%s_image%s.jpg'%(key,time()), 'wb')
            self.output.write(buf)


def pi_capture():
    global train_img,train_labels,is_capture_running,key

    print('start capture')

    is_capture_running = True

    with picamera.PiCamera(resolution=(160,120), framerate=30) as camera:
        camera.start_preview()
        # Give the camera some warm-up time
        sleep(2)
        output = SplitFrames()
        start = time()
        camera.start_recording(output, format='mjpeg')
        camera.wait_recording(5)
        camera.stop_recording()
        finish = time()
        print('Captured %d frames at %.2ffps' % (
                output.frame_num,
                output.frame_num / (finish - start)))

    print('quit pi camera')
    is_capture_running = False

def my_car_control():
    global is_capture_running,key

    key = 4

    pygame.init()
    pygame.display.set_mode((1,1))
    car_control.carStraight()
    car_control.carStop()

    sleep(0.1)
    print('start control')

    while is_capture_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                key_input = pygame.key.get_pressed()
                print(key_input[pygame.K_w],key_input[pygame.K_a],key_input[pygame.K_d])

                if key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                    print('forward')
                    key = 2
                    car_control.carMoveForward()
                elif key_input[pygame.K_a]:
                	   print('left')
                	   car_control.carLeft()
                	   sleep(0.1)
                	   key = 0
                elif key_input[pygame.K_d]:
                	   print('right')
                	   car_control.carRight()
                	   sleep(0.1)
                	   key=1
                elif key_input[pygame.K_s]:
                	   print('back')
                	   car_control.carMoveBack()
                	   key = 3
                	
                	   
                
    car_control.clean()
    
if __name__ == '__main__':
    
    global train_labels,train_img,key
    print('start')

    print('*'*50)

    capture_thread= threading.Thread(target=pi_capture, args=())
    capture_thread.setDaemon(True)
    capture_thread.start()

    my_car_control()































