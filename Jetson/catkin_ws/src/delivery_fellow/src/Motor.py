import serial


class Motor:

    def __init__(self, device):
        self.device = device
        self.ser = serial.Serial(self.device, 9600, timeout=1)

    def drive(self, left, right):
        message = "#" + str(left) + "," + str(right)
        #print(message)
        self.ser.write(message.encode('utf-8'))

    def stop(self):
        self.ser.write("#1000,1000".encode('utf-8'))
