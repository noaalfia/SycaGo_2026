from moving_profile import moving_profile
from turn import turn
from new import * 

moving_profile(230,1000,950,0)
turn(-35)
right_arm.run_angle(1000, -700, Stop.BRAKE, False) 
moving_profile(640, 700, 650, -40)
right_arm.run_angle(1000, 700) 

turn(-82)
moving_profile(725, 1000, 950, -90, kp=7.5)
turn(-160)
moving_profile(70,1000,950,-160)
left_arm.run_angle(1000, 700)
moving_profile(60, 1000, 950, -160)
moving_profile(60, -1000, 950, -160)
 
