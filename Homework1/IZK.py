import numpy as np
import math
import matplotlib.pyplot as plt
 
#Theory of IZK
#dV/dt = 0.04*v^2 + 5v + 140 - u + I
#du/dt = a(bv-u)

#time values
totalTime = 500 #total time to run for each injected current [msec]
t_startCurrent = 100 #time to start injecting current [msec]
t_stopCurrent = totalTime - 100 #time to stope injecting current [msec] 
dt = 0.1 #steps of time [msec] ... in order to differentiate membrane potential with respect to time, we need to move in steps of dt
timeArray =  np.arange(0, totalTime+dt, dt) #time intervals in array [msec] ... note: totalTime+dt makes totalTime inclusive

ARP = 2 #absolute refractory period [msec] The neuron cannot spike during this time. Note: For the sake of convenience, we ignore the relative refractory period
#Note: Value assigned to ARP has been taken from http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html

#parameters
a = 0.02
b = 0.2
c = -65.0
d = 8.0


v = np.zeros(len(timeArray)) #membrane potential [mV]
v[0] = -70 #resting potential
u = np.zeros(len(timeArray)) #membrane recovery variable [mV]
u[0] = -14 #steady state

Vthresh = 30 #threshold value [mV]
Vspike = 35 #spike [mV]

#current values
StartCurrentValue = 10 #starting value for input current stimulus [nA]
EndCurrentValue = 12 #ending value for input current stimulus [nA]
CurrentSteps = 1 #steps to increment input current stimulus [nA]
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
			v[t] = v[t-1] + ((0.04*(v[t-1]*v[t-1])) + (5*v[t]) + 140 - u[t-1] + current[t-1])*dt
			u[t] = u[t-1] + (a*(b*v[t-1]-u[t-1]))*dt
			
			if v[t] > Vthresh: #membrane potential is over the threshold
				v[t] = Vspike #neuron spikes
				numSpikes += 1 #incrememnt number of spikes
				ARPOver = time+ARP #neuron goes into refractory period
					
		else:
			v[t] = c #reset v
			u[t] = u[t-1] + d #increase u
			
			
	firingRate[figNum-1] = numSpikes/((t_stopCurrent - t_startCurrent + 1)/1000) #time is converted from msec to sec, so that firingRate can be in Hz. numSpikes depends on input current so firing rate is a function of input current.
	
	dV = np.zeros(len(v)) #to show change in V in order to plot membrane potential decay
	for i in range(len(dV)):
		if i!=0:
			dV[i] = (v[i] - v[i-1])
			
	#plot graph to show membrane potential decay
	plt.figure(figNum)	
	plt.title("IZK Model: Membrane Potential decay when injected current I=%f" %I)
	plt.plot(timeArray, dV)
	plt.xlabel("Time (msec)")	
	plt.ylabel("Membrane Potential (mV)")
	plt.show()
	
	#plot graph to show spiking behavior
	plt.figure(figNum)	
	plt.title("IZK Model: Spiking Behavior when injected current I=%f" %I)
	plt.plot(timeArray, v)
	plt.xlabel("Time (msec)")	
	plt.ylabel("Membrane Potential (mV)")
	plt.show()
	figNum += 1
	
#plot graph of firing rate vs injected current
plt.figure(figNum)
plt.title("IZK Model: Firing Rate vs Injected Current")
plt.plot(IArray, firingRate)
plt.xlabel("Injected Current (nA)")
plt.ylabel("Firing Rate (Hz)")
plt.show()

	