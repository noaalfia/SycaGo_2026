from pybricks.tools import wait, StopWatch
from new import * # בהנחה ש-WHEEL_DIAMETER ו-AXLE_TRACK כאן
from umath import pi

def smart_profiled_turn(
    target_angle, 
    max_turn_rate=700, 
    turn_acceleration=480,
    kp=5.0,                  
    kd=0.4,                  
    ks=20,                   
    tolerance_deg=0.3,       
    settle_time_ms=50,       
    absolute=True
):
    
    # print(f"\n--- START TURN: angle={target_angle}, v={max_turn_rate} ---")

    drive_base.stop()
    if not absolute:
        hub.imu.reset_heading(0)
    
    direction = 1 if target_angle >= 0 else -1
    total_angle = abs(target_angle)
    v_max = abs(max_turn_rate)
    accel = abs(turn_acceleration)
    
    ratio = AXLE_TRACK / WHEEL_DIAMETER
    
    accel_angle = (v_max * v_max) / (2 * accel)
    if (accel_angle * 2) > total_angle:
        accel_angle = total_angle / 2
        decel_angle = total_angle / 2
        cruise_angle = 0
        v_max = (2 * accel * accel_angle) ** 0.5
    else:
        decel_angle = accel_angle
        cruise_angle = total_angle - (accel_angle + decel_angle)

    point_end_accel = accel_angle
    point_start_decel = accel_angle + cruise_angle
    
    sw = StopWatch()
    last_time = sw.time() / 1000.0
    current_speed = 0.0
    MIN_SPEED = 15
    
    # ==========================================
    # שלב א': פרופיל תנועה
    # ==========================================
    while True:
        now = sw.time() / 1000.0
        dt = now - last_time
        if dt <= 0: dt = 0.001
        
        current_angle_covered = abs(hub.imu.heading())
        remain = total_angle - current_angle_covered
        
        if remain <= 2.0:
            break
            
        if current_angle_covered < point_end_accel:
            current_speed += (accel * dt)
            if current_speed > v_max: current_speed = v_max
        elif current_angle_covered < point_start_decel:
            current_speed = v_max
        else:
            current_speed -= (accel * dt)
            if current_speed < MIN_SPEED: current_speed = MIN_SPEED
            
        wheel_speed = current_speed * ratio
        left_wheel_motors.run(wheel_speed * direction)
        right_wheel_motors.run(-wheel_speed * direction)
        
        # current_heading = hub.imu.heading()
        # error = target_angle - current_heading
        # print(f"{now:.3f},1,{current_heading:.2f},{error:.2f},{wheel_speed * direction:.2f}")
        
        last_time = now
        wait(10)
        
    # ==========================================
    # שלב ב': התייצבות PID
    # ==========================================
    last_error = target_angle - hub.imu.heading()
    on_target_ms = 0
    last_ms = sw.time()
    
    while True:
        now_ms = sw.time()
        dt_ms = now_ms - last_ms
        if dt_ms <= 0: dt_ms = 10
        dt = dt_ms / 1000.0
        
        current_heading = hub.imu.heading()
        error = target_angle - current_heading
        
        if abs(error) <= tolerance_deg:
            on_target_ms += dt_ms
            if on_target_ms >= settle_time_ms:
                break
        else:
            on_target_ms = 0
            
        p = kp * error
        d = kd * (error - last_error) / dt
        
        desired_direction = 1 if error >= 0 else -1
        ff_left = ks * desired_direction
        ff_right = ks * -desired_direction
        
        speed_left = (p + d) * ratio + ff_left
        speed_right = -((p + d) * ratio + ff_right)
        
        left_wheel_motors.run(speed_left)
        right_wheel_motors.run(speed_right)
        
        # now_sec = now_ms / 1000.0
        # print(f"{now_sec:.3f},2,{current_heading:.2f},{error:.2f},{speed_left:.2f}")
        
        last_error = error
        last_ms = now_ms
        wait(10)
        
    left_wheel_motors.hold()
    right_wheel_motors.hold()
    
    # now_sec = sw.time() / 1000.0
    # final_heading = hub.imu.heading()
    # print(f"{now_sec:.3f},3,{final_heading:.2f},{target_angle - final_heading:.2f},0.00")
    # print("--- END TURN ---")
