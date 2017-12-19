import numpy as np
import math
import OnOffCell

'''
LINE DETECTOR PROGRAM TO DETECT HORIZONTAL LINES
'''

'''
A line detector has a sequence of on cells sandwiched between 2 sequences of off cells. 
Example:
x x x 
o o o 
x x x 

x = off cell
o = on cell

3 on cells making a horizontal line:
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 1 0 1 0 1 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
'''
	
#function to check if a matrix of cells contains a horizontal line
def horizontalLineDetector(rows, cols, matrix):

	#print the matrix
	f.write("The matrix of cells is: \n")
	for i in range(rows):
		for j in range(cols):
			f.write("%d " %(matrix[i][j]))
		f.write("\n")
		
	#represents a single cell from the cells matrix
	subgrid = [[0, 0, 0],
			   [0, 0, 0],
			   [0, 0, 0]]
					
	bools = [False, False, False, False, False, False, False, False, False]	 #booleans will be true if that sub-grid is an on cell
	boolCount = 0 #boolCount to control position in bools list

	for i in range(0, rows-2, 1): #sub-grids should fit inside cells matrix
		#f.write("i = %d\n" %(i))
		for j in range(0, cols-2, 2): #sub-grids should fit inside cells matrix
			#f.write("j = %d\n" %(j))
			
			#initialize sub-grid
			k = j
			subgrid[0][0] = matrix[i][k]
			subgrid[0][1] = matrix[i][k+1]
			subgrid[0][2] = matrix[i][k+2]
			subgrid[1][0] = matrix[i+1][k]
			subgrid[1][1] = matrix[i+1][k+1]
			subgrid[1][2] = matrix[i+1][k+2]
			subgrid[2][0] = matrix[i+2][k]
			subgrid[2][1] = matrix[i+2][k+1]
			subgrid[2][2] = matrix[i+2][k+2]
			#f.write("%s\n" %(subgrid))
			#f.write("\n")
			bools[boolCount] = OnOffCell.checkOnCell(5,20,subgrid)
			boolCount += 1
			
	#f.write("%s\n" %(bools))
	#f.write("\n")

	containsHorizontalLine = False
	
	if bools[0]==True and bools[1]==True and bools[2]==True: #horizontal line on the top of cells matrix
		f.write("OUTPUT: Yes, it contains a horizontal line towards the top of matrix\n")
		containsHorizontalLine = True
	if bools[3]==True and bools[4]==True and bools[5]==True: #horizontal line in the middle of cells matrix
		f.write("OUTPUT: Yes, it contains a horizontal line in the middle of matrix\n")
		containsHorizontalLine = True
	if bools[6]==True and bools[7]==True and bools[8]==True: #horizontal line on the bottom of cells matrix
		f.write("OUTPUT: Yes, it contains a horizontal line towards the bottom of matrix\n")
		containsHorizontalLine = True
		
	if containsHorizontalLine == False:
		f.write("OUTPUT: It does not contain a horizontal line\n")
		
	f.write("\n")
		
f = open('LDNoutput.txt', 'w') #output file

rows = 5
cols = 7

f.write("LINE DETECTOR to detect horizontal line\n")
f.write("\n")

f.write("Testing with horizontal line i.e. 0degree, 180degree or 360degree\n")
#0degree, 180degree, 360degree line
#horizontal line
test =  [[0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 1, 0, 1, 0, 1, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with 20 degree line, i.e same as 200 degree \n")
#20 degree line
#non-horizontal line
test =  [[0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 1, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with 40 degree line, i.e same as 220 degree \n")
#40 degree line
#non-horizontal line
test =  [[0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 1, 0, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with 80 degree line, i.e same as 260 degree \n")
#80 degree line
#non-horizontal line
test =  [[0, 0, 0, 0, 1, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 1, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with 90 degree line, i.e. same as 270 degree \n")
#90 degree line
#non-horizontal line
test =  [[0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)
	
f.write("Testing with 100 degree line, i.e. same as 280 degree \n")	
#100 degree line
#non-horizontal line
test =  [[0, 0, 1, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 1, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with 140 degree line, i.e. same as 320 degree \n")
#140 degree line
#non-horizontal line
test = 	[[0, 1, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 1, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with 160 degree line, i.e. same as 340 degree \n")
#160 degree line
#non-horizontal line
test = 	[[0, 0, 0, 0, 0, 0, 0],
		 [0, 1, 0, 0, 0, 0, 0],
		 [0, 0, 0, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with horizontal line towards the top \n")
#horizontal line
test =  [[0, 0, 0, 0, 0, 0, 0],
		 [0, 1, 0, 1, 0, 1, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)

f.write("Testing with horizontal line towards the bottom \n")
#horizontal line
test =  [[0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0],
		 [0, 1, 0, 1, 0, 1, 0],
		 [0, 0, 0, 0, 0, 0, 0]]
horizontalLineDetector(rows,cols,test)