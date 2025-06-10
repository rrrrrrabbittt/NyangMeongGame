# 통합된 전체 주행 코드 제공
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile
from pybricks.iodevices import I2CDevice, UARTDevice
from mindsensorsPYB import LSA

# 장치 설정
ev3 = EV3Brick()
run_motor = Motor(Port.A)
steering_motor = Motor(Port.D)
lsa = LSA(Port.S1, 0x14)
cs = ColorSensor(Port.S4)
ser = UARTDevice(Port.S2, baudrate=115200)
ultra = UltrasonicSensor(Port.S3)

# 초기 설정
distance_threshold = 4
time_threshold = 2500
column_timer = StopWatch()
red_count = 0
red_timer = StopWatch()
green_count = 0
crosswalk_timer = StopWatch()
start_timer1 = StopWatch()
start_timer2 = StopWatch()
after_parking_timer = StopWatch()

def start():
    steering_motor.run(100)
    while True:
        a = steering_motor.angle()
        wait(100)
        b = steering_motor.angle()
        if a == b:
            break
    steering_motor.stop()
    steering_motor.run_angle(-100, 105)
    steering_motor.reset_angle(0)

def forward(speed=210, gain=4):
    try:
        run_motor.run(speed)
        data = lsa.ReadRaw_Calibrated()
        sensor_value = list(data)
        line_value1 = sum(sensor_value[:3])/len(sensor_value[:3])
        line_value2 = sum(sensor_value[4:])/len(sensor_value[3:])
        error = line_value1 - line_value2
        corr = gain * error
        if error > 5:
            corr += 5
        elif error < -5:
            corr -= 5
        corr = max(min(corr, 90), -90)
        steering_motor.run_target(1500, corr)
    except:
        pass

def detect_column():
    distance = ultra.distance() / 10
    return distance <= distance_threshold

def detect_yellow():
    try:
        r, g, b = cs.rgb()
        print("RGB: {} {} {}".format(r, g, b))
        if r >= 10 and g >= 10 and b <= 10:
            print("YELLOW DETECTED ✅")
            return True
        else:
            print("Not yellow ❌")
            return False
    except:
        print("Sensor error")
        return False

def detect_red():
    try:
        r, g, b = cs.rgb()
        print("RGB: {} {} {}".format(r, g, b))
        if r >= 10 and g <= 5 and b <= 6:
            print("RED DETECTED ✅")
            return True
        else:
            print("Not red ❌")
            return False
    except:
        print("Sensor error")
        return False

def read_openmv_data():
    try:
        camera_data = ser.read_all()
        return camera_data.decode().strip()
    except:
        pass

def parking():
    run_motor.run_time(-500, 700)
    steering_motor.run_angle(500, -80)
    run_motor.run_time(500, 800)
    steering_motor.run_angle(500, 140)
    ev3.speaker.beep()
    run_motor.run_time(-500, 1100)
    steering_motor.run_angle(500, -130)
    ev3.speaker.beep()
    run_motor.run_time(-500, 1200)
    steering_motor.run_angle(500, 140)
    run_motor.run_time(390, 590)
    ev3.light.on(Color.RED)
    wait(1000)
    ev3.light.on(Color.YELLOW)
    wait(1000)
    ev3.light.on(Color.GREEN)
    wait(1000)
    run_motor.run_time(-500, 650)
    steering_motor.run_angle(500, -140)
    run_motor.run_time(500, 930)
    steering_motor.run_angle(500, 120)
    run_motor.run_time(500, 2200)

# 주행 시작
start()
run_motor.run_time(200, 2000)
steering_motor.run_target(1500, 90)
run_motor.run_time(100, 1500)

start_timer1.reset()
while True:
    forward(speed=200)
    if start_timer1.time() >= 2000:
        run_motor.stop()
        break

start_timer2.reset()
while True:
    forward(speed=350)
    if start_timer2.time() >= 17000:
        run_motor.stop()
        break

while True:
    forward(speed=200)
    if detect_yellow():
        run_motor.stop()
        wait(100)
        break

ev3.light.on(Color.RED)
wait(1000)
ev3.light.on(Color.ORANGE)
wait(1000)
ev3.light.on(Color.GREEN)
wait(1000)

while True:
    forward(speed=200)
    if detect_column():
        run_motor.stop()
        wait(100)
        break

ev3.speaker.beep()
column_timer.reset()
while not detect_column():
    forward(speed=200)

run_motor.stop()
detected_time = column_timer.time()
print(detected_time)

if detected_time >= time_threshold:
    print("parking start")
    ev3.speaker.beep()
    parking()
else:
    print("No space for parking")
    ev3.speaker.beep()
    ev3.speaker.beep()
    column_timer.reset()
    while True:
        forward(speed=200)
        if detect_column() and column_timer.time() > 2000:
            print(column_timer.time())
            run_motor.stop()
            print("final parking")
            ev3.speaker.beep()
            parking()
            break

wait(100)
after_parking_timer.reset()
while True:
    forward(speed=200)
    if after_parking_timer.time() >= 2000:
        run_motor.stop()
        break

# 빨간선 2회 감지되면 정지
red_timer.reset()
while True:
    forward(speed=270)
    if red_timer.time() > 5000 and detect_red():
        red_count += 1
        ev3.speaker.beep()
        print(f"Red line #{red_count} detected")
        red_timer.reset()
        if red_count == 2:
            print("stop line detected")
            run_motor.stop()
            break

wait(1000)
while True:
    label = read_openmv_data()
    if label == 'green':
        ev3.light.on(Color.GREEN)
        green_count += 1
        if green_count == 10:
            run_motor.run(200)
            break
    elif label == 'red':
        ev3.light.on(Color.RED)
        green_count = 0
        run_motor.stop()

crosswalk_timer.reset()
while True:
    forward(speed=200)
    if crosswalk_timer.time() >= 9000:
        run_motor.stop()
        break

# 횡단보도 주행
for angle in [-60, -35, -65, -30, -65, -35, -65, -40, -60, -35, -65, -40, -65, -40, -65]:
    steering_motor.run_target(1500, angle)
    run_motor.run_time(200, 1000)

steering_motor.run_target(1500, 60)
run_motor.run_time(100, 2000)

while True:
    forward(speed=200)
    if detect_red():
        run_motor.stop()
        break

for i in range(500, 2100, 100):
    ev3.speaker.beep(i, 100)
    wait(10)

ev3.speaker.say('Good')

