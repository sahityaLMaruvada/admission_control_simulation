"""
module that calculates number of users trying to make calls every second and assigns locations and appends them to the attempting_users_list
"""

import userlocation as user_loc
from collections import Counter
import numpy as np
from user import user
people=1000
#people=10000 #uncomment this for 10000
total_attempting_user_count =0

#to get the probabillity of attempting a call in seconds, returns the probability of attempting a call per second
def get_call_probability():
	probability_hr=6
	call_probability=probability_hr/3600
	return call_probability

#calculates the count of users trying to attempt a call, returns the count of users trying to attempt a call per that second
def attempting_users(current_attempting_and_active_users):
	global people
	call_probability = get_call_probability()
	#1 symbolizes the users attempting a call and 0 for users who don't
	attempting_users=np.random.choice([1,0], size=people-current_attempting_and_active_users ,p=(call_probability,1-call_probability))
	return(Counter(attempting_users)[1]) #returns the number of users trying to attempt a call in 



#function that assigns location to a user who  is trying to make a call. Returns a list which contains attempting users in the current second and the
#total count of attempting users
def assign_locations(current_attempting_and_active_users):
	#active_user_duration=get_call_duration(attempting_user_count)
	global total_attempting_user_count
	attempting_user_count=attempting_users(current_attempting_and_active_users)
	current_second_attempting_users=[]
	for i in range(attempting_user_count):
		(location,angle)=user_loc.getUserlocation()
		user_id=total_attempting_user_count
		get_attempting_user = user(user_id,location,angle)
		current_second_attempting_users.append(get_attempting_user) 
		total_attempting_user_count += 1
	return [current_second_attempting_users,total_attempting_user_count] #]

