import csv
from copy import deepcopy

def findnextbsindex(matrix, num):
	num += 1
	while num < (len(matrix)):
		if matrix[num][0] == -2:
			return num
		num += 1
	return -1

def getendpoints(selected, matrix):
	scount = 0
	currentbs = findnextbsindex(matrix, 0)
	oldbs = currentbs
	for i in range(len(matrix)):
		if matrix[i][0] == -1:
			if selected[scount][1] == 'r':
				userpos = selected[scount][0]
				bspos = matrix[currentbs][1]
				selected[scount].append(userpos) #left endpoint
				selected[scount].append(bspos + (bspos - userpos)) #right endpoint
			elif selected[scount][1] == 'l':
				userpos = selected[scount][0]
				bspos = matrix[oldbs][1]
				selected[scount].append(bspos - (userpos - bspos)) #left endpoint
				selected[scount].append(userpos) #right endpoint
			scount += 1
		else:
			oldbs = currentbs
			currentbs = findnextbsindex(matrix, currentbs)
			
def assigncoloring(selected, graph, users):
	usedcolors = [[1, selected[0][0]]]
	selected[0].append(1)
	for i in range(1, len(selected)):
		temppossiblecolors = deepcopy(usedcolors)
		for j in range(i):
			current = 0
			temp = 0
			if selected[i][1] == 'l':
				current = users.index(selected[i][0]) + 1
			else:
				current = users.index(selected[i][0]) + 1 + len(users)
			if selected[j][1] == 'l':
				temp = users.index(selected[j][0]) + 1
			else:
				temp = users.index(selected[j][0]) + 1 + len(users)
			if temp in graph[current]:
				if ([selected[j][4],selected[j][0]]) in temppossiblecolors:
					temppossiblecolors.remove([selected[j][4],selected[j][0]])
		
		if not temppossiblecolors:
			usedcolors.append([usedcolors[len(usedcolors) - 1][0] + 1, selected[i][0]])
			selected[i].append(usedcolors[len(usedcolors) - 1][0])
		else:
			right = 0
			color = 0
			for j in temppossiblecolors:
				for k in range(len(selected)):
					if selected[k][0] == j[1]:
						if selected[k][3] > right:
							right = selected[k][3]
							color = selected[k][4]
						break
			selected[i].append(color)
			for k in range(len(usedcolors)):
				if usedcolors[k][0] == color:
					usedcolors[k][1] = selected[i][0]
			
	print len(usedcolors)
	
if __name__ == '__main__':
	ipfile = open('1DJBSInput.txt', 'r')
	numofusers = int(ipfile.readline()) #number of agents
	numofbs = int(ipfile.readline()) #number of base stations
	
	grouplist = []
	matrix = []
	users = []
	basestations = []
	# -1 is a user while -2 is a base station
	tempgrouplist = []
	for i in range(0, int(numofusers)+int(numofbs)):
		temp = ipfile.readline()
		newtemp = str(temp)
		element = []
		tempchar = newtemp[0]
		if tempchar == 'u':
			tempchar = -1
			users.append(int(newtemp[1:].replace('\n', '')))
			tempgrouplist.append(int(newtemp[1:].replace('\n', '')))
		else:
			tempchar = -2
			basestations.append(int(newtemp[1:].replace('\n', '')))
			if tempgrouplist != []:
				grouplist.append(tempgrouplist)
				tempgrouplist = []
		element.append(tempchar)
		element.append(int(newtemp[1:].replace('\n', '')))
		matrix.append(element)

	if tempgrouplist != []:
		grouplist.append(tempgrouplist)
	
	
	arrows = []
	with open('constraintfile.lp.csv', 'rb') as f:
		reader = csv.reader(f, delimiter = ';')
		arrows = list(reader)
	
	arrows = arrows[2:]
	k = float(arrows[0][1])
	print k
	
	arrows = arrows[1:]
	selected = []
	for i in range(len(arrows)):
		temp = arrows[i]
		if temp[0][0] == 'l':
			tempnum = float(temp[1])
			tempnum = int(tempnum + 0.5)
			if tempnum == 1:
				selected.append(temp[0])
			else:
				temptemp = temp[0][1:]
				selected.append('r'+temptemp)
	
	for i in range(len(selected)):
		temp = []
		temp1 = int(selected[i][1:])
		temp2 = selected[i][0]
		temp.append(temp1)
		temp.append(temp2)
		selected[i] = temp
	
	selected.sort()
	
	getendpoints(selected, matrix)
	selected.sort(key=lambda x: x[2])
	
	graph = {}
	array = []
	with open('stage1.csv', 'rb') as f:
		reader = csv.reader(f)
		array = list(reader)
	for i in range(len(array)):
		graph[i+1] = map(int, array[i])
	
	assigncoloring(selected, graph, users)
	
