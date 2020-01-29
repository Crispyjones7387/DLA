# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 19:04:53 2020

@author: Caleb Jones
"""

import time
import numpy as np
import random
import matplotlib.pyplot as plt 
#import decimal
#from numba import jit, cuda, prange
#from numba import roc

starttime = time.time()
arr = [h,w] = [500,500] #track of height and width of canvas
particles = 50000
sticking_coeff = 1
canvas = np.zeros((h, w)).astype(int) #the blank n * n matrix
canvas[h//2,w//2] = 1 #make center element is 1; place seed 
#// to get the floor value

stick = [] #list that keeps track of neighbors of the seed
stick.append([h//2 + 1, w//2])#below seed 
stick.append([h//2 - 1, w//2])#above seed
stick.append([h//2, w//2 + 1])#right of seed 
stick.append([h//2, w//2 - 1])#left of seed 

#@jit(nopython=True, parallel=True)
#@roc.jit(device=True)
#@numba.jit()
#@jit(cache=True)
def add_one_step(steps: list):
    random_step = [(1,0), (0,1), (-1,0), (0,-1)]
    if steps == []:
        return random_step
    result = []
    for i, steps_entry in enumerate(steps):
        for step in random_step:
            a = steps_entry[0]+step[0]
            b = steps_entry[1]+step[1]
            result.append((a, b))
    return result


def get_multiple_steps(n=5):
    final_directions = []
    while n > 0:
        final_directions = add_one_step(final_directions)
        n -= 1
    return final_directions


#  steps to precalculate! The list lengths go with 4**n
precalculated_steps = []
for i in range(12):
    precalculated_steps.append(get_multiple_steps(i))
    #brute force approach where all steps are calculated and stored since each
    #step or direction has the same probablity
    
    
    
def walk(A, B, canvas):# A: row B: Column
    while True:
        
        n = 10
        direction = precalculated_steps[n][np.random.randint(4**n)]
        A += direction[0]
        B += direction[1]
        
        #take care of overflow & underflow
        if A < 0: A = 0 
        elif B < 0: B = 0
        if A >= h: A -= 1
        elif B >= w: B -= 1
        
        positi = [A , B]    
        if positi in stick:
            stick.pop(0)
            if np.random.rand() < sticking_coeff: #stick only if it is less than sticking coeff
                for site in [[positi[0] + 1, positi[1]],
                            [positi[0] - 1, positi[1]],
                            [positi[0], positi[1] + 1],
                            [positi[0], positi[1] - 1]]:
                    if site not in stick:
                        stick.append(site) #new neighbor of seeds gets added to the list
                canvas[positi[0] , positi[1]] = 1   
                break  
            else:
                continue
    
    return canvas

for i in range(particles):
        print('particle ',i+1)
        selec = random.sample(set(['A','B','C','D']),1)
        #pos1 = randrange(0, len(arr))
        pos = np.random.randint(0, arr[0])
#        print(selec)
    
        if selec == ['A']:
            #first column
            walk(pos,0,canvas)
    
        elif selec == ['B']:
            #last column
            walk(pos,arr[1]-1,canvas)
    
        elif selec == ['C']:   
            #first row
            walk(0,pos,canvas)
    
        else:    
            #last row
            walk(arr[0]-1,pos,canvas)
            
print('That took {} seconds'.format(time.time() - starttime))

plt.matshow(canvas)
#plt.title("50k Particles & Sticking Coff:0.05", fontsize=8)
#plt.savefig("DLA_50k_0.05_2.png",dpi=2000)