from pybricks.tools import wait, StopWatch
from umath import pi, fabs
# הנחה שהקבוע WHEEL_DIAMETER וייבוא המנועים נמצאים ב-new
from new import * # --- הגדרות קבועות ---

# עודכן ל-18.0 כדי להגיב מהר יותר לסטיות
KP_DEFAULT = 18.0   
# עודכן ל-1.2 כדי לרסן את התיקון ולמנוע רעידות
KD_DEFAULT = 1.2    

def calculate_distance():
    """ חישוב מרחק לפי ממוצע המנועים """
    left = left_wheel_motors.angle()
    right = right_wheel_motors.angle()
    avg_angle = (left + right) / 2
    return (avg_angle / 360) * (WHEEL_DIAMETER * pi)

def moving_profile(target_distance, max_velocity, acceleration, target_heading, absolute=True, kp=KP_DEFAULT, kd=KD_DEFAULT):
    """
    פרופיל תנועה טרפזי (האצה -> שיוט -> האטה) מחושב מראש.
    מונע קפיצות וגמגומים.
    """
    
    # print(f"\n--- START MOVE: dist={target_distance}, v={max_velocity} ---")
    
    # 1. איפוסים והכנות
    drive_base.stop()
    left_wheel_motors.reset_angle(0)
    right_wheel_motors.reset_angle(0)
    
    if not absolute:
        hub.imu.reset_heading(0)

    # כיוון וערכים מוחלטים
    direction = 1 if target_distance >= 0 else -1
    total_dist = abs(target_distance)
    v_max = abs(max_velocity)
    accel = abs(acceleration)
    
    # --- 2. חישוב הפרופיל ---
    accel_dist = (v_max * v_max) / (2 * accel)
    
    if (accel_dist * 2) > total_dist:
        accel_dist = total_dist / 2
        decel_dist = total_dist / 2
        cruise_dist = 0
        v_max = (2 * accel * accel_dist) ** 0.5
    else:
        decel_dist = accel_dist
        cruise_dist = total_dist - (accel_dist + decel_dist)

    point_end_accel = accel_dist
    point_start_decel = accel_dist + cruise_dist
    
    timer = StopWatch()
    last_time = timer.time() / 1000.0
    last_error = 0
    current_speed = 0.0
    MIN_SPEED = 25
    
    while True:
        now = timer.time() / 1000.0
        dt = now - last_time
        if dt <= 0: dt = 0.001
        
        current_dist_covered = abs(calculate_distance())
        remain = total_dist - current_dist_covered
        
        # --- 3. מכונת מצבים ---
        if current_dist_covered < point_end_accel:
            current_speed += (accel * dt)
            if current_speed > v_max: current_speed = v_max
        elif current_dist_covered < point_start_decel:
            current_speed = v_max
        else:
            current_speed -= (accel * dt)
            if current_speed < MIN_SPEED: current_speed = MIN_SPEED

        # --- 4. בקרת כיוון (PID) ---
        current_heading = hub.imu.heading()
        error = target_heading - current_heading
        
        derivative = (error - last_error) / dt
        
        scale_factor = 1.0
        if current_speed < (v_max * 0.4): 
            scale_factor = 0.8  
            
        turn_rate = (error * kp + derivative * kd) * scale_factor

        # --- 5. הפעלה ---
        drive_base.drive(current_speed * direction, turn_rate)
        
        # הדפסות מושהות לביצועים
        # print(f"{now:.3f},{current_dist_covered:.2f},{current_speed:.2f},{error:.2f},{turn_rate:.2f}")
        
        last_time = now
        last_error = error
        
        if remain <= 5: 
            break
            
        wait(10)

    drive_base.stop()
    # print("--- END MOVE ---")
