from Motor import Motor
from Constants import MIN_MOTORS, MAX_MOTORS, MAX_SPEED


class MotorControl:

    def __init__(self, motors):
        self.motors = motors

        self.k = float((MAX_MOTORS - MIN_MOTORS) / (2 * MAX_SPEED))
        self.c = float((MAX_MOTORS + MIN_MOTORS) / 2)

    def translate(self, speed):
        # return k*speed + c
        return int(self.k * speed + self.c)

    def move(self, data):
        print(self.translate(data[0]), '\t-\t', self.translate(data[1]))
        #print("#")
        self.motors.drive(self.translate(data[0]), self.translate(data[1]))
