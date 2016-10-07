# Assume users to left of leftmost BS and to right of rightmost BS exist
numofusers = 0
numofbs = 0

def inputData(grouplist, matrix, users, basestations):
	ipfile = open('1DJBSInput.txt', 'r')
	global numofusers, numofbs
	numofusers = int(ipfile.readline()) #number of agents
	numofbs = int(ipfile.readline()) #number of base stations

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
		
def createConflictGraph(confgraph):
	for i in range(numofusers * 2):
		confgraph.append([0] * numofusers * 2)
	for i in range(numofusers):
		confgraph[i][numofusers + i] = 1
		confgraph[numofusers + i][i] = 1
		
def GenericCaseConflict(grouplist, matrix, users, basestations, confgraph):
	grouplistcount = 1
	for i in range(numofbs - 1):
		#case 1
		for l in range(len(grouplist[grouplistcount - 1])):
			for r in range(len(grouplist[grouplistcount])):
				if grouplist[grouplistcount][r] - basestations[i] <= basestations[i] - grouplist[grouplistcount - 1][l]:
					confgraph[users.index(grouplist[grouplistcount][r])][numofusers + users.index(grouplist[grouplistcount - 1][l])] = 1
					confgraph[numofusers + users.index(grouplist[grouplistcount - 1][l])][users.index(grouplist[grouplistcount][r])] = 1
				if basestations[i] - grouplist[grouplistcount - 1][l] <= grouplist[grouplistcount][r] - basestations[i]:
					confgraph[users.index(grouplist[grouplistcount][r])][numofusers + users.index(grouplist[grouplistcount - 1][l])] = 1
					confgraph[numofusers + users.index(grouplist[grouplistcount - 1][l])][users.index(grouplist[grouplistcount][r])] = 1
		#case 2
		for r in range(len(grouplist[grouplistcount + 1])):
			for l in range(len(grouplist[grouplistcount])):
				if grouplist[grouplistcount + 1][r] - basestations[i + 1] <= basestations[i + 1] - grouplist[grouplistcount][l]:
					confgraph[users.index(grouplist[grouplistcount + 1][r])][numofusers + users.index(grouplist[grouplistcount][l])] = 1
					confgraph[numofusers + users.index(grouplist[grouplistcount][l])][users.index(grouplist[grouplistcount + 1][r])] = 1
				if basestations[i + 1] - grouplist[grouplistcount][l] <= grouplist[grouplistcount + 1][r] - basestations[i + 1]:
					confgraph[users.index(grouplist[grouplistcount + 1][r])][numofusers + users.index(grouplist[grouplistcount][l])] = 1
					confgraph[numofusers + users.index(grouplist[grouplistcount][l])][users.index(grouplist[grouplistcount + 1][r])] = 1
		#case 3
		for l in range(len(grouplist[grouplistcount])):
			for ll in range(len(grouplist[grouplistcount])):
				if grouplist[grouplistcount][ll] - basestations[i] > grouplist[grouplistcount][l] - basestations[i]:
					confgraph[users.index(grouplist[grouplistcount][ll])][users.index(grouplist[grouplistcount][l])] = 1
					confgraph[users.index(grouplist[grouplistcount][l])][users.index(grouplist[grouplistcount][ll])] = 1
		#case 4
		for r in range(len(grouplist[grouplistcount])):
			for rr in range(len(grouplist[grouplistcount])):
				if basestations[i + 1] - grouplist[grouplistcount][rr] > basestations[i + 1] - grouplist[grouplistcount][r]:
					confgraph[numofusers + users.index(grouplist[grouplistcount][rr])][numofusers + users.index(grouplist[grouplistcount][r])] = 1
					confgraph[numofusers + users.index(grouplist[grouplistcount][r])][numofusers + users.index(grouplist[grouplistcount][rr])] = 1
		#case 5
		for r in range(len(grouplist[grouplistcount])):
			for rr in range(len(grouplist[grouplistcount + 1])):
				if basestations[i + 1] - (grouplist[grouplistcount + 1][rr] - basestations[i + 1]) <= grouplist[grouplistcount][r]:
					confgraph[users.index(grouplist[grouplistcount + 1][rr])][users.index(grouplist[grouplistcount][r])] = 1
					confgraph[users.index(grouplist[grouplistcount][r])][users.index(grouplist[grouplistcount + 1][rr])] = 1
		#case 6
		for l in range(len(grouplist[grouplistcount])):
			for ll in range(len(grouplist[grouplistcount - 1])):
				if basestations[i+1] - (basestations[i + 1] - grouplist[grouplistcount][l]) <= basestations[i] + (basestations[i] - grouplist[grouplistcount - 1][ll]):
					confgraph[numofusers + users.index(grouplist[grouplistcount][l])][numofusers + users.index(grouplist[grouplistcount - 1][ll])] = 1 
					confgraph[numofusers + users.index(grouplist[grouplistcount - 1][ll])][numofusers + users.index(grouplist[grouplistcount][l])] = 1
		#case 7
		for l in range(len(grouplist[grouplistcount])):
			for r in range(len(grouplist[grouplistcount])):
				if grouplist[grouplistcount][r] <= grouplist[grouplistcount][l]:
					confgraph[users.index(grouplist[grouplistcount][l])][numofusers + users.index(grouplist[grouplistcount][r])] = 1
					confgraph[numofusers + users.index(grouplist[grouplistcount][r])][users.index(grouplist[grouplistcount][l])] = 1
		
		grouplistcount += 1

def PostProcess(grouplist, matrix, users, basestations, confgraph):
	firstcount = 0
	secondcount = 0
	for i in range(len(grouplist[0])):
		for j in range(len(confgraph[users.index(grouplist[0][i])])):
			confgraph[users.index(grouplist[0][i])][j] = 0
		firstcount += 1
	for i in range(len(grouplist[len(grouplist) - 1])):
		for j in range(len(confgraph[numofusers + users.index(grouplist[len(grouplist) - 1][i])])):
			confgraph[numofusers + users.index(grouplist[len(grouplist) - 1][i])][j] = 0
		secondcount += 1
	
	for i in range(1, len(confgraph) - 1):
		for j in range(firstcount):
			confgraph[i][j] = 0
		for j in range(secondcount):
			confgraph[i][len(confgraph[i]) - 1 - j] = 0
	
def printList(confgraph, users):
	endvariables = []
	opfile = open('stage1.csv', 'w')
	for i in range(len(confgraph)):
		temparray = []
		for j in range(len(confgraph[i])):
			if confgraph[i][j] == 1:
				temparray.append(j + 1)
		if not temparray:
			endvariables.append(i + 1)
		for k in range(len(temparray)):
			if k == len(temparray) - 1:
				opfile.write('%d' % temparray[k])
			else:
				opfile.write('%d,' % temparray[k])
		opfile.write("\n")
	opfile = open('endvars.csv', 'w')
	for i in range(len(endvariables)):
		if i == len(endvariables) - 1:
			opfile.write('%d' % endvariables[i])
		else:
			opfile.write('%d,' % endvariables[i])
		
if __name__ == '__main__':
	grouplist = []
	matrix = []
	users = []
	basestations = []
	
	inputData(grouplist, matrix, users, basestations)
	confgraph = [] #Uses a i - left arrows, numofusers + i - right arrows, type of indexing
	createConflictGraph(confgraph)
	
	GenericCaseConflict(grouplist, matrix, users, basestations, confgraph)
	PostProcess(grouplist, matrix, users, basestations, confgraph)
	printList(confgraph, users)