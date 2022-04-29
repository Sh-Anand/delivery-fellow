#!/usr/bin/python3
# Largely derived from https://github.com/Reinbert/teleop_twist_gamepad/blob/indigo-devel/src/teleop_twist_gamepad.cpp
import cv2
import jetson.utils
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

from AutoFollow import AutoFollow
from AutoFollowController import AutoFollowController
from Camera import Camera
from Constants import *
from Motor import Motor
from MotorControl import MotorControl
from DiffDriveController import DiffDriveController


class Controller:

    def __init__(self, diff_drive_controller, auto_follow_controller):
        # # Joystick controller inits for xbox one controller 
        # self.type = 'xbox_one'
        # self.axis_accel = 4
        # self.axis_brake = 5
        # self.axis_steer = 0
        # self.axis_speed_adj = 7
        # self.axis_angle_adj = 6
        # self.scale_accel = 1.0
        # self.scale_steer = 1.0
        # self.btn_deadman = 0
        # self.btn_af_switch = 3

        # Joystick controller inits for ps3 controller
        self.type = 'ps3'
        self.axis_accel = 1# self.axis_accel = 4
        self.axis_steer = 0
        self.btn_spped_up = 4
        self.btn_spped_dw = 6
        self.btn_angle_up = 5
        self.btn_angle_dw = 7
        self.btn_deadman = 14
        self.btn_af_switch = 15
        self.scale_accel = 1.0
        self.scale_steer = 1.0

        rospy.init_node("Controller")
        rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.diff_drive_controller = diff_drive_controller
        self.auto_follow_controller = auto_follow_controller
        self.auto_follow_controller.set_diff_drive_controller(self.diff_drive_controller)

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def joy_callback(self, joy_msg):
        if joy_msg.buttons[self.btn_af_switch]:
            print("TOGGLING TO AUTOFOLLOW")
            self.auto_follow_controller.toggle()

        else:
            cmd_msg = Twist()
            if self.type == 'xbox_one':
                if joy_msg.axes[self.axis_speed_adj]:
                    self.scale_accel += 0.1 * self.scale_accel * joy_msg.axes[self.axis_speed_adj]  # 1 up -1 down
                    print("ACCELERATION ADJUSTED TO " + str(self.scale_accel))

                elif joy_msg.axes[axis_angle_adj]:
                    self.scale_steer += 0.1 * self.scale_accel * -1 * joy_msg.axes[axis_angle_adj]  # 1 left -1 right
                    print("TURN SPEED ADJUSTED TO " + str(self.scale_steer))

                elif self.deadman < 0 or joy_msg.buttons[self.deadman] == 1:
                    vel = self.map(joy_msg.axes[self.axis_accel], 1, -1, 0, 1)
                    vel -= self.map(joy_msg.axes[self.axis_brake], 1, -1, 0, 1)

                    cmd_msg.linear.x = vel * self.scale_accel
                    cmd_msg.angular.z = joy_msg.axes[self.axis_steer] * self.scale_steer

                    self.pub.publish(cmd_msg)
                    self.diff_drive_controller.diff_drive(cmd_msg)

                else:
                    self.diff_drive_controller.diff_drive(cmd_msg)
            elif self.type == 'ps3':
                if joy_msg.buttons[self.btn_spped_up] == 1:
                    self.scale_accel += 0.1 * self.scale_accel
                    print('ACCELERATION ADJUSTED TO '+str(self.scale_accel))
                elif joy_msg.buttons[self.btn_spped_dw] == 1:
                    self.scale_accel -= 0.1 * self.scale_accel
                    print('ACCELERATION ADJUSTED TO '+str(self.scale_accel))
                elif joy_msg.buttons[self.btn_angle_up] == 1:
                    self.scale_steer += 0.1 * self.scale_steer
                    print('TURN SPEED ADJUSTED TO '+str(self.scale_steer))
                elif joy_msg.buttons[self.btn_angle_dw] == 1:
                    self.scale_steer -= 0.1 * self.scale_steer
                    print('TURN SPEED ADJUSTED TO '+str(self.scale_steer))

                elif self.btn_deadman < 0 or joy_msg.buttons[self.btn_deadman] == 1:
                    vel = joy_msg.axes[self.axis_accel]

                    cmd_msg.linear.x = vel * self.scale_accel
                    cmd_msg.angular.z = joy_msg.axes[self.axis_steer] * self.scale_steer

                    self.pub.publish(cmd_msg)
                    self.diff_drive_controller.diff_drive(cmd_msg)

                else:
                    self.diff_drive_controller.diff_drive(cmd_msg)
            else:
                print('Unsupported controller')
            


if __name__ == "__main__":
    # devices = list(list_ports.grep("[Aa]rduino"))
    motor = None
    motor = Motor("/dev/ttyACM0")
    auto_follow = AutoFollow()
    # auto_follow.setCamera(Camera('/dev/video0', angle=160, ratio=0.5))
    auto_follow_control = AutoFollowController(auto_follow)
    Controller(DiffDriveController(MotorControl(motor)), auto_follow_control)
    rospy.spin()
