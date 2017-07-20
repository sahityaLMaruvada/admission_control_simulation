
import math
#calculates and returns Signal level for SINR calculation
def Signal_level(RSL):
	PG=20 #db
	Signal_level=RSL+PG
	return Signal_level

#calculates and returns SINR
def cal_SINR(N,RSL):
	Interference_level_db= RSL+ 10*math.log10(N-1)if(N>1) else 0
	Interference_level_linear = 10**(Interference_level_db/10)
	noise_level_linear=10**(-110/10)
	total_noise_linear=noise_level_linear+Interference_level_linear
	total_noise_db=10*math.log10(total_noise_linear)
	SINR= Signal_level(RSL)-total_noise_db
	return SINR

