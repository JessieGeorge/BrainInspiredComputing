import numpy as np
import math
import matplotlib.pyplot as plt
 
#Theory of LIF
#tau_m *(dV_m/dt) = -V_m(t) + (R_m * I(t)) ...Equation 1 (equation taken from assignment question)
#where tau_m = R_m * C_m
#In the absence of an injected current, the membrane potential of the cell decays to a resting membrane potential, so to be more accurate we can write Equation 1 as:
#tau_m *(dV_m/dt) = Vrest - V_m(t) + (R_m * I(t)) ...Equation 2
#Solving Equation 2 we get:
#V_m(t) = Vrest + (R_m * I(t)) + (V_m(t_0) - Vrest - (R_m * I(t))) * e^(-(t - t_0)/tau_m) ... Equation 3
#where t is the present time step and t_0 is the previous time step. e is Euler's constant. The difference in time is t - t_0 which is dt.
#From Equation 3, we see that as t tends to infinity, V_m tends to Vrest + (R_m * I(t))
#Let Vinf = Vrest + (R_m * I(t)) be the membrane potential at infinity. 
#Plugging Vinf and dt into equation 3, we get:
#V_m(t) = Vinf + (V_m(t_0) - Vinf) * e^(-dt/tau_m) ... Equation 4
#I use Equation 4 to calculate membrane potential in my code.
#I referred to http://neuroscience.ucdavis.edu/goldman/Tutorials_files/Integrate%26Fire.pdf for help with theory

#initializing properties of the cell membrane
R_m = 10 #resistance of the cell membrane [MOhm]
C_m = 1 #capacitance of the cell membrane [nF]
tau_m = R_m * C_m #time constant [msec]

#time values
totalTime = 500 #total time to run for each injected current [msec]
t_startCurrent = 100 #time to start injecting current [msec]
t_stopCurrent = totalTime - 100 #time to stope injecting current [msec] 
dt = 0.1 #steps of time [msec] ... in order to differentiate membrane potential with respect to time, we need to move in steps of dt
timeArray =  np.arange(0, totalTime+dt, dt) #time intervals in array [msec] ... note: totalTime+dt makes totalTime inclusive

ARP = 2 #absolute refractory period [msec] The neuron cannot spike during this time. Note: For the sake of convenience, we ignore the relative refractory period
#Note: Value assigned to ARP has been taken from http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html

#membrane potential values
Vrest = -70 #resting membrane potential [mV]
V_m = np.zeros(len(timeArray)) * Vrest # membrane potential array [mV] i.e membrane potential will be calculated for each time step, for now it is initialized to Vrest because there is no spike yet.
Vthresh = -55 #threshold potential [mV] ... Note: For the sake of convenience, we assume Vthresh remains constant i.e. threshold does not get higher and higher after consecutive spikes.
Vspike = 20 #spike value for membrane potential [mV]
Vdip = -75 #dip the membrane potential after a spike [mV] i.e. hyperpolarization
#Note: Values assigned to Vrest and Vthresh have been taken from https://teaching.ncl.ac.uk/bms/wiki/index.php/Action_potential

#current values
StartCurrentValue = 1.43 #starting value for input current stimulus [nA]
EndCurrentValue = 1.63 #ending value for input current stimulus [nA]
CurrentSteps = 0.04 #steps to increment input current stimulus [nA]
IArray = np.arange(StartCurrentValue, EndCurrentValue+CurrentSteps, CurrentSteps) #array of input current stimuli [nA] ... note: EndCurrentValue+CurrentSteps makes EndCurrentValue inclusive

firingRate = np.zeros(len(IArray)) #for each input current stimulus, calculate firingRate [Hz]

figNum = 1 #to count the figure number to plot graph

#for each current value in the current array
for I in IArray:

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
				
		else: #still in absolute refractory period
			V_m[t] = Vdip #hyperpolarization after spike		

	firingRate[figNum-1] = numSpikes/((t_stopCurrent - t_startCurrent + 1)/1000) #time is converted from msec to sec, so that firingRate can be in Hz. numSpikes depends on input current so firing rate is a function of input current.
	
	dV = np.zeros(len(V_m)) #to show change in V in order to plot membrane potential decay
	for i in range(len(dV)):
		if i!=0:
			dV[i] = (V_m[i] - V_m[i-1])
			
	#plot graph to show membrane potential decay
	plt.figure(figNum)	
	plt.title("LIF Model: Membrane Potential decay when injected current I=%f" %I)
	plt.plot(timeArray, dV)
	plt.xlabel("Time (msec)")	
	plt.ylabel("Membrane Potential (mV)")
	plt.show()
	
	#plot graph to show spiking behavior
	plt.figure(figNum)	
	plt.title("LIF Model: Spiking Behavior when injected current I=%f" %I)
	plt.plot(timeArray, V_m)
	plt.xlabel("Time (msec)")	
	plt.ylabel("Membrane Potential (mV)")
	plt.show()
	figNum += 1
	
#plot graph of firing rate vs injected current
plt.figure(figNum)
plt.title("LIF Model: Firing Rate vs Injected Current")
plt.plot(IArray, firingRate)
plt.xlabel("Injected Current (nA)")
plt.ylabel("Firing Rate (Hz)")
plt.show()

	