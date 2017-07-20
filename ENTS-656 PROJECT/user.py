
"""
This module defines each of the users as a class and initializes them with a unique id and location and the angle(polar coordinates)
The angle is used during the shadowing value configuration
It has other needful attributes like call duration which keeps track of the active user call duration
RSL which is determined when the user is created based on his location
RSL_attempts and SINR attempts which keep a track of the users retrials due to low RSL and SINR respectively
"""
import rsl_calculation as rsl_c
import sinr_calculation as sinr_c
total_attempting_users = 0
class user:
	def __init__(self,user_id,location,angle):
		self.user_id=user_id
		self.location=location
		self.angle=angle
		self.call_duration=0
		self.RSL=0
		self.RSL_attempts=0
		self.SINR_attempts=0

	def set_SINR(self,active_user_list):
		EIRP=52
		self.SINR=sinr_c.cal_SINR(len(active_user_list),self.RSL)










	 
