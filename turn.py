from pybricks.tools import wait, StopWatch
from parameters import *
from umath import pi

def turn(set_point, absolute = True, kp = 11, kd = 2, ki = 0.03):
    if absolute == False:
        hub.imu.reset_heading(0)

    time = StopWatch()
    time.time()
    
    left_wheel_motors.reset_angle(0)
    right_wheel_motors.reset_angle(0)

    angle = hub.imu.heading()
    error = set_point - angle
    last_error = 0
    last_time = 0
    count = 0

    while abs(error) > 0.5: 
        current_time = time.time()
        angle = hub.imu.heading()

        error = set_point - angle
        
        p = kp * error
        d = (error - last_error) / max((current_time - last_time), 1e-3) * kd

        if error <= 5:
            count += error

        i = count * ki

        correction = p + d + i
        
        if abs(error) == 0:
            correction = 0

        right_wheel_motors.run(-correction)
        left_wheel_motors.run(correction)

        last_error = error 
        last_time = time.time()
