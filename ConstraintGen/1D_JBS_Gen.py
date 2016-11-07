import random, time
start_t = time.clock()	#To calculate the time taken for generating the constraints

ipfile = open('1DJBSInput.txt', 'r')
numofusers = ipfile.readline() #number of agents
numofbs = ipfile.readline() #number of base stations

# -1 is a user while -2 is a base station
grouplist = []
tempgrouplist = []
matrix = []
users = []
basestations = []
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
	
print(matrix)
print(grouplist)
		
f = open('1DJBS.xml', 'w')
f.write('<instance>\n')

#Description
f.write('\t<presentation name="JBSProblem" maxConstraintArity="4" maximize="false" format="XCSP 2.1_FRODO" />\n\n')

#Agents
f.write('\t<agents nbAgents="%d">\n' % int(numofusers))
for i in range(0, int(numofusers)):
	f.write('\t\t<agent name=\"agent%d\" />\n' % users[i])
f.write('\t</agents>\n\n')

#Domains - restricted so that only adjacent base stations are included
f.write('\t<domains nbDomains=\"%d\">\n' %(int(numofusers) + 1))
basestationptr = 0
for i in users:
	while basestationptr < int(numofbs) and i > basestations[basestationptr]:
		basestationptr += 1	
	if basestationptr != 0:
		if basestationptr < int(numofbs):
			f.write('\t\t<domain name=\"basestation%d\" nbValues=\"%d\">' % (i, 2))
			f.write(str(basestations[basestationptr - 1]))
			f.write(' ')
			f.write(str(basestations[basestationptr]))
			f.write('</domain>\n')
		else:
			f.write('\t\t<domain name=\"basestation%d\" nbValues=\"%d\">' % (i, 1))
			f.write(str(basestations[basestationptr - 1]))
			f.write('</domain>\n')
	else:
		f.write('\t\t<domain name=\"basestation%d\" nbValues=\"%d\">' % (i, 1))
		f.write(str(basestations[basestationptr]))
		f.write('</domain>\n')
k = int(int(numofusers)/int(numofbs))*6
k -= 1
f.write('\t\t<domain name=\"rounds\" nbValues=\"%d\">' % k )
numofrounds = k
k += 1
for i in range(1,k):
	f.write(str(i))
	if i != k-1:
		f.write(' ')
f.write('</domain>\n')
f.write('\t</domains>\n\n')

#Variables
f.write('\t<variables nbVariables=\"%d\">\n' % (int(numofusers)*2))
for i in range(0, int(numofusers)):
	f.write('\t\t<variable name=\"agent%dbs\" domain=\"basestation%d\" agent=\"agent%d\" />\n' % (int(users[i]), int(users[i]), int(users[i])))
	f.write('\t\t<variable name=\"agent%dr\" domain=\"rounds\" agent=\"agent%d\" />\n' % (int(users[i]), int(users[i])))
f.write('\t</variables>\n\n')	

#Relations - This is the cost relation part
f.write('\t<relations nbRelations=\"%d\">\n' % 1)
f.write('\t\t<relation name=\"COST\" arity=\"1\" nbTuples=\"%d\" semantics=\"soft\" defaultCost=\"infinity\">\n' % (numofrounds))
f.write('\t\t\t')
for i in range(1, numofrounds+1):
	if i == numofrounds:
		f.write('%d: %d' % (i, i))
		continue
	f.write('%d: %d | ' % (i, i))
f.write('\n')
f.write('\t\t</relation>\n')
f.write('\t</relations>\n\n')

#Predicates - The same timeslot, no same base station and collision predicates
f.write('\t<predicates nbPredicates=\"2\">\n')
#
f.write('\t\t<predicate name=\"NEQ\">\n')
f.write('\t\t\t<parameters> int X1 int X2 int Y1 int Y2 </parameters>\n')
f.write('\t\t\t<expression>\n')
f.write('\t\t\t\t<functional> or( ne(Y1, Y2), ne(X1, X2) ) </functional>\n')
f.write('\t\t\t</expression>\n')
f.write('\t\t</predicate>\n')
#
f.write('\t\t<predicate name=\"ISCOLLIDE\">\n')
f.write('\t\t\t<parameters> int X1 int X2 int Y1 int Y2 int Z1 int Z2 </parameters>\n')
f.write('\t\t\t<expression>\n')
f.write('\t\t\t\t<functional> or( ne(X1, X2), or( ne(Y1, Z1), ne(Y2, Z2) ) ) </functional>\n')
f.write('\t\t\t</expression>\n')
f.write('\t\t</predicate>\n')
#
f.write('\t</predicates>\n\n')

#Constraints
overallcount = 0
f.write('\t<constraints nbConstraints=\"%d\">\n' % overallcount)
# Simple cost constraints, one for each 'round' variable
f.write('\t\t<!-- Cost of each round assignment -->\n')	
for i in range(0, int(numofusers)):
	f.write('\t\t<constraint name=\"agent%d_cost\" arity=\"1\" scope=\"agent%dr\" reference=\"COST\" />\n' % (int(users[i]),int(users[i])))
	overallcount += 1
# Simply check for all agents which could possibly have the same base station assigned to them and form constraints based on them
f.write('\t\t<!-- If same round, then can\'t have same BS -->\n')
bscount = 0
for i in range(0, len(grouplist)):
	if grouplist[i][0] > basestations[bscount]:
		bscount += 1
	#In same grouplist
	for outer in range(0, len(grouplist[i])):
		for inner in range(outer+1, len(grouplist[i])):
			f.write('\t\t<constraint name=\"agent%d_and_agent%d_have_different_bs_if_in_same_round\" arity=\"4\" scope=\"agent%dbs agent%dbs agent%dr agent%dr\" reference=\"NEQ\" >\n' % (grouplist[i][outer], grouplist[i][inner], grouplist[i][outer], grouplist[i][inner], grouplist[i][outer], grouplist[i][inner]))
			f.write('\t\t\t<parameters> agent%dbs agent%dbs agent%dr agent%dr </parameters>\n' % (grouplist[i][outer], grouplist[i][inner], grouplist[i][outer], grouplist[i][inner]))
			f.write('\t\t</constraint>\n')
			overallcount += 1
			#Part of next case
			if bscount != 0 and bscount != len(basestations):
				f.write('\t\t<!-- The following constraint is part of IsCollide -->\n')
				f.write('\t\t<constraint name=\"agent%d_and_agent%d_don\'t_collide\" arity=\"4\" scope=\"agent%dr agent%dr agent%dbs agent%dbs\" reference=\"ISCOLLIDE\" >\n' % (grouplist[i][outer],grouplist[i][inner],grouplist[i][outer],grouplist[i][inner],grouplist[i][outer],grouplist[i][inner]))
				f.write('\t\t\t<parameters> agent%dr agent%dr agent%dbs agent%dbs %d %d </parameters>  \n' % (grouplist[i][outer],grouplist[i][inner],grouplist[i][outer],grouplist[i][inner],basestations[bscount],basestations[bscount - 1]))
				f.write('\t\t</constraint>\n')
				overallcount += 1
	#Same group and next group
	for outer in range(0, len(grouplist[i])):
		if i+1 < len(grouplist):
			for inner in range(0, len(grouplist[i+1])):
				f.write('\t\t<constraint name=\"agent%d_and_agent%d_have_different_bs_if_in_same_round\" arity=\"4\" scope=\"agent%dbs agent%dbs agent%dr agent%dr\" reference=\"NEQ\" >\n' % (grouplist[i][outer], grouplist[i+1][inner], grouplist[i][outer], grouplist[i+1][inner], grouplist[i][outer], grouplist[i+1][inner]))
				f.write('\t\t\t<parameters> agent%dbs agent%dbs agent%dr agent%dr </parameters>\n' % (grouplist[i][outer], grouplist[i+1][inner], grouplist[i][outer], grouplist[i+1][inner]))
				f.write('\t\t</constraint>\n')
				overallcount += 1
# Detect amongst which agents collision is possible - split into initial part, the middle main part - which is further split into two cases, the last part
f.write('\t\t<!-- IsCollide -->\n')
grouplistcount = 1
basestationleft = 0
if grouplist[0][0] > basestations[0]:
	left = basestations[0]
	right = basestations[1]
	for i in grouplist[0]:
		for j in grouplist[1]:
			distm = right - i
			distr = j - right
			if distr >=  distm:
				f.write('\t\t<constraint name=\"agent%d_and_agent%d_don\'t_collide_%d%d\" arity=\"4\" scope=\"agent%dr agent%dr agent%dbs agent%dbs\" reference=\"ISCOLLIDE\" >\n' % (i,j,random.randrange(1,99),random.randrange(1,99),i,j,i,j))
				f.write('\t\t\t<parameters> agent%dr agent%dr agent%dbs agent%dbs %d %d </parameters>  \n' % (i,j,i,j,left,right))
				f.write('\t\t</constraint>\n')
				overallcount += 1
	basestationleft = 1
#
while grouplistcount != len(grouplist) - 1:
	for i in grouplist[grouplistcount]:
		#First case
		left = basestations[basestationleft]
		right = basestations[basestationleft + 1]
		for j in grouplist[grouplistcount - 1]:
			distm = i - left
			distl = left - j
			if distl >= distm: 
				f.write('\t\t<constraint name=\"agent%d_and_agent%d_don\'t_collide_%d%d\" arity=\"4\" scope=\"agent%dr agent%dr agent%dbs agent%dbs\" reference=\"ISCOLLIDE\" >\n' % (j,i,int(random.randrange(1,99)),int(random.randrange(1,99)),j,i,j,i))
				f.write('\t\t\t<parameters> agent%dr agent%dr agent%dbs agent%dbs %d %d </parameters>  \n' % (j,i,j,i,left,right))
				f.write('\t\t</constraint>\n')
				overallcount += 1
		#Second case
		left = basestations[basestationleft]
		right = basestations[basestationleft + 1]
		for k in grouplist[grouplistcount + 1]:
			distm = right - i
			distr = k - right
			if distr >= distm:
				f.write('\t\t<constraint name=\"agent%d_and_agent%d_don\'t_collide_%d%d\" arity=\"4\" scope=\"agent%dr agent%dr agent%dbs agent%dbs\" reference=\"ISCOLLIDE\" >\n' % (i,k,random.randrange(1,99),random.randrange(1,99),i,k,i,k))
				f.write('\t\t\t<parameters> agent%dr agent%dr agent%dbs agent%dbs %d %d </parameters>  \n' % (i,k,i,k,left,right))
				f.write('\t\t</constraint>\n')
				overallcount += 1
	basestationleft += 1
	grouplistcount += 1
#
if grouplist[len(grouplist) - 1][0] < basestations[len(basestations) - 1]:
	left = basestations[len(basestations) - 2]
	right = basestations[len(basestations) - 1]
	for i in grouplist[len(grouplist) - 1]:
		for j in grouplist[len(grouplist) - 2]:
			distm = i - left
			distl = left - j
			if distl >=  distm:
				f.write('\t\t<constraint name=\"agent%d_and_agent%d_don\'t_collide_%d%d\" arity=\"4\" scope=\"agent%dr agent%dr agent%dbs agent%dbs\" reference=\"ISCOLLIDE\" >\n' % (j,i,random.randrange(1,99),random.randrange(1,99),j,i,j,i))
				f.write('\t\t\t<parameters> agent%dr agent%dr agent%dbs agent%dbs %d %d </parameters>  \n' % (j,i,j,i,left,right))
				f.write('\t\t</constraint>\n')
				overallcount += 1
#
print('Enter this number manually as nbConstraints %d' % overallcount)
f.write('\t</constraints>\n\n')

f.write('</instance>\n')

print('%s seconds' % (time.clock() - start_t))