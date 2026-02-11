from new import *
from turn import turn
from moving_profile import moving_profile

moving_profile(260,1000,950,0)
turn(-35) 
moving_profile(525, 500, 450, -35)

turn(-82)
moving_profile(690, 1000, 950, -90, kp=7.5) 
turn(-155)
left_arm.run_angle(1000, 700, Stop.BRAKE, False)
moving_profile(40, 700, 650, -155)
moving_profile(100, 900, 850, -170)
