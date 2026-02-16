from pybricks.tools import wait, StopWatch
from umath import pi, fabs
# הנחה שהקבוע WHEEL_DIAMETER וייבוא המנועים נמצאים ב-new
from new import * # --- הגדרות קבועות ---
# אם הרובוט רועד, תוריד את המספר הזה ל-15 או 12
KP_DEFAULT = 12.0   
# אם יש רעש של "דבורה", תוריד את זה ל-0
KD_DEFAULT = 0.5    

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
    
    # --- 2. חישוב הפרופיל (המתמטיקה שמונעת את הבאמפר) ---
    # המרחק שלוקח להאיץ למהירות המקסימלית
    accel_dist = (v_max * v_max) / (2 * accel)
    
    # אם המרחק הכולל קצר מדי (אין מקום להגיע למהירות מקסימלית) -> פרופיל משולש
    if (accel_dist * 2) > total_dist:
        accel_dist = total_dist / 2
        decel_dist = total_dist / 2
        cruise_dist = 0
        # חישוב המהירות החדשה שנגיע אליה (תהיה נמוכה מהמקסימום)
        # v = sqrt(2 * a * d)
        v_max = (2 * accel * accel_dist) ** 0.5
    else:
        # פרופיל טרפז מלא
        decel_dist = accel_dist
        cruise_dist = total_dist - (accel_dist + decel_dist)

    # נקודות ציון למעבר בין שלבים
    point_end_accel = accel_dist
    point_start_decel = accel_dist + cruise_dist
    
    # משתנים ללולאה
    timer = StopWatch()
    last_time = timer.time() / 1000.0
    last_error = 0
    current_speed = 0.0
    MIN_SPEED = 25  # מהירות מינימלית כדי לא להיתקע בסוף
    
    while True:
        # חישוב זמנים (בשניות)
        now = timer.time() / 1000.0
        dt = now - last_time
        if dt <= 0: dt = 0.001
        
        # איפה אנחנו נמצאים?
        current_dist_covered = abs(calculate_distance())
        remain = total_dist - current_dist_covered
        
        # --- 3. מכונת מצבים (State Machine) ---
        if current_dist_covered < point_end_accel:
            # שלב האצה
            current_speed += (accel * dt)
            if current_speed > v_max: current_speed = v_max
            
        elif current_dist_covered < point_start_decel:
            # שלב שיוט (מהירות קבועה)
            current_speed = v_max
            
        else:
            # שלב האטה
            # כאן אנחנו מורידים מהירות בצורה לינארית
            current_speed -= (accel * dt)
            # מוודאים שלא יורדים מתחת למינימום עד שממש מגיעים
            if current_speed < MIN_SPEED:
                current_speed = MIN_SPEED

        # --- 4. בקרת כיוון (PID) ---
        current_heading = hub.imu.heading()
        error = target_heading - current_heading
        
        derivative = (error - last_error) / dt
        
        # Gain Scheduling: החלשת התיקון במהירויות נמוכות למניעת רעידות
        scale_factor = 1.0
        if current_speed < (v_max * 0.4): # אם אנחנו ב-40% מהירות ומטה
            scale_factor = 0.5  # חותכים את עוצמת התיקון בחצי
            
        turn_rate = (error * kp + derivative * kd) * scale_factor

        # --- 5. הפעלה ותנאי יציאה ---
        drive_base.drive(current_speed * direction, turn_rate)
        
        last_time = now
        last_error = error
        
        # יציאה מהלולאה כשהגענו למרחק
        if remain <= 5: # 5 מ"מ טולרנס
            break
            
        wait(10)

    drive_base.stop()
