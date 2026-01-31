from pybricks.tools import wait, StopWatch
from new import *
from umath import pi


def turn(
    target_deg,
    absolute=True,
    kp=13.0,
    ki=0,
    kd=0.35,
    tolerance_deg= 1,        # כמה מעלות "מספיק קרוב"
    settle_time_ms=50,       # כמה זמן צריך להיות קרוב כדי לסיים
    timeout_ms=4000,         # גיבוי: לא להיתקע לנצח
    loop_ms=10,              # תדר בקרה קבוע
    max_speed=10000,         # הגבלת מהירות
    integral_zone_deg=40,    # I עובד רק כשקרובים יחסית
    integral_limit=10000,    # anti-windup: הגבלת האינטגרל
    slowdown_zone_deg=25,    # רמפה: האטה כשמתקרבים ליעד
):
    """
    סיבוב במקום לפי IMU עם PID, כולל:
    - יציאה כשקרובים לאורך settle_time_ms + timeout
    - עצירה בסוף
    - dt בשניות + הגנה על dt
    - wait קבוע
    - Integral נכון + anti-windup (zone+clamp)
    - רמפה להאטה ליד היעד
    """
    if abs(target_deg) <= 15:
        kp = 13.0
        ki = 0
        kd = 0.35
    elif abs(target_deg) <= 30:
        kp = 13.0
        ki = 0
        kd = 0.35
    elif abs(target_deg) <= 45:
        kp = 12.0
        ki = 0
        kd = 0.35
    elif abs(target_deg) <= 90:
        kp = 13.6
        kd = 0.6 
        ki = 0.1
    else:
        kp = 10
        kd = 0.35
        ki = 0

    # סיבוב יחסי: מאפסים heading ל-0
    if not absolute:
        hub.imu.reset_heading(0)

    sw = StopWatch()
    start_ms = sw.time()
    last_ms = sw.time()

    # מצב PID
    integral = 0.0
    on_target_ms = 0

    # שגיאה התחלתית
    last_error = target_deg - hub.imu.heading()

    while True:
        now_ms = sw.time()
        elapsed_ms = now_ms - start_ms

        # timeout: גיבוי
        if elapsed_ms >= timeout_ms:
            break

        # dt בשניות + הגנה על dt
        dt_ms = now_ms - last_ms
        if dt_ms <= 0:
            dt_ms = loop_ms
        dt = dt_ms / 1000.0  # שניות

        # שגיאה
        error = target_deg - hub.imu.heading()

        # יציאה: להיות בתוך טולרנס לאורך זמן
        if abs(error) <= tolerance_deg:
            on_target_ms += dt_ms
            if on_target_ms >= settle_time_ms:
                break
        else:
            on_target_ms = 0

        # PID
        p = kp * error

        # Integral נכון + anti-windup (zone + clamp)
        if abs(error) <= integral_zone_deg:
            integral += error * dt
            if integral > integral_limit:
                integral = integral_limit
            elif integral < -integral_limit:
                integral = -integral_limit

        i = ki * integral
        d = kd * ((error - last_error) / dt)

        speed = p + i + d

        # רמפה: להאט כשקרובים ליעד
        # if abs(error) < slowdown_zone_deg:
        #     speed *= abs(error) / max(slowdown_zone_deg, 1e-6)

        # הגבלת מהירות
        if speed > max_speed:
            speed = max_speed
        elif speed < -max_speed:
            speed = -max_speed

        # הפעלה (כמו אצלך: ימין הפוך משמאל)
        right_wheel_motors.run(-speed)
        left_wheel_motors.run(speed)

        last_error = error
        last_ms = now_ms

        # תדר בקרה קבוע
        wait(loop_ms)

    # עצירה בסוף (גם אחרי timeout)
    try:
        left_wheel_motors.brake()
        right_wheel_motors.brake()
    except:
        try:
            left_wheel_motors.stop()
            right_wheel_motors.stop()
        except:
            left_wheel_motors.run(0)
            right_wheel_motors.run(0)
