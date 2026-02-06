
from new import *
from turn import turn
from moving_profile import moving_profile

moving_profile(260,1000,950,0)
turn(-35)
right_arm.run_angle(1000, -700, Stop.BRAKE, False) 
moving_profile(515, 500, 450, -35)

turn(-82)
moving_profile(680, 1000, 950, -90, kp=7.5) 
turn(-155)
left_arm.run_angle(1000, 700, Stop.BRAKE, False)
moving_profile(40, 700, 650, -155)
moving_profile(100, 900, 850, -170)

moving_profile(60, -500, 450, -160)
turn(-92)
moving_profile(224, 900, 850, -88)
