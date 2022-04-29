#! /usr/bin/env python
# Derived from https://github.com/merose/diff_drive

import rospy
from geometry_msgs.msg import Twist
from Constants import TICKS_PER_METER, WHEEL_SEPARATION, MAX_SPEED, TOPIC

class DiffDriveController:

    def __init__(self, motor_control, is_node=False):
        self.ticksPerMeter = TICKS_PER_METER
        self.wheelSeparation = WHEEL_SEPARATION
        self.maxMotorSpeed = MAX_SPEED

        self.motor_translator = motor_control

        if is_node:
            rospy.init_node('diff_drive_controller')
            rospy.Subscriber(TOPIC, Twist, self.diff_drive)

    def diff_drive(self, twist):
        speeds = self.get_speeds(twist.linear.x, twist.angular.z)
        self.motor_translator.move(speeds)

    def get_speeds(self, linear_speed, angular_speed):
        tickRate = linear_speed * self.ticksPerMeter
        diffTicks = angular_speed * self.wheelSeparation * self.ticksPerMeter

        speeds = [0, 0]
        speeds[0] = tickRate - diffTicks
        speeds[1] = tickRate + diffTicks

        # Adjust speeds if they exceed the maximum.
        if max(abs(speeds[0]), abs(speeds[1])) > self.maxMotorSpeed:
            factor = self.maxMotorSpeed / max(abs(speeds[0]), abs(speeds[1]))
            speeds[0] *= factor
            speeds[1] *= factor

        speeds[0] = int(speeds[0])
        speeds[1] = int(speeds[1])

        return speeds
