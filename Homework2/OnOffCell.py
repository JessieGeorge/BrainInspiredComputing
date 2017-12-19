import numpy as np
import math

'''
HELPER PROGRAM FOR LDN
'''

#function to check if it is an on cell, given the stimulus current in nA, total time to inject the current in msec, and a 3x3 grid representing the dendrites tied to other neurons that have spiked or not spiked
def checkOnCell(currentArg, totalTimeArg, grid):
	#initializing properties of the cell membrane
	R_m = 10 #resistance of the cell membrane [MOhm]
	C_m = 1 #capacitance of the cell membrane [nF]
	tau_m = R_m * C_m #time constant [msec]

	#time values
	totalTime = totalTimeArg #total time to inject current [msec]
	t_startCurrent = 0 #time to start injecting current [msec]
	t_stopCurrent = totalTime #time to stop injecting current [msec] 
	dt = 1 #steps of time [msec] ... in order to differentiate membrane potential with respect to time, we need to move in steps of dt
	timeArray =  np.arange(0, totalTime+dt, dt) #time intervals in array [msec] ... note: totalTime+dt makes totalTime inclusive
	timeOfSpikesArray = np.zeros(len(timeArray)) #at a subscript t, timeOfSpikesArray is 1 if there is a spike at that time, and 0 if not
	
	ARP = 2 #absolute refractory period [msec] The neuron cannot spike during this time. Note: For the sake of convenience, we ignore the relative refractory period
	#Note: Value assigned to ARP has been taken from http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html

	#membrane potential values
	Vrest = -70 #resting membrane potential [mV]
	V_m = np.zeros(len(timeArray)) * Vrest # membrane potential array [mV] i.e membrane potential will be calculated for each time step, for now it is initialized to Vrest because there is no spike yet.
	Vthresh = -55 #threshold potential [mV] ... Note: For the sake of convenience, we assume Vthresh remains constant i.e. threshold does not get higher and higher after consecutive spikes.
	Vspike = 20 #spike value for membrane potential [mV]
	Vdip = -75 #dip the membrane potential after a spike [mV] i.e. hyperpolarization
	#Note: Values assigned to Vrest and Vthresh have been taken from https://teaching.ncl.ac.uk/bms/wiki/index.php/Action_potential

	I = currentArg #the current to inject [nA]

	firingRate = 0 #for each input current stimulus, calculate firingRate [Hz]

	numSpikes = 0 #counter for the number of spikes
		
	beginNoCurrent = np.zeros(int(t_startCurrent/dt)) #no current until the time to start current
	injectCurrent = np.ones(int((t_stopCurrent - t_startCurrent + 1)/dt)) * I #duration for which we inject the current
	endNoCurrent = np.zeros(int((totalTime - t_stopCurrent)/dt)) #no current after the time to stop current

	#append all arrays into one array called current
	current = beginNoCurrent
	current = np.append(current, injectCurrent)
	current = np.append(current, endNoCurrent) 
		
	ARPOver = 0 #the neuron can now be allowed to spike [msec]. This value is initialized to zero, but it will be calculated after spike time.
		
	#run a loop through timeArray with counter t
	for t, time in enumerate(timeArray):
		
		if time>ARPOver: #absolute refractory period is over
			Vinf = Vrest + current[t] * R_m #V at infinity, i.e. membrane potential exponentially decays towards Vinf
			V_m[t] = Vinf + ((V_m[t-1] - Vinf) * math.exp(-dt/tau_m)) #calculate membrane potential (explanation given in theory note above)
			
			if V_m[t] > Vthresh: #membrane potential is over the threshold
				V_m[t] = Vspike #neuron spikes
				numSpikes += 1 #incrememnt number of spikes
				ARPOver = time+ARP #neuron goes into refractory period
				timeOfSpikesArray[t] = 1
				
		else: #still in absolute refractory period
			V_m[t] = Vdip #hyperpolarization after spike		

	firingRate = numSpikes/((t_stopCurrent - t_startCurrent + 1)/1000) #time is converted from msec to sec, so that firingRate can be in Hz. numSpikes depends on input current so firing rate is a function of input current.
	#print ("firingRate = ", firingRate)
	#print ("timeOfSpikesArray = ", timeOfSpikesArray)
	
	onCell = [[0, 0, 0],
			  [0, 1, 0],
			  [0, 0, 0]]
	
	if grid == onCell:
		return True
	
	else:
		return False
		
#function to check if it is an off cell, given the stimulus current in nA, total time to inject the current in msec, and a 3x3 grid representing the dendrites tied to other neurons that have spiked or not spiked
def checkOffCell(currentArg, totalTimeArg, grid):
	#initializing properties of the cell membrane
	R_m = 10 #resistance of the cell membrane [MOhm]
	C_m = 1 #capacitance of the cell membrane [nF]
	tau_m = R_m * C_m #time constant [msec]

	#time values
	totalTime = totalTimeArg #total time to inject current [msec]
	t_startCurrent = 0 #time to start injecting current [msec]
	t_stopCurrent = totalTime #time to stop injecting current [msec] 
	dt = 1 #steps of time [msec] ... in order to differentiate membrane potential with respect to time, we need to move in steps of dt
	timeArray =  np.arange(0, totalTime+dt, dt) #time intervals in array [msec] ... note: totalTime+dt makes totalTime inclusive
	timeOfSpikesArray = np.zeros(len(timeArray)) #at a subscript t, timeOfSpikesArray is 1 if there is a spike at that time, and 0 if not
	
	ARP = 2 #absolute refractory period [msec] The neuron cannot spike during this time. Note: For the sake of convenience, we ignore the relative refractory period
	#Note: Value assigned to ARP has been taken from http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html

	#membrane potential values
	Vrest = -70 #resting membrane potential [mV]
	V_m = np.zeros(len(timeArray)) * Vrest # membrane potential array [mV] i.e membrane potential will be calculated for each time step, for now it is initialized to Vrest because there is no spike yet.
	Vthresh = -55 #threshold potential [mV] ... Note: For the sake of convenience, we assume Vthresh remains constant i.e. threshold does not get higher and higher after consecutive spikes.
	Vspike = 20 #spike value for membrane potential [mV]
	Vdip = -75 #dip the membrane potential after a spike [mV] i.e. hyperpolarization
	#Note: Values assigned to Vrest and Vthresh have been taken from https://teaching.ncl.ac.uk/bms/wiki/index.php/Action_potential

	I = currentArg #the current to inject [nA]

	firingRate = 0 #for each input current stimulus, calculate firingRate [Hz]

	numSpikes = 0 #counter for the number of spikes
		
	beginNoCurrent = np.zeros(int(t_startCurrent/dt)) #no current until the time to start current
	injectCurrent = np.ones(int((t_stopCurrent - t_startCurrent + 1)/dt)) * I #duration for which we inject the current
	endNoCurrent = np.zeros(int((totalTime - t_stopCurrent)/dt)) #no current after the time to stop current

	#append all arrays into one array called current
	current = beginNoCurrent
	current = np.append(current, injectCurrent)
	current = np.append(current, endNoCurrent) 
		
	ARPOver = 0 #the neuron can now be allowed to spike [msec]. This value is initialized to zero, but it will be calculated after spike time.
		
	#run a loop through timeArray with counter t
	for t, time in enumerate(timeArray):
		
		if time>ARPOver: #absolute refractory period is over
			Vinf = Vrest + current[t] * R_m #V at infinity, i.e. membrane potential exponentially decays towards Vinf
			V_m[t] = Vinf + ((V_m[t-1] - Vinf) * math.exp(-dt/tau_m)) #calculate membrane potential (explanation given in theory note above)
			
			if V_m[t] > Vthresh: #membrane potential is over the threshold
				V_m[t] = Vspike #neuron spikes
				numSpikes += 1 #incrememnt number of spikes
				ARPOver = time+ARP #neuron goes into refractory period
				timeOfSpikesArray[t] = 1
				
		else: #still in absolute refractory period
			V_m[t] = Vdip #hyperpolarization after spike		

	firingRate = numSpikes/((t_stopCurrent - t_startCurrent + 1)/1000) #time is converted from msec to sec, so that firingRate can be in Hz. numSpikes depends on input current so firing rate is a function of input current.
	#print ("firingRate = ", firingRate)
	#print ("timeOfSpikesArray = ", timeOfSpikesArray)
	
	offCell = [[1, 1, 1],
			   [1, 0, 1],
			   [1, 1, 1]]
	
	if grid == offCell:
		return True
	
	else:
		return False
	
	
	