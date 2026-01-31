from pybricks.tools import wait, StopWatch
from new import *
from umath import pi

def calculate_distance():
    left_wheel_angle = left_wheel_motors.angle()  
    right_wheel_angle = right_wheel_motors.angle() 
    perimetr = WHEEL_DIAMETER * pi
    
    avg_angle = (left_wheel_angle + right_wheel_angle) / 2

    wheel_turns = avg_angle / 360
    drive_distance = wheel_turns * perimetr
    return drive_distance


def moving_profile(distance, max_velocity, acceleration, set_point, absolute = True, kp = 8, kd = 2):

    direction = 1 if max_velocity >= 0 else -1

    distance = abs(distance)
    max_velocity = abs(max_velocity)
    acceleration = abs(acceleration)


    if not absolute:
        hub.imu.reset_heading(0)

    time = (abs(max_velocity)) / acceleration
    triangle = 0.5 * (acceleration * time ** 2)
    drive_base.stop()

    left_wheel_motors.reset_angle(0)
    right_wheel_motors.reset_angle(0)
    timer = StopWatch()
    
    MIN_REMAIN_MM = 0.5
    MIN_SPEED_MM_S = 5.0
    current_speed = 0.0
    start_distance_0 = 0
    velocity_0 = 0.0
    upperBase = distance - triangle*2
    after_acceleration = triangle
    before_deceleration = upperBase + triangle
    last_time = 0
    last_error = 0 

    while True: 
        angle = hub.imu.heading()
        error = set_point - angle

        current_time = timer.time()
        dt = max(1e-3, (current_time - last_time) / 1000.0)
        passed = calculate_distance()
        remain = max(0.0, distance - abs(passed))

        p = error * kp
        d = (error - last_error) / max((current_time - last_time), 1e-3) * kd
        correction = p + d

        if remain <= MIN_REMAIN_MM and current_speed <= MIN_SPEED_MM_S:
            break

        d_brake = (current_speed * current_speed) / (2 * acceleration)

        if remain <= d_brake + 1e-9:
            current_speed = max(0.0, current_speed - acceleration * dt)
        else:
            if current_speed < max_velocity:
                current_speed = min(max_velocity , current_speed + acceleration*dt)
            else:
                current_speed = max_velocity

        last_time = current_time
        last_error = error

        wait(10)
        print(current_speed )

        drive_base.drive(current_speed * direction, correction)

    drive_base.stop()
