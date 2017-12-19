import numpy as np
import math
import matplotlib.pyplot as plt
 
#Theory of HH model
#C*(dV/dt) = I - g_Na*m^3*h(V-V_Na) - g_K*n^4*(V-V_K) - g_L(V-V_L)

#initializing properties of the cell membrane
C = 10 #membrane capacitance per unit area [nF/mm^2]

#time values
totalTime = 500 #total time to run for each injected current [msec]
t_startCurrent = 100 #time to start injecting current [msec]
t_stopCurrent = totalTime - 100 #time to stope injecting current [msec] 
dt = 0.1 #steps of time [msec] ... in order to differentiate membrane potential with respect to time, we need to move in steps of dt
timeArray =  np.arange(0, totalTime+dt, dt) #time intervals in array [msec] ... note: totalTime+dt makes totalTime inclusive
ARP = 2 #absolute refractory period [msec] The neuron cannot spike during this time. Note: For the sake of convenience, we ignore the relative refractory period
#Note: Value assigned to ARP has been taken from http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html

#maximum conductance values
gMax_Na = 1200 #maximum conductance for sodium [microS/mm^2]
gMax_K = 360 #maximum conductance for potassium [microS/mm^2]
gMax_L = 3 #maximum conductance for leak [microS/mm^2]

#membrane potential values
E_Na = 50.0 #equilibrium potential for sodium [mV]
E_K = -77.0 #equilibrium potential for potassium [mV]
E_L = -54.387 #equilibrium potential for leak [mV]
Vrest = -65 #resting potential of cell membrane [mV]
V = np.ones(len(timeArray)) * Vrest #membrane potential array [mV] i.e membrane potential will be calculated for each time step, for now it is initialized to Vrest because there is no spike yet.
Vthresh = -10 #threshold potential [mV] ... Note: For the sake of convenience, we assume Vthresh remains constant i.e. threshold does not get higher and higher after consecutive spikes.
Vspike = 20 #spike value for membrane potential [mV]
Vdip = -60 #dip the membrane potential after a spike [mV] i.e. hyperpolarization

#ion channel values
mArray = np.zeros(len(timeArray)) #the proportion of sodium activation molecules
mArray[0] = 0.0529 #initialized to value of m_inf(-65) ... see equation for m_inf below
hArray = np.zeros(len(timeArray)) #the proportion of sodium inactivation molecules
hArray[0] = 0.5961 #initialized to value of h_inf(-65) ... see equation for h_inf below
nArray = np.zeros(len(timeArray)) #the proportion of potassium activation molecules
nArray[0] = 0.3177 #initialized to value of n_inf(-65) ... see equation for n_inf below

#current values
StartCurrentValue = 80 #starting value for input current stimulus [nA]
EndCurrentValue = 120 #ending value for input current stimulus [nA]
CurrentSteps = 10 #steps to increment input current stimulus [nA]
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
		
		#alpha determines the rate of transfer of ions from outside to inside the membrane ... rate of opening of ion channels
		#beta determines the rate of transfer of ions in the opposite direction ... rate of closing of ion channels
		#note: the following equations for alphas and betas are taken from http://neuroscience.ucdavis.edu/goldman/Tutorials_files/HodgkinHuxley.pdf
		#it is similar to equations 20, 21, 23, 24, 12 and 13 in the Hodgkin and Huxley 1952 research paper given in class
		alpha_m = 0.1 * (V[t-1]+40) / (1 - math.exp(-0.1*(V[t-1]+40)))
		beta_m = 4 * math.exp(-0.0556 * (V[t-1]+65))
		alpha_h = 0.07 * math.exp(-0.05 * (V[t-1]+65))
		beta_h = 1/(1+math.exp(-0.1 * (V[t-1]+35)))
		alpha_n = 0.01 * (V[t-1]+55)/(1-math.exp(-0.1*(V[t-1]+55)))
		beta_n = 0.125 * math.exp(-0.0125*(V[t-1]+65))
			
		#time constants for m,h,n
		tau_m = 1/(alpha_m+beta_m)
		tau_h = 1/(alpha_h+beta_h)
		tau_n = 1/(alpha_n+beta_n)
			
		
		#infinity values for m,h,n
		m_inf = alpha_m/(alpha_m+beta_m)
		h_inf = alpha_h/(alpha_h+beta_h)
		n_inf = alpha_n/(alpha_n+beta_n)
			
		#time constant and infinity value for V
		V_denominator = (gMax_Na * (mArray[t-1]**3) * hArray[t-1]) + (gMax_K * (nArray[t-1]**4)) + gMax_L
		tau_V = C / V_denominator			
		V_inf = (current[t] + (E_Na * gMax_Na * (mArray[t-1]**3) * hArray[t-1]) + (E_K * gMax_K * (nArray[t-1]**4)) + (E_L * gMax_L) )/V_denominator
			
		#update arrays
		mArray[t] = m_inf + (mArray[t-1] - m_inf) * math.exp(-dt/tau_m)
		hArray[t] = h_inf + (hArray[t-1] - h_inf) * math.exp(-dt/tau_h)
		nArray[t] = n_inf + (nArray[t-1] - n_inf) * math.exp(-dt/tau_n)
		V[t] = V_inf + (V[t-1] - V_inf) * math.exp(-dt/tau_m)
	
		if time>t_startCurrent and time>ARPOver: #neuron is allowed to spike because current is injected and absolute refractory period is over
			if V[t] > Vthresh: #membrane potential is over the threshold
				V[t] = Vspike #neuron spikes
				numSpikes += 1 #incrememnt number of spikes	
				ARPOver = time + ARP #neuron goes into refractory period
	
		elif time<=ARPOver: #still in absolute refractory period
			V[t] = Vdip #hyperpolarization after a spike
			
		else:
			continue #do nothing. i.e before we inject current we don't need spiking or hyperpolarization. 
	
	firingRate[figNum-1] = numSpikes/((t_stopCurrent - t_startCurrent + 1)/1000) #time is converted from msec to sec, so that firingRate can be in Hz. numSpikes depends on input current so firing rate is a function of input current.
	
	dV = np.zeros(len(V)) #to show change in V in order to plot membrane potential decay
	for i in range(len(dV)):
		if i!=0:
			dV[i] = (V[i] - V[i-1])
			
	#plot graph to show membrane potential decay
	plt.figure(figNum)	
	plt.title("HH Model: Membrane Potential decay when injected current I=%.2f" %I)
	plt.plot(timeArray, dV)
	plt.xlabel("Time (msec)")	
	plt.ylabel("Membrane Potential (mV)")
	plt.show()
	
	#plot graph to show spiking behavior
	plt.figure(figNum)	
	plt.subplot(2,1,1)
	plt.title("HH Model: Spiking Behavior when injected current I=%.2f" %I)
	plt.plot(timeArray, V, 'b') #blue
	plt.ylabel("Membrane Potential (mV)")
	plt.subplot(2,1,2)
	mhundredplot, = plt.plot(timeArray, 100*mArray, 'k', label='m*100') #black
	hhundredplot, = plt.plot(timeArray, 100*hArray, 'r', label='h*100') #red
	nhundredplot, = plt.plot(timeArray, 100*nArray, 'g', label='n*100') #green
	plt.xlabel("Time (msec)")	
	plt.ylabel("m*100, h*100, or n*100")
	plt.legend(handles = [mhundredplot,hhundredplot,nhundredplot], loc='upper left')
	plt.show()
	figNum += 1
	
#plot graph of firing rate vs injected current
plt.figure(figNum)
plt.title("HH Model: Firing Rate vs Injected Current")
plt.plot(IArray, firingRate)
plt.xlabel("Injected Current (nA)")
plt.ylabel("Firing Rate (Hz)")
plt.show()

	