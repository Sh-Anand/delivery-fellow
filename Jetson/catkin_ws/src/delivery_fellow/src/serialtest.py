import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

ser.write(b"#1400,1400")

sleep(2)

ser.write(b"#1400,1800")

sleep(2)

ser.write(b"#1400,1400")

sleep(2)

ser.write(b"#1400, 1100")