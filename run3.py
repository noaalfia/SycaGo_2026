from new import *
from turn import turn
from moving_profile import moving_profile

moving_profile(552, 500, 300, 0, False)
right_arm.run_angle(700, 1100)
moving_profile(115, -525, 300, 0)
moving_profile(75, 500, 500, 0)

right_arm.run_angle(700 , -600)
moving_profile(80, -500, 500, 0)
turn(-45, False)
moving_profile(165, 500, 500, -45)
turn(15)
moving_profile(50, 500, 500, 15)
turn(20)
moving_profile(100, -600 ,600, 20)
right_arm.run_angle(700, 500)
right_arm.run_angle(700, -500)
turn(-25)
