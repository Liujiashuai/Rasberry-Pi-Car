import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import time
from enum import Enum
import copy

from picamera.array import PiRGBArray
from picamera import PiCamera

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared
from camera import CarCamera
from track import CarDetect

GPIO.setwarnings(False)  # Disable warning
GPIO.setmode(GPIO.BCM)  # BCM coding


# # 远程调试用代码,如果不使用pycharm进行调试，请注释该段代码
# import sys
#
# sys.path.append("pydevd_pycharm.egg")
# import pydevd_pycharm
#
# pydevd_pycharm.settrace('192.168.12.162', port=20000, stdoutToServer=True, stderrToServer=True)
#
#
# # =======================


class CarState(Enum):
    stop = 0
    go = 1
    fast_go = 2
    light_left = 3
    left = 4
    heavy_left = 5
    light_right = 6
    right = 7
    heavy_right = 8


class Car(CarMove, CarUltrasound, CarInfrared, CarCamera, CarDetect):  # create class Car, which derives all the modules
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)
        CarCamera.__init__(self)
        CarDetect.__init__(self)
        self.state = CarState.stop

    def AllStop(self):
        self.state = CarState.stop
        CarMove.MotorStop(self)
        CarCamera.CameraCleanup(self)
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        car = Car()

        VideoReturn = True
        num_lane_point = 8   # the number of detected points on the lane
        
        turn_right_speed = 50
        turn_left_speed = 50
        forward_speed = 40
        speed_high = 50
        speed_low = 10

        ForB = 'Forward'
        LorR = 'Brake'

        camera, rawCapture = car.CameraInit()  # Initialize the PiCamera
        for raw_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame_origin = raw_frame.array

            ################## lane detection ##############################################
            img = cv2.blur(frame_origin, (5, 5))  # denoising
            blu_img, _, red_img = cv2.split(img)  # extract the red channel of the RGB image (since the lane in our experiment is blue or black)
            # gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # rgb to gray
            
            _, dst = cv2.threshold(blu_img,  30, 255, cv2.THRESH_BINARY)  # binaryzation, the thresold deponds on the light in the environment

            height, width = dst.shape
            print(height, width)
            half_width = int(width/2)
            

            all_line_pos = np.zeros((num_lane_point, 1))

            img_out = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
            for i in range(num_lane_point):   # each detected point on the lane
                detect_height = height - 20 * (i+1)
                detect_area_all = dst[detect_height, 0: width-1]
                line_all = np.where(detect_area_all == 0)

                if len(line_all[0]):
                    all_line_pos[i] = int(np.max(line_all) + np.min(line_all)) / 2
                else:
                    all_line_pos[i] = -1

                if all_line_pos[i] >= 0:   # draw the lane points on the binary image
                    img_out = cv2.circle(img_out, (all_line_pos[i], detect_height), 4, (0, 0, 255), thickness=10)

            if VideoReturn:  # detect the tennis & transmit the frames to PC
                car.VideoTransmission(img_out)

            ############################ decision making #####################################
            all_mean = np.median(all_line_pos) # choose the most internal lane point for decision making

            if all_mean < 0:
                ForB = 'Backward'
            else:  #if line is on the left, turn left and fo straight
                ForB = 'Forward'
            # print("the result", ForB, LorR)

            ############################ motion control #####################################
            if ForB is 'Forward':
                vleft = speed_low + (speed_high-speed_low)/width * all_mean
                vright = speed_high + (speed_low-speed_high)/width * all_mean
                print("all_mean", all_mean, "v_left", vleft, "v_right", vright)
                car.forward_turn(vleft, vright)
            elif ForB is 'Backward':
                car.back(25)

            rawCapture.truncate(0)  # PiCamera必备

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()

    except:
        print("stop")
        car.AllStop()

