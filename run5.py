from moving_profile import moving_profile
from turn import turn
from new import * 

moving_profile(280,1000,950,0)
turn(-33)
moving_profile(570,1000,950,-33)
left_arm.run_angle(1000, -700)

moving_profile(45, -1000, 950, -30)
turn(-85)
moving_profile(750,1000,950,-85)
turn(-150)
moving_profile(90,1000,950,-150)
right_arm.run_angle(1000, -700)
moving_profile(50, 1000, 950, -150)
moving_profile(140, -1000, 950, -150)
 
