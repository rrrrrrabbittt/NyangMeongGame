#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from pybricks.iodevices import I2CDevice
from mindsensorsPYB import LSA

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
lsa = LSA(Port.S1, 0x14)

# Write your program here.
ev3.speaker.beep()

# while True : 
#     data = lsa.ReadRaw_Calibrated()
#     sensor_value = list(data)
#     print(sensor_value)
#     wait(500)



run_motor = Motor(Port.A)
steering_motor = Motor(Port.D)



def start() :
    steering_motor.run(100)
    while True :
        #현재 모터 각도
        a = steering_motor.angle()
        wait(60)
        #0.1초 후 모터 각도
        b = steering_motor.angle()
        #모터 각도가 동일하면 반복문 종료
        if a == b :
            break
    # 모터 정지 후 중심까지 모터 이동
    steering_motor.stop()
    steering_motor.run_angle(-80,100)
    #현재 위치를 원점으로 초기화
    steering_motor.reset_angle(0)


start()
run_motor.run(230)

th = 40
Gain = 5

# on&off 라인 트레이싱
while True :
    try :
        data = lsa.ReadRaw_Calibrated()
        sensor_value = list(data)
        line_value = sensor_value[5]

        print(sensor_value)
        error = th - line_value
        correction = Gain * error

        if correction > 90 :
            correction = 90
        if correction < -90 :
            correction = -90


        steering_motor.run_target(1500, correction)
    except :
        pass


