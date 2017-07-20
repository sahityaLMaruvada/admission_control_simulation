"""
module that gets the user location and gives the maximum distance from the base station
"""

from time import time, sleep
import math
import numpy as np
distance_from_bs=[]
radius = 10
people = 1000
#people=10000 #Uncomment this for 10000
random_theta = np.random.uniform(0.0, 1.0, size=people)*2*np.pi
random_radius = radius * np.sqrt(np.random.uniform(0.0, 1.0, size=people)) 
x = random_radius * np.cos(random_theta)
y = random_radius * np.sin(random_theta) 
uniform_distance_points=[(x[i],y[i]) for i in range(people)]
def getUserlocation():
	global people
	select_location=np.random.randint(0,people)
	x_uniform=uniform_distance_points[select_location][0]
	y_uniform=uniform_distance_points[select_location][1]
	user_location = math.sqrt(x_uniform**2+y_uniform**2)
	return (user_location,random_theta[select_location]) #returning the polar coordinates of the corresponding point


def get_maximum_radius(active_user_list):
	if active_user_list !=[]:
		distance_from_bs=[i.location for i in active_user_list]
	else:
		distance_from_bs=[0]
	return max(distance_from_bs)

