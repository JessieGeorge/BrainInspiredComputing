import numpy as np
import math
import LIF

#program for a network of LIF neurons to form an XOR gate, trained with STDP

#	input1	|	input2	|	XOR
#	0		|	0		|	0
#	0		|	1		|	1
#	1		|	0		|	1
#	1		|	1		|	0

f = open('XORstdpOutput.txt', 'w') #output file

totalTime = 20 #total time to inject current (and also total time to run xor and hebbian learning)
#at a subscript t, timeOfSpikesArray is 1 if there is a spike at that time, and 0 if not
#let A be the timeOfSpikesArray for the first input neuron
A = LIF.getTimeOfSpikesArray(60, totalTime) #current of 50nA
#let B be the timeOfSpikesArray for the second input neuron
B = LIF.getTimeOfSpikesArray(5, totalTime) #current of 5nA

h1 = np.zeros(len(A)) #h1 is the first neuron in the hidden layer which is a nand gate
h2 = np.zeros(len(A)) #h2 is the second neuron in the hidden layer which is an or gate
o = np.zeros(len(A)) #the output neuron is an and gate (because and of the result from nand and the result from or in the hidden layer is the same as xor)
XORoutput = np.zeros(len(A)) #NOT involved in learning, just for output to see where the learning has errors
dt = 1 #time steps, i.e. update weights at this time

wmax = 1 #max weight
gamma = 0.5 #the value of a_2_corr = gamma
w_h1A = np.zeros(len(A)) #weight of the synapse where A is the presynaptic neuron and h1 is the postsynaptic neuron
w_h1B = np.zeros(len(A)) #weight of the synapse where B is the presynaptic neuron and h1 is the postsynaptic neuron
w_h2A = np.zeros(len(A)) #weight of the synapse where A is the presynaptic neuron and h2 is the postsynaptic neuron
w_h2B = np.zeros(len(A)) #weight of the synapse where B is the presynaptic neuron and h2 is the postsynaptic neuron
w_oh1 = np.zeros(len(A)) #weight of the synapse where h1 is the presynaptic neuron and the output nueron is the postsynaptic neuron
w_oh2 = np.zeros(len(A)) #weight of the synapse where h2 is the presynaptic neuron and the output nueron is the postsynaptic neuron

sumh1 = 0 #sum of activity so far for h1
sumh2 = 0 #sum of activity so far for h2
sumo = 0 #sum of activity so far for o
avgh1 = 0 #average activity of h1
avgh2 = 0 #average activity of h2
avgo = 0 #average activity of o

#for now it is set to len(A) i.e. an impossible value for timing, it is properly initialized when the presynaptic neuron first spikes
t_Af = len(A) #time that neuron A fires
t_Bf = len(A) #time that neuron B fires
t_h1f = len(A) #time that neuron h1 fires
t_h2f = len(A) #time that neuron h2 fires
t_of = len(A) #time that neuron o fires

def nandFunction(inp1, inp2):
	if inp1 == 1 and inp2 == 1:
		return 0
	else:
		return 1
		
def orFunction(inp1, inp2):
	if inp1 or inp2:
		return 1
	else:
		return 0
		
def andFunction(inp1, inp2):
	if inp1 and inp2:
		return 1
	else:
		return 0
		
#used only to check accuracy
def xorFunction(inp1, inp2):
	if inp1 != inp2:
		return 1
	else:
		return 0
		
#get the time differnce between when the presynaptic neuron fired and the postsynaptic neuron fired
def getTimeDifference(preFireTime, postFireTime):
	return preFireTime-postFireTime
		
for i in range(0, totalTime+dt, dt): #go from the zeroeth second to the tenth second
	
	if A[i] == 1:
		t_Af = i
	
	if B[i] == 1:
		t_Bf = i
		
	#equations to update weights based on firing times and calculate output for h1
	h1[i] = nandFunction(A[i],B[i])
	if h1[i] == 1:
		t_h1f = i
	
	timediff_h1A = getTimeDifference(t_Af, t_h1f)
	if t_Af == len(A) and t_h1f == len(A): #neither have spiked yet
		w_h1A[i] = 0 
	elif	timediff_h1A <=0: #pre spike before post, increase weight
		w_h1A[i] = 1
	else:	#pre spike after post, decrease weight
		w_h1A[i] = -1
		
	timediff_h1B = getTimeDifference(t_Bf, t_h1f)
	if t_Bf == len(A) and t_h1f == len(A): #neither have spiked yet
		w_h1B[i] = 0 
	elif	timediff_h1B <=0: #pre spike before post, increase weight
		w_h1B[i] = 1
	else:	#pre spike after post, decrease weight
		w_h1B[i] = -1
	
	#equations to update weights based on firing times and calculate output for h2
	h2[i] = orFunction(A[i],B[i])
	if h2[i] == 1:
		t_h2f = i
	
	timediff_h2A = getTimeDifference(t_Af, t_h2f)
	if t_Af == len(A) and t_h2f == len(A): #neither have spiked yet
		w_h2A[i] = 0
	elif	timediff_h2A <=0: #pre spike before post, increase weight
		w_h2A[i] = 1
	else:	#pre spike after post, decrease weight
		w_h2A[i] = -1
		
	timediff_h2B = getTimeDifference(t_Bf, t_h2f)
	if t_Bf == len(A) and t_h2f == len(A): #neither have spiked yet
		w_h2B[i] = 0
	elif	timediff_h2B <=0: #pre spike before post, increase weight
		w_h2B[i] = 1
	else:	#pre spike after post, decrease weight
		w_h2B[i] = -1
	
	#equations to update weights based on firing times and calculate output for o
	o[i] = andFunction(h1[i],h2[i])
	if o[i] == 1:
		t_of = i
	
	timediff_oh1 = getTimeDifference(t_h1f, t_of)
	if t_h1f == len(A) and t_of == len(A): #neither have spiked yet
		w_oh1[i] = 0
	elif	timediff_oh1 <=0: #pre spike before post, increase weight
		w_oh1[i] = 1
	else:	#pre spike after post, decrease weight
		w_oh1[i] = -1
		
	timediff_oh2 = getTimeDifference(t_h2f, t_of)
	if t_h2f == len(A) and t_of == len(A): #neither have spiked yet
		w_oh2[i] = 0
	elif	timediff_oh2 <=0: #pre spike before post, increase weight
		w_oh2[i] = 1
	else:	#pre spike after post, decrease weight
		w_oh2[i] = -1
	
	XORoutput[i] = xorFunction(A[i], B[i]) #xor output, not for learning just for output to check accuracy

#write to output file
f.write("INPUT AND OUTPUT FOR THE XOR GATE\n")
f.write(" first input neuron spike timings = %12s\n" % (A)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("second input neuron spike timings = %12s\n" % (B)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                       XOR output = %12s\n" % (XORoutput)) #the XOR output
f.write("                   learned output = %12s\n" % (o)) #the learned output
f.write("\n")
f.write("\n")
f.write("                 spike train for A = %12s\n" % (A)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                spike train for h1 = %12s\n" % (h1)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("weight of synapse between h1 and A = %12s\n" % (w_h1A)) #1 if pre spikes before post, -1 if pre spikes after post, 0 if neither have spiked
f.write("\n")
f.write("\n")
f.write("                 spike train for B = %12s\n" % (B)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                spike train for h1 = %12s\n" % (h1)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("weight of synapse between h1 and B = %12s\n" % (w_h1B)) #1 if pre spikes before post, -1 if pre spikes after post, 0 if neither have spiked
f.write("\n")
f.write("\n")
f.write("                 spike train for A = %12s\n" % (A)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                spike train for h2 = %12s\n" % (h2)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("weight of synapse between h2 and A = %12s\n" % (w_h2A)) #1 if pre spikes before post, -1 if pre spikes after post, 0 if neither have spiked
f.write("\n")
f.write("\n")
f.write("                 spike train for B = %12s\n" % (B)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                spike train for h2 = %12s\n" % (h2)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("weight of synapse between h2 and B = %12s\n" % (w_h2B)) #1 if pre spikes before post, -1 if pre spikes after post, 0 if neither have spiked
f.write("\n")
f.write("\n")
f.write("                spike train for h1 = %12s\n" % (h1)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                 spike train for o = %12s\n" % (o)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("weight of synapse between o and h1 = %12s\n" % (w_oh1)) #1 if pre spikes before post, -1 if pre spikes after post, 0 if neither have spiked
f.write("\n")
f.write("\n")
f.write("                spike train for h2 = %12s\n" % (h2)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                 spike train for o = %12s\n" % (o)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("weight of synapse between o and h2 = %12s\n" % (w_oh2)) #1 if pre spikes before post, -1 if pre spikes after post, 0 if neither have spiked
f.close()
