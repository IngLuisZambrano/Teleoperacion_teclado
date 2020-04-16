#!/usr/bin/env python
# coding: utf-8
import rospy
from ik import *
import tkMessageBox
from Tkinter import *
from dynamixel_sdk import *
from dxl.dxlchain import DxlChain
from proyecto_delta.msg import posicion

global motores
motores = DxlChain("/dev/ttyUSB0", rate=1000000)
motors = motores.get_motor_list()
print motors

def callback_function(data):
    ri = inverse(data.x, data.y, data.z)
    motor1 = int(round(3800 - 10.8888*ri[0]))
    print motor1
    motor2 = int(round(3050 - 11.8888*ri[1]))
    motor3 = int(round(2350 - 11.4444*ri[2]))
    motores.goto(1, motor1, speed = 20, blocking = False) 
    motores.goto(2, motor2, speed = 20, blocking = False)
    motores.goto(3, motor3, speed = 20, blocking = False)
    rospy.loginfo("He recibido: Px = %f, Py = %f y Pz = %f", data.x, data.y, data.z) 
    return [motor1, motor2, motor3]

rospy.init_node('tele_local', anonymous=True) 
rospy.Subscriber("coordenadas", posicion, callback_function)


rospy.spin()

