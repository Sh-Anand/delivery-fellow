#!/usr/bin/python
# Largely derived from https://github.com/Reinbert/teleop_twist_gamepad/blob/indigo-devel/src/teleop_twist_gamepad.cpp

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from Constants import DEADMAN, ADJUST_SPEED, ADJUST_TURN
from Motor import Motor
from MotorControl import MotorControl
from DiffDriveController import DiffDriveController


class JoystickControl:

    def __init__(self, diff_drive_controller):
        self.axis_accel = 4
        self.axis_brake = 5
        self.axis_steer = 0
        self.scale_accel = 1.0
        self.scale_steer = 1.0
        self.disable_message_sent = False

        rospy.init_node("Joystick_Controller")
        rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.diff_drive_controller = diff_drive_controller

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def joy_callback(self, joy_msg):
        cmd_msg = Twist()
        if joy_msg.axes[ADJUST_SPEED]:
            self.scale_accel += 0.1 * self.scale_accel * joy_msg.axes[ADJUST_SPEED] # 1 up -1 down
            print("ACCELERATION ADJUSTED TO " + str(self.scale_accel))

        elif joy_msg.axes[ADJUST_TURN]:
            self.scale_steer += 0.1 * self.scale_accel * -1 * joy_msg.axes[ADJUST_TURN] # 1 left -1 right
            print("TURN SPEED ADJUSTED TO " + str(self.scale_steer))

        elif DEADMAN < 0 or joy_msg.buttons[DEADMAN]:
            vel = self.map(joy_msg.axes[self.axis_accel], 1, -1, 0, 1)
            vel -= self.map(joy_msg.axes[self.axis_brake], 1, -1, 0, 1)

            cmd_msg.linear.x = vel * self.scale_accel
            cmd_msg.angular.z = joy_msg.axes[self.axis_steer] * self.scale_steer

            self.disable_message_sent = False
            self.pub.publish(cmd_msg)
            self.diff_drive_controller.diff_drive(cmd_msg)

        elif not self.disable_message_sent:
            self.disable_message_sent = True
            self.diff_drive_controller.diff_drive(cmd_msg)

if __name__ == "__main__":
    # devices = list(list_ports.grep("[Aa]rduino"))
    motor = None
    motor = Motor("/dev/ttyACM0")
    JoystickControl(DiffDriveController(MotorControl(motor)))
    rospy.spin()