import numpy as np
import math
import LIF

#program for a network of LIF neurons to form an XOR gate, with Hebbian learning

#	input1	|	input2	|	XOR
#	0		|	0		|	0
#	0		|	1		|	1
#	1		|	0		|	1
#	1		|	1		|	0

f = open('XORHebbOutput.txt', 'w') #output file
totalTime = 20 #total time to inject current (and also total time to run xor and hebbian learning)
#at a subscript t, timeOfSpikesArray is 1 if there is a spike at that time, and 0 if not
#let A be the timeOfSpikesArray for the first input neuron
A = LIF.getTimeOfSpikesArray(60, totalTime) #current of 50nA
#let B be the timeOfSpikesArray for the second input neuron
B = LIF.getTimeOfSpikesArray(5, totalTime) #current of 5nA

h1 = np.zeros(len(A)) #h1 is the first neuron in the hidden layer which is a nand gate
h2 = np.zeros(len(A)) #h2 is the second neuron in the hidden layer which is an or gate
o = np.zeros(len(A)) #the output neuron is an and gate (because and of the result from nand and the result from or in the hidden layer is the same as xor)
XORoutput = np.zeros(len(A)) #NOT involved in learning, just for output to see accuracy
dt = 1 #time steps, i.e. update weights at this time

#using Hebbian learning equation from lecture 5 slide 43
# dw_ij/dt = a_2_corr * v_j_pre * (v_i_post - theta)
#a_2_corr = gamma so we will use the notation gamma
#v_j_pre is the presynaptic activity
#v_i_post is the postsynaptic activity
#theta is the average postsynaptic activity so we will use avg appended by the name of the postsynaptic neuron

wmax = 1 #max weight
gamma = 0.5 #the value of a_2_corr = gamma
w_h1A = 0 #weight of the synapse where A is the presynaptic neuron and h1 is the postsynaptic neuron
w_h1B = 0 #weight of the synapse where B is the presynaptic neuron and h1 is the postsynaptic neuron
w_h2A = 0 #weight of the synapse where A is the presynaptic neuron and h2 is the postsynaptic neuron
w_h2B = 0 #weight of the synapse where B is the presynaptic neuron and h2 is the postsynaptic neuron
w_oh1 = 0 #weight of the synapse where h1 is the presynaptic neuron and the output nueron is the postsynaptic neuron
w_oh2 = 0 #weight of the synapse where h2 is the presynaptic neuron and the output nueron is the postsynaptic neuron

sumh1 = 0 #sum of activity so far for h1
sumh2 = 0 #sum of activity so far for h2
sumo = 0 #sum of activity so far for o
avgh1 = 0 #average activity of h1
avgh2 = 0 #average activity of h2
avgo = 0 #average activity of o

def nandFunction(inp1, inp2):
	if inp1 == 1 and inp2 == 1:
		return 0
	else:
		return 1
		
def orFunction(inp1, inp2):
	if inp1 == 1 or inp2 == 1:
		return 1
	else:
		return 0
		
def andFunction(inp1, inp2):
	if nandFunction(inp1, inp2) and orFunction(inp1, inp2):
		return 1
	else:
		return 0
		
for i in range(0, totalTime+dt, dt): #go from the zeroeth second to the tenth second
	
	#increment sum of activity and calculate average activity
	if i != 0:
		sumh1 += h1[i]
		avgh1 = sumh1 / i
		sumh2 += h2[i]
		avgh2 = sumh2 / i
		sumo += o[i]
		avgo = sumo / i
		
	#equations to update weights and calculate output for h1
	teacherNeuron = nandFunction(A[i],B[i])
	w_h1A += dt * gamma * A[i] * (teacherNeuron - avgh1) #using Hebbian learning equation from lecture 5 slide 43
	w_h1B += dt * gamma * B[i] * (teacherNeuron - avgh1) #using Hebbian learning equation from lecture 5 slide 43
	w_h1A = wmax - w_h1A #soft bound, lecture 5 slide 29
	w_h1B = wmax - w_h1B #soft bound, lecture 5 slide 29
	h1[i] = (w_h1A * A[i]) + (w_h1B * B[i])
	'''
	print("w_h1A %d" % (w_h1A))
	print("w_h1B %d" % (w_h1B))
	print("h1[%d] %d" % (i, h1[i]))
	'''
	
	#equations to update weights and calculate output for h2
	teacherNeuron = orFunction(A[i],B[i])
	w_h2A += dt * gamma * A[i] * (teacherNeuron - avgh2) #using Hebbian learning equation from lecture 5 slide 43
	w_h2B += dt * gamma * B[i] * (teacherNeuron - avgh2) #using Hebbian learning equation from lecture 5 slide 43
	w_h2A = wmax - w_h2A #soft bound, lecture 5 slide 29
	w_h2B = wmax - w_h2B #soft bound, lecture 5 slide 29
	h2[i] = (w_h2A * A[i]) + (w_h2B * B[i])
	'''
	print("w_h2A %d" % (w_h2A))
	print("w_h2B %d" % (w_h2B))
	print("h2[%d] %d" % (i, h2[i]))
	'''
	
	#equations to update weights and calculate output for o
	teacherNeuron = andFunction(h1[i],h2[i])
	w_oh1 += dt * gamma * h1[i] * (teacherNeuron - avgo) #using Hebbian learning equation from lecture 5 slide 43
	w_oh2 += dt * gamma * h2[i] * (teacherNeuron - avgo) #using Hebbian learning equation from lecture 5 slide 43
	w_oh1 = wmax - w_oh1 #soft bound, lecture 5 slide 29
	w_oh2 = wmax - w_oh2 #soft bound, lecture 5 slide 29
	o[i] = (w_oh1 * h1[i]) + (w_oh2 * h2[i]) #the learned output
	
	#to keep within bounds
	if o[i] > 1:
		o[i] = 1
	if o[i] <= 0:
		o[i] = 0
	'''
	print("w_oh1 %d" % (w_oh1))
	print("w_oh2 %d" % (w_oh2))
	print("o[%d] %d" % (i, o[i]))
	'''
	'''
	print("WEIGHTS")
	print("w_h1A = ", w_h1A)
	print("w_h1B = ", w_h1B)
	print("w_h2A = ", w_h2A)
	print("w_h2B = ", w_h2B)
	print("w_oh1 = ", w_oh1)
	print("w_oh2 = ", w_oh2)
	'''
	
	XORoutput[i] = andFunction(A[i], B[i]) #xor output, not for learning just for output to check accuracy


f.write("INPUT AND OUTPUT FOR THE XOR GATE\n")
f.write(" first input neuron spike timings = %12s\n" % (A)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("second input neuron spike timings = %12s\n" % (B)) #at the nth subscript, it is 1 if neuron spiked at nth second, else 0
f.write("                       XOR output = %12s\n" % (XORoutput)) #the XOR output
f.write("                   learned output = %12s\n" % (o)) #the learned output

f.close()

