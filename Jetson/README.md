# The Jetson Program

This application runs on the Jetson Nano, which is the main computing unit of the robot.


ANALOG WRITE:

135 <-> 160 - 0  
165 - Start FWD  
130 - Start BKD
  
  
ESC PPM Config:  

Input deadband - 3%
lower limit = 0.1 us  
upper limit = 2 us  
mid limit = 1.1/1.2 us  


Parameters for diff_drive_controller package  
ticks_per_metere = 20  
wheel_separation = 1  
max_motor_speed = 20  