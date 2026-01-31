from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

right_wheel_motors = Motor(Port.A)
left_wheel_motors = Motor(Port.B, Direction.COUNTERCLOCKWISE)
left_arm = Motor(Port.D, Direction.COUNTERCLOCKWISE)
right_arm = Motor(Port.F)
right_colorsensor = ColorSensor(Port.C)
left_colorsensor = ColorSensor(Port.E)
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 130
drive_base = DriveBase(left_wheel_motors, right_wheel_motors, WHEEL_DIAMETER, AXLE_TRACK)
