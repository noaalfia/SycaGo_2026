from moving_profile import moving_profile
from turn import turn
from new import * 
moving_profile(200 , 600 , 500 , 0 , False)
turn(-28 , False)
moving_profile(550 , 600 , 500 , -28 )
turn(-50)
moving_profile(100 , 600 , 500 , -50 )
left_arm.run_angle(700 , -700)
moving_profile(50 , 600 , 500 , -50 )

