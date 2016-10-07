import csv

numofusers = 0
numofbs = 0
users = []

def mapping(num):
	global numofusers, users
	return 'l' + str(users[num - 1]) if num <= numofusers else 'r' + str(users[num - numofusers - 1])

if __name__ == '__main__':
	ipfile = open('1DJBSInput.txt', 'r')
	numofusers = int(ipfile.readline()) #number of agents
	numofbs = int(ipfile.readline()) #number of base stations
	
	users = []
	for i in range(0, int(numofusers)+int(numofbs)):
		temp = ipfile.readline()
		newtemp = str(temp)
		tempchar = newtemp[0]
		if tempchar == 'u':
			tempchar = -1
			users.append(int(newtemp[1:].replace('\n', '')))
	
	endvars = []
	with open('endvars.csv', 'rb') as f:
		reader = csv.reader(f)
		endvars = list(reader)
	endvars = map(int, endvars[0])
	
	array = []
	with open('stage2.csv', 'rb') as f:
		reader = csv.reader(f)
		array = list(reader)
	
	opfile = open('constraintfile.lp', 'w')
	opfile.write('min: k;\n\n')
	for i in range(len(array)):
		array[i] = map(int, array[i])
		
		for j in range(len(array[i])):
			if j == len(array[i]) - 1:
				opfile.write('%s <= k;\n' % (mapping(array[i][j])))
			else:
				opfile.write('%s + ' % (mapping(array[i][j])))
	
	opfile.write('\n')
	for i in range(numofusers):
		opfile.write('%s + %s = 1;\n' % (mapping(i + 1), mapping(i + 1 + numofusers)))
		
	opfile.write('\n')
	for i in range(numofusers):
		opfile.write('%s >= 0;\n' % mapping(i + 1))
		opfile.write('%s <= 1;\n' % mapping(i + 1))
		opfile.write('%s >= 0;\n' % mapping(i + 1 + numofusers))
		opfile.write('%s <= 1;\n' % mapping(i + 1 + numofusers))
		
	opfile.write('\n')
	for i in endvars:
		opfile.write('%s = 0;\n' % mapping(i))
		