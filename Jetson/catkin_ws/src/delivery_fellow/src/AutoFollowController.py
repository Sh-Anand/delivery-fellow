import cv2
import jetson.utils

from Constants import *
from geometry_msgs.msg import Twist
from Motor import Motor
from MotorControl import MotorControl
from AutoFollow import AutoFollow
from Camera import Camera
from DiffDriveController import DiffDriveController
from threading import Thread


import time

class AutoFollowController:

    def __init__(self, auto_follow):#, debug_out=None):
        self.auto_follow = auto_follow
        self.diff_drive_controller = None
        self.ratio = CAMERA_MAX_TWIST_ANGULAR / CAMERA_MAX_TURN_ANGLE
        self.linear_slope = CAMERA_MAX_LINEAR / (CAMERA_MIN_SIZE - CAMERA_MAX_SIZE)
        self.linear_intercept = self.linear_slope * CAMERA_MAX_SIZE * -1
        self.debug_out = jetson.utils.videoOutput() #debug_out
        self.auto_follow_thread = None
        self.enabled = False
        self.timeout = None

    def start(self):
        while True:
            if not self.enabled:
                break
            steering = self.auto_follow.getSteering(debugOut=self.debug_out)
            print(steering)
            twist = Twist()
            if steering is None:
                self.diff_drive_controller.diff_drive(twist)
                continue
            turn_angle = self.transform_to_angular(steering[0][0])  # ((horizontal, vertical), size)
            if abs(turn_angle) <= CAMERA_DEADZONE:
                turn_angle = 0
            linear = self.transform_to_linear(steering[1])

            if linear == 0 and turn_angle != 0:
                linear = -1 * TWIST_BACK_CORRECTION

            twist.linear.x = linear
            twist.angular.z = turn_angle
            self.diff_drive_controller.diff_drive(twist)

    def set_diff_drive_controller(self, diff_drive_controller):
        self.diff_drive_controller = diff_drive_controller

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled and self.auto_follow_thread is None:
            self.auto_follow_thread = Thread(target=self.start, daemon=True)
            self.auto_follow_thread.start()
        else:
            self.auto_follow_thread = None

    def transform_to_angular(self, angle):
        return float(self.ratio * angle)

    def transform_to_linear(self, x):
        if x > CAMERA_MAX_SIZE:
            x = CAMERA_MAX_SIZE
        return (self.linear_slope * x) + self.linear_intercept

    def stop(self):
        self.diff_drive_controller.diff_drive(Twist())


if __name__ == "__main__":
    motor = None
    motor = Motor("/dev/ttyACM0")
    auto_follow = AutoFollow()
    auto_follow.setCamera(Camera('/dev/video0', angle=160, ratio=0.5))
    out = jetson.utils.videoOutput()
    diff_drive_controller = DiffDriveController(MotorControl(motor))
    auto_follow_controller = AutoFollowController(auto_follow)
    auto_follow_controller.enabled = True
    auto_follow_controller.set_diff_drive_controller(diff_drive_controller)
    auto_follow_controller.start()
