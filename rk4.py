# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 18:41:08 2016

@author: Boris
"""

import numpy as np
import math
import os

class body:
    position = np.zeros([3,1])
    velocity = np.zeros([3,1])
    acc = np.zeros([3,1])
    mass = 0
    
    positionStep = np.zeros([4,3])
    velocityStep = np.zeros([4,3])
    accStep = np.zeros([4,3])
    
    #Initialization: 
    #inital acceleration is zero!
    def __init__(self, p, v, m):
        self.position = p
        self.velocity = v
        self.mass = m
      
def radius(body1, body2):
    r = math.sqrt(np.sum(np.square(body1.position - body2.position)))
    return(r)
    
G = 6.67e-11                #Gravitational constant
secInYr = 365.24*24*3600    #Seconds in a year
dt = 86400.0                  #Time step (in seconds)
maxTime = secInYr * 10      #Simulation time (in seconds)
AU = 149597871000.0           #Astronomical unit (in meters)       
       
#Setting up Sun - Earth system for testing
#TODO: Set up initialization from file
bodies = []
bodies.append(body(np.array([AU, 0, 0]), np.array([0, 2*math.pi*AU/(secInYr), 0]), 6e24))
bodies.append(body(np.array([0, 0, 0]), np.array([0, 0, 0]), 2e30))
N = len(bodies)

currTime = 0
while currTime < maxTime:
    #Calculating acceleration (second derivative ov position)
    for i in range(N):
        Force = np.zeros([1,3])
        for j in range(N):
            if(i != j):
                Force += -G * bodies[i].mass * bodies[j].mass * (bodies[i].position - bodies[j].position) / (radius(bodies[i], bodies[j]) ** 3)
        bodies[i].acc = Force / bodies[i].mass
        
    
    currTime += dt
    
    
    
    
    
    
