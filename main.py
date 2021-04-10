#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import os
import socket
os.system('setfont Lat15-TerminusBold14')
#os.system('setfont Lat15-TerminusBold32x16')

# set up TCP server
#TCP_IP = '127.0.0.1'
#TCP_PORT = 50001
#BUFFER_SIZE = 20

def gripper_calibrate():
    grip_motor.run_until_stalled(50, Stop.BRAKE, 30)
    brick.sound.file(SoundFile.UP)
    grip_motor.reset_angle(0)

def gripper_close():
    grip_motor.run_until_stalled(50, Stop.BRAKE, 50)

def gripper_open():
    grip_motor.run_target(100, -120, Stop.BRAKE)

def arm_down():
    extend_motor.run_until_stalled(50, Stop.BRAKE, 30)
    brick.sound.file(SoundFile.DOWN)

def arm_up():
    while extend_sensor.pressed() == False:
        extend_motor.run_until_stalled(-255, Stop.BRAKE, 50)
        brick.sound.file(SoundFile.UP)

def turn(target_degrees):
    turn_motor.run_target(255, target_degrees, Stop.COAST)
    #say_number(target_degrees)

def say_number(number):
    number_as_string = str(number)
    for chr in number_as_string:
        if chr is '-':
            brick.sound.file(SoundFile.NO)
        if chr is '0':
            brick.sound.file(SoundFile.ZERO)
        if chr is '1':
            brick.sound.file(SoundFile.ONE)
        if chr is '2':
            brick.sound.file(SoundFile.TWO)
        if chr is '3':
            brick.sound.file(SoundFile.THREE)
        if chr is '4':
            brick.sound.file(SoundFile.FOUR)
        if chr is '5':
            brick.sound.file(SoundFile.FIVE)
        if chr is '6':
            brick.sound.file(SoundFile.SIX)
        if chr is '7':
            brick.sound.file(SoundFile.SEVEN)
        if chr is '8':
            brick.sound.file(SoundFile.EIGHT)
        if chr is '9':
            brick.sound.file(SoundFile.NINE)
        




#conn, addr = s.accept()
#while 1:
#    data = conn.recv(BUFFER_SIZE)
#    if not data: break
#    brick.display.text(data,(60,50))


# Write your program here
#brick.display.clear()
#brick.display.text('Hello',(60,50))
#brick.display.text('World')
brick.sound.file(SoundFile.ONE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.86.23',50001))

s.send(bytes('one\n', 'utf-8'))


turn_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12,36])
extend_motor = Motor(Port.B, Direction.CLOCKWISE, [8,48])
grip_motor = Motor(Port.A, Direction.CLOCKWISE, [12,8])
turn_sensor = TouchSensor(Port.S1)
extend_sensor = TouchSensor(Port.S2)


brick.sound.beep()
brick.light(Color.GREEN)
#turn_motor.run_time(255,5000,Stop.BRAKE,True)
turn_motor.run_until_stalled(255, Stop.COAST, 50)
brick.sound.file(SoundFile.TWO)
s.send(bytes('two\n', 'utf-8'))
turn_motor.reset_angle(-90)


turn_home_found = False
while not turn_home_found:

    turn_motor.run_until_stalled(-255,Stop.COAST,50)
    if turn_sensor.pressed() == True:
        turn_home_found = True
        brick.sound.file(SoundFile.THREE)
        s.send(bytes('three\n', 'utf-8'))
        break

turn_motor.reset_angle(0)

while True:
    data = s.recv(500)
    if (data):
        #brick.sound.file(SoundFile.FOUR)
        tx_str = 'received string:[' + str(data) + ']' +'\n'
        s.send(bytes(tx_str, 'utf-8'))

        if 'turn_to_' in str(data):
            rx_str = str(data)
            number_str = chr(data[8]) + chr(data[9]) + chr(data[10])
            number = int(number_str)
            tx_str = 'decoded number is:[' + str(number) + ']' +'\n'
            s.send(bytes(tx_str, 'utf-8'))
            turn(number)
            data=None

        if 'get_turn_angle' in str(data):
            tx_string = 'turn_motor.angle()=' + str(turn_motor.angle()) + '\n'
            s.send(bytes(tx_string, 'utf-8'))
            data = None

        if 'set_turn_angle_90' in str(data):
            turn_motor.reset_angle(90)
            brick.sound.beep()
            data = None

        if 'arm_down' in str(data):
            arm_down()
            brick.sound.beep()
            data = None

        if 'arm_up' in str(data):
            arm_up()
            brick.sound.beep()
            data = None

        if 'get_extend_sensor' in str(data):
            tx_string = 'extend_sensor.pressed()=' + str(extend_sensor.pressed()) + '\n'
            s.send(bytes(tx_string, 'utf-8'))
            data = None

        if 'gripper_open' in str(data):
            gripper_open()
            brick.sound.beep()
            data = None

        if 'gripper_close' in str(data):
            gripper_close()
            brick.sound.beep()
            data = None

        if 'gripper_calibrate' in str(data):
            gripper_calibrate()
            brick.sound.beep()
            data = None

        if 'get_gripper_stalled' in str(data):
            tx_string = 'grip_motor.stalled()=' + str(grip_motor.stalled()) + '\n'
            s.send(bytes(tx_string, 'utf-8'))
            data = None

        if 'get_gripper_angle' in str(data):
            tx_string = 'grip_motor.angle()=' + str(grip_motor.angle()) + '\n'
            s.send(bytes(tx_string, 'utf-8'))
            data = None

        if 'set_gripper_angle_0' in str(data):
            grip_motor.reset_angle(0)
            brick.sound.beep()
            data = None

s.close()