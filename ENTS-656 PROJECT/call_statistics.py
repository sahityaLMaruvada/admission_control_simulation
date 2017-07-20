
from user import user
import time
start_t = time.time()
import numpy as np
import rsl_calculation as rsl_calc
import sinr_calculation as sinr_calc
import user_selection
import userlocation as user_loc
active_user_list=[]
total_channels=56 
attempting_user_list=[]
reattempting_low_RSL=[]
reattempting_low_SINR=[]
completed_calls_count=0
blocked_calls_signal_strength = 0
blocked_calls_channel_capacity = 0
dropped_calls = 0
minimum_RSL = -107



"""compares the SINR with minimum SINR and if the value is lower than minimum SINR,
it checks the SINR to reach the required level for three consequtive times. If failed
the call is dropped
 """
def check_SINR(active_user):
	minimum_SINR =6
	if(active_user.SINR>=minimum_SINR): 
		active_user.SINR_attempts=0 #reset the count of SINR attempts if an element in the reattempting low SINR satisfies the condition in the consequtive second
		return True
	else:
		
		active_user.SINR_attempts += 1
		if active_user not in reattempting_low_SINR: reattempting_low_SINR.append(active_user)
		if(active_user.SINR_attempts>=3):
			active_user_list.remove(active_user)
			reattempting_low_SINR.remove(active_user)
			global dropped_calls
			dropped_calls +=1 #this is when the call gets dropped
		return False


#checks if a channel is available or not for a user to attempt a call
def check_channel_availability():
	global total_channels
	global active_user_list
	#print(len(active_user_list))
	available_channels=total_channels-len(active_user_list)
	channel_availability_status= True if available_channels>0 else False
	return channel_availability_status

"""decides whether the RSL level for the attempting user is met and if he becomes an active or blocked user.
it also checks for the channel availability for the attempting user and blocks the user if there are no free channels"""
def attempting_user_status(attempting_user_list,selection):
	global active_user_list
	EIRP=rsl_calc.alter_EIRP(len(active_user_list),selection)
	current_active_users=[]
	blocked_users_list=[]
	blocked_calls_channel_capacity_list=[]
	global reattempting_low_RSL
	for i in attempting_user_list:
		i.RSL=rsl_calc.RSL(EIRP,i.location,i.angle) #assign RSL here for both current_second_attempting users and reattempting_low_RSL users
		if(i.RSL>minimum_RSL):
			if(not check_channel_availability()):
				global blocked_calls_channel_capacity
				blocked_calls_channel_capacity_list.append(i)
				#if i in attempting_user_list: attempting_user_list.remove(i)
				blocked_calls_channel_capacity +=1
			else:
				active_user_list.append(i)
				current_active_users.append(i)
				if i in reattempting_low_RSL: reattempting_low_RSL.remove(i)
				i.call_duration=int(np.random.exponential(60,size=None)) #method that gives the call duration value for  a particular call
		else:
			i.RSL_attempts += 1
			if i not in reattempting_low_RSL: reattempting_low_RSL.append(i)
			if(i.RSL_attempts==3):
				global blocked_calls_signal_strength
				reattempting_low_RSL.remove(i)
				blocked_users_list.append(i)
				blocked_calls_signal_strength +=1 #this is when the call gets blocked

		

	return (current_active_users ,blocked_users_list,blocked_calls_channel_capacity_list)


#calculates SINR every second and checks if the active user meets the required SINR or not
def active_user_status(active_user_list):
	for i in  active_user_list:
		i.set_SINR(active_user_list) #calculates SINR value for every second keeping the EIRP=52dbm
		if(check_SINR(i)):
			if i in reattempting_low_SINR: reattempting_low_SINR.remove(i) #if the user meets the SINR condition before 3 consequitive checks, he should be removed fr
	return reattempting_low_SINR


#checks if the call duration and marks the call as complete if the call duration becomes 0
def check_call_duration(active_user_list):
	global completed_calls_count
	for i in active_user_list:
		if i.call_duration !=0: i.call_duration += -1
		if(i.call_duration==0):
			active_user_list.remove(i)
			completed_calls_count +=1


#prints the desired statistics for every two minutes
def print_variables(time):
	retrials_RSL_list = [i.RSL_attempts-1 for i in reattempting_low_RSL]
	print("number of call attempts not counting retries:" + str(total_attempting_user_count))
	print("total number of attempts including retries is", total_attempting_user_count+sum(retrials_RSL_list)+3*blocked_calls_signal_strength)
	print("number of users retrying", len(reattempting_low_RSL))
	print("number of dropped calls: ", dropped_calls)
	print("number of blocked calls due to signal strength :"+str(blocked_calls_signal_strength))
	print("number of blocked calls due to channel capacity: "+str(blocked_calls_channel_capacity))
	print("number of successfully completed calls:"+ str(completed_calls_count))
	print("number of calls in progress in any given time: "+str(len(active_user_list)))
	print("number of failed calls: "+str(blocked_calls_signal_strength+blocked_calls_channel_capacity+dropped_calls))
	print("current cell radius is: "+str(user_loc.get_maximum_radius(active_user_list)))
	print("**************************************************************")



print("**************Cell Statistics****************")
selection=input("Enter 1 for admission control \n 0 for no admission control: ")
for i in range(7200):
	#global attempting_user_list
	[current_second_attempting_users,total_attempting_user_count]=user_selection.assign_locations(len(active_user_list)+len(attempting_user_list))
	reattempting_low_SINR= active_user_status(active_user_list)
	if(i != 0 and len(active_user_list)>0):
		check_call_duration(active_user_list)
	attempting_user_list = attempting_user_list+current_second_attempting_users
	current_active_users,blocked_users_list,blocked_calls_channel_capacity_list = attempting_user_status(attempting_user_list,selection)
	attempting_user_list = [i for i in attempting_user_list if i not in (current_active_users+blocked_users_list+blocked_calls_channel_capacity_list)]
	if(i%120==0):	
		print_variables(i)
print("time taken: ",time.time()-start_t)
print("Ratio of dropped calls to completed calls",dropped_calls/completed_calls_count)