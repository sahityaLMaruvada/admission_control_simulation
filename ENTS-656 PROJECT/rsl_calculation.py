import userlocation as ul
import numpy as np
import math

#the below variables are used for calculating the shadowing value using the 10*10 square technique
side_length = 2000
sub_spilt = side_length//2
EIRP=52
shadow_values = np.random.lognormal(0,2,[side_length,side_length])
quadrant1 = shadow_values[:sub_spilt,sub_spilt:]
quadrant2 = shadow_values[:sub_spilt,:sub_spilt]
quadrant3 = shadow_values[sub_spilt:,:sub_spilt]
quadrant4 = shadow_values[:sub_spilt,:sub_spilt]

def PlCOST231(user_location):
	antenna_ht=50 #metresmobile_ht=0 #metres
	frequency=1900
	d= user_location
	B = 44.9 - 6.55 *math.log10(antenna_ht)
	PL = 46.3+33.9*math.log10(frequency)-13.82*math.log10(antenna_ht)+ B*math.log10(d)
	return PL


#calculates the EIRP when admission control is imposed, retuns updated EIRP which is later on passed as 
#a parameter for RSL calculation
def alter_EIRP(active_user_count,selection):
	global EIRP
	channel_decrease = 20 if selection=='1' else 57
	channel_increase =15 if selection=='1' else 0
	if(active_user_count>channel_decrease):
		EIRP = EIRP - 0.5 if EIRP >30 else 30
		#print(EIRP)
	elif(active_user_count<channel_increase):
		EIRP =EIRP+ 0.5 if EIRP <52 else 52
	else:
		pass
	return EIRP

def fading():
	fading= np.random.rayleigh()
	return 20*math.log10(fading)


def shadowing(radius,theta):
	x=radius*np.cos(theta)
	y=radius*np.sin(theta)
	theta = np.arctan(y/x)
	x=abs(np.int(x))
	y=abs(np.int(y))
	if(theta>=0 and theta<=np.pi/2):
		shadowing_val = quadrant1[x,y]
	elif(theta>np.pi/2 and theta <= np.pi):
		shadowing_val = quadrant2[x,y]
	elif(theta>np.pi and theta <= 3*(np.pi)/2):
		shadowing_val = quadrant3[x,y]
	else:
		shadowing_val = quadrant4[x,y]
	return shadowing_val


def RSL(EIRP,user_location,angle):
	call_active=0
	F=fading()
	S=shadowing(user_location,angle)	
	PL=PlCOST231(user_location)
	RSL = EIRP - PL + F + S
	return(RSL)

