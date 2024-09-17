#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:37:06 2024

@author: nando
"""

import serial
import mouse

X = 0
Y = 1
Z = 2

ser = serial.Serial('/dev/ttyUSB0', 115200)
while True:
    line = ser.readline()
    x = float(line.decode("utf-8").split(' ')[X])
    y = float(line.decode("utf-8").split(' ')[Y])
    z = float(line.decode("utf-8").split(' ')[Z])
    print(x,y,z)
    if z >= 2:
        mouse.move(-3, 0, absolute=False, duration=0)
    if z <= -1:
        mouse.move(3, 0, absolute=False, duration=0)
    if y >= 5:
       mouse.move(0, 3, absolute=False, duration=0)
    if y <= 2:
        mouse.move(0, -3, absolute=False, duration=0)