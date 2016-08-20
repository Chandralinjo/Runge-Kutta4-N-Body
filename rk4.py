# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 18:41:08 2016

@author: Boris
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import os

class body:
    position = np.zeros([3,1])
    velocity = np.zeros([3,1])
    acc = np.zeros([3,1])
    mass = 0.0
    
    positionStep = np.zeros([4,3])
    velocityStep = np.zeros([4,3])
    accStep = np.zeros([4,3])
    
    #Initialization: 
    #inital acceleration is zero!
    def __init__(self, p, v, m):
        self.position = p
        self.velocity = v
        self.mass = m
      
#Distance between two body objects:
def bodyDistance(body1, body2):
    r = np.sum(np.square(body1.position - body2.position)) ** 0.5
    return(r)

#Distance between two 3-radius vectors (in form of numpy arrays):
def distance(vector1, vector2):
    r = np.sum(np.square(vector1 - vector2)) ** 0.5
    return r

G = 6.67e-11                #Gravitational constant
secInYr = 365.24*24*3600    #Seconds in a year
stepSize = 86400.0                  #Time step (in seconds)
maxTime = secInYr    #Simulation time (in seconds)
#maxTime = 80000.0
AU = 1.49597871000e11           #Astronomical unit (in meters)       

x = []
y = []
       
#Setting up Sun - Earth system for testing
#TODO: Set up initialization from file
bodies = []
bodies.append(body(np.array([AU, 0, 0], dtype = float), np.array([0, 2*math.pi*AU/(secInYr), 0], dtype = float), 6.0e24))
bodies.append(body(np.array([0, 0, 0], dtype = float), np.array([0, 0, 0], dtype = float), 2.0e30))
N = len(bodies)

currTime = 0
while currTime < maxTime:
    #Calculating step 1 accelerations (second derivative ov position)
    for i in range(N):
        bodies[i].positionStep = np.zeros([4,3])
        bodies[i].velocityStep = np.zeros([4,3])        
        bodies[i].accStep = np.zeros([4,3])        
        Force = np.zeros([1,3], dtype = float)
        for j in range(N):
            if(i != j):
                Force += -G * bodies[i].mass * bodies[j].mass * (bodies[i].position - bodies[j].position) / (bodyDistance(bodies[i], bodies[j]) ** 3)
        bodies[i].accStep[0] = Force / bodies[i].mass
        
        
    #Calculating step 1 velocities and positions:
    for i in range(N):
        bodies[i].velocityStep[0] += bodies[i].accStep[0]
        bodies[i].positionStep[0] += bodies[i].velocity
        
    
    #Calculating step 2 accelerations:
    for i in range(N):
        Force = np.zeros([1,3], dtype = float)
        for j in range(N):
            if(i != j):
                Force += -G* bodies[i].mass * bodies[j].mass * ((bodies[i].position + bodies[i].positionStep[0] * stepSize / 2) - (bodies[j].position + bodies[j].positionStep[0] * stepSize / 2)) / (distance(bodies[i].position + bodies[i].positionStep[0] * stepSize / 2, bodies[j].position + bodies[j].positionStep[0] * stepSize / 2) ** 3)
        bodies[i].accStep[1] = Force / bodies[i].mass        
        #print(i, bodies[i].accStep)
        #print('\n')
    #Calculating step 2 velocities and positions:
    for i in range(N):
        bodies[i].velocityStep[1] += bodies[i].accStep[1]
        bodies[i].positionStep[1] += bodies[i].velocity + bodies[i].velocityStep[0] * stepSize / 2
        print(bodies[i].positionStep)
   
   #Calculating step 3 accelerations:
    for i in range(N):
        Force = np.zeros([1,3], dtype = float)
        for j in range(N):
            if(i != j):
               Force += -G* bodies[i].mass * bodies[j].mass * ((bodies[i].position + bodies[i].positionStep[1] * stepSize / 2) - (bodies[j].position + bodies[j].positionStep[1] * stepSize / 2)) / (distance(bodies[i].position + bodies[i].positionStep[1] * stepSize / 2, bodies[j].position + bodies[j].positionStep[1] * stepSize / 2) ** 3)
        bodies[i].accStep[2] = Force / bodies[i].mass
    
    #Calculating step 3 velocities and positions:    
    for i in range(N):
        bodies[i].velocityStep[2] += bodies[i].accStep[2]
        bodies[i].positionStep[2] += bodies[i].velocity + bodies[i].velocityStep[1] * stepSize / 2
    #Calculating step 4 accelerations:
    for i in range(N):
        Force = np.zeros([1,3])
        for j in range(N):
            if(i != j):
                Force += -G* bodies[i].mass * bodies[j].mass * ((bodies[i].position + bodies[i].positionStep[2] * stepSize / 2) - (bodies[j].position + bodies[j].positionStep[2] * stepSize / 2)) / (distance(bodies[i].position + bodies[i].positionStep[2] * stepSize / 2, bodies[j].position + bodies[j].positionStep[2] * stepSize / 2) ** 3)
        bodies[i].accStep[3] = Force / bodies[i].mass
        #print(i, bodies[i].accStep)
    
    #Calculating step 4 velocities and positions:    
    for i in range(N):
        bodies[i].velocityStep[3] += bodies[i].accStep[3]
        bodies[i].positionStep[3] += bodies[i].velocity + bodies[i].velocityStep[1] * stepSize

    #Calculating next itteration velocities and positions   
    for i in range(N):    
        bodies[i].velocity += stepSize / 6 * (bodies[i].velocityStep[0] + 2 * bodies[i].velocityStep[1] + 2 * bodies[i].velocityStep[2] + bodies[i].velocityStep[3])
        bodies[i].position += stepSize / 6 * (bodies[i].positionStep[0] + 2 * bodies[i].positionStep[1] + 2 * bodies[i].positionStep[2] + bodies[i].positionStep[3])
    
    x.append(bodies[0].position[0])
    y.append(bodies[0].position[1])
    
    currTime += stepSize

plt.scatter(x,y)
plt.show()
    
    
    
    
    
