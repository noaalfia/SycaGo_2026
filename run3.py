
from new import *
from turn import turn
from moving_profile import moving_profile

moving_profile(140,700,600,0, False)
turn(-43)
moving_profile(340, 700,600,-43)
right_arm.run_angle(1000, 700)
turn(-58)
turn(-43)

moving_profile(47, -695, 650, -43)
turn(0)
right_arm.run_angle(1000, -683, Stop.BRAKE, False)
moving_profile(337, 1000, 1000, 0)
right_arm.run_angle(1000, 800)

moving_profile(37, -650, 550, 0)
turn(48)
right_arm.run_angle(1000, -900, Stop.BRAKE, False)
moving_profile(75, 300, 350, 48)
right_arm.run_angle(600, 800)

right_arm.run_angle(1000, -683, Stop.BRAKE, False)
moving_profile(35, -400, 350, 48)
left_arm.run_angle(300, -360)
moving_profile(62, 400,350, 40)
turn(82, kp=22)

left_arm.run_angle(1000, 1000)
turn(50)
moving_profile(88, -600, 550, 50)
turn(-90)
moving_profile(255, -900, 850, -90)

moving_profile(200, 900, 850, -90)
turn(0)
moving_profile(350, -900, 850, 0)
turn(31)
left_arm.run_angle(1000, -900)
left_arm.run_angle(600, 900)
left_arm.run_angle(1000, -900)
left_arm.run_angle(600, 900)
left_arm.run_angle(1000, -900)
left_arm.run_angle(600, 900)
left_arm.run_angle(1000, -900)

left_arm.run_angle(800, 800, Stop.BRAKE, False)
turn(-20)
moving_profile(270, -1000, 950, -20)
