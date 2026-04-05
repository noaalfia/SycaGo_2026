from pybricks.tools import wait, StopWatch
from umath import pi
from new import * 
def smart_profiled_turn(
    target_angle, 
    max_turn_rate=700, 
    turn_acceleration=480,
    kp=4.0,                  
    kd=0.3,                  
    ks=15,                   
    tolerance_deg=0.5,       
    settle_time_ms=50,       
    absolute=True
):
    
    # 1. שחרור מנועים (מניעת התנגשות עם DriveBase)
    left_wheel_motors.stop()
    right_wheel_motors.stop()
    
    if not absolute:
        hub.imu.reset_heading(0)
        
    # שמירת זווית התחלתית לחישוב התקדמות ולמניעת באג אבסולוטי
    start_heading = hub.imu.heading() 
    
    direction = 1 if target_angle >= start_heading else -1
    
    # חישוב המרחק הזוויתי הכולל שצריך לעבור (בדלתא)
    total_angle = abs(target_angle - start_heading) 
    
    ratio = AXLE_TRACK / WHEEL_DIAMETER
    
    # מנגנון הגנה: הגבלת המהירות כדי שלא לעבור את היכולת הפיזית של המנוע (Saturation)
    max_safe_turn_rate = 850 / ratio 
    v_max = min(abs(max_turn_rate), max_safe_turn_rate)
    
    accel = abs(turn_acceleration)
    
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
        
        # חישוב ההתקדמות היחסית מתחילת הפנייה
        current_angle_covered = abs(hub.imu.heading() - start_heading)
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
        
        last_time = now
        wait(10)
        
    # ==========================================
    # שלב ב': התייצבות PID
    # ==========================================
    last_error = target_angle - hub.imu.heading()
    on_target_ms = 0
    last_ms = sw.time()
    pid_start_time = sw.time() # הגנת תקיעה (Timeout)
    
    # מעקב Overshoot לטובת ציון ה-Twiddle
    peak_angle = abs(hub.imu.heading() - start_heading)

    while True:
        now_ms = sw.time()
        dt_ms = now_ms - last_ms
        if dt_ms <= 0: dt_ms = 10
        dt = dt_ms / 1000.0
        
        current_heading = hub.imu.heading()
        error = target_angle - current_heading
        
        # עדכון שיא הפנייה אם עברנו אותו (חריגה)
        current_abs_angle = abs(current_heading - start_heading)
        if current_abs_angle > peak_angle:
            peak_angle = current_abs_angle
        
        if abs(error) <= tolerance_deg:
            on_target_ms += dt_ms
            if on_target_ms >= settle_time_ms:
                break
        else:
            on_target_ms = 0
            
        # הגנת Timeout - אם ה-PID לא מצליח להתייצב אחרי 5 שניות, חותכים כדי לא להיתקע
        if (now_ms - pid_start_time) > 5000:
            print("PID TIMEOUT REACHED!")
            break
            
        p = kp * error
        d = kd * (error - last_error) / dt
        
        desired_direction = 1 if error >= 0 else -1
        ff_left = ks * desired_direction
        ff_right = ks * -desired_direction
        
        speed_left = (p + d) * ratio + ff_left
        speed_right = -((p + d) * ratio + ff_right)
        
        left_wheel_motors.run(speed_left)
        right_wheel_motors.run(speed_right)
        
        last_error = error
        last_ms = now_ms
        wait(10)
        
    # החלפה ל-brake למניעת רעידת סיום שקיימת לעתים ב-hold
    left_wheel_motors.brake()
    right_wheel_motors.brake()
    
    # החזרת ה-Peak עבור ה-Auto-Tuner (Twiddle) שיוכל לחשב Overshoot
    return peak_angle
