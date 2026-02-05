from new import *
from turn import turn
from moving_profile import moving_profile

moving_profile(50,700,600,0, False)
turn(-50)
moving_profile(475,700,600,-50)
left_arm.run_angle(1000,-1200)
moving_profile(102,-1000, 700,-50)
left_arm.run_angle(700,1100)

turn(-45, False)
moving_profile(250, 600, 500, -45)
turn(42)
moving_profile(35, 630, 500, 42)
left_arm.run_angle(1000 , -1150)
left_arm.run_angle(1000, 1000)
moving_profile(140 ,-400, 200, 42)
left_arm.run_angle(700 , 360 , Stop.BRAKE , False)

turn(-30)
moving_profile(302, 700, 650, -30)
turn(19)
right_arm.run_angle(600, -900)
moving_profile(50, -400, 350, 19)
moving_profile(155,500,150, 19)
right_arm.run_angle(1000, 900)
moving_profile(120, -500, 400, 19)
turn(-40)
moving_profile(900, -1000, 950, -40)
