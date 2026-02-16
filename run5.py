from new import *
from turn import turn
from moving_profile import moving_profile

moving_profile(215,1000,950,0)
turn(-35) 
moving_profile(588, 500, 450, -35)
turn(-95)
moving_profile(700, 1000, 950, -95, kp=7.5) 
turn(-140)
left_arm.run_angle(1000, 700, Stop.BRAKE, False)
moving_profile(190, 850, 850, -140)


