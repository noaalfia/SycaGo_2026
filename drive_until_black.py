from new import *
def drive_until_black(speed):
    hub.imu.reset_heading(0)
    drive_base.drive(speed, 0) 

    while True:
        if right_colorsensor.reflection() <= 20:
            drive_base.stop()
