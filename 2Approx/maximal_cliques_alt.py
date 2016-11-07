# Finds all maximal cliques in a graph using the Bron-Kerbosch algorithm. The input graph here is 
# in the adjacency list format, a dict with vertexes as keys and lists of their neighbors as values.
# https://en.wikipedia.org/wiki/Bron-Kerbosch_algorithm

from collections import defaultdict
import csv

def find_cliques(graph):
  p = set(graph.keys())
  r = set()
  x = set()
  cliques = []
  for v in degeneracy_ordering(graph):
    neighs = graph[v]
    find_cliques_pivot(graph, r.union([v]), p.intersection(neighs), x.intersection(neighs), cliques)
    p.remove(v)
    x.add(v)
	
  #print cliques
  maxsize = 0
  opfile = open('stage2.csv', 'w')
  for i in cliques:
	templist = list(i)
	if len(templist) > maxsize:
		maxsize = len(templist)
	for j in range(len(templist)):
		if j == len(templist) - 1:
			opfile.write('%d\n' % templist[j])
		else:
			opfile.write('%d,' % templist[j])
  print maxsize
  #return sorted(cliques, lambda x: len(x))

def find_cliques_pivot(graph, r, p, x, cliques):
  if len(p) == 0 and len(x) == 0:
    cliques.append(r)
  else:
    u = iter(p.union(x)).next()
    for v in p.difference(graph[u]):
      neighs = graph[v]
      find_cliques_pivot(graph, r.union([v]), p.intersection(neighs), x.intersection(neighs), cliques)
      p.remove(v)
      x.add(v)

def degeneracy_ordering(graph):
  ordering = []
  ordering_set = set()
  degrees = defaultdict(lambda : 0)
  degen = defaultdict(list)
  max_deg = -1
  for v in graph:
    deg = len(graph[v])
    degen[deg].append(v)
    degrees[v] = deg
    if deg > max_deg:
      max_deg = deg

  while True:
    i = 0
    while i <= max_deg:
      if len(degen[i]) != 0:
        break
      i += 1
    else:
      break
    v = degen[i].pop()
    ordering.append(v)
    ordering_set.add(v)
    for w in graph[v]:
      if w not in ordering_set:
        deg = degrees[w]
        degen[deg].remove(w)
        if deg > 0:
          degrees[w] -= 1
          degen[deg - 1].append(w)

  ordering.reverse()
  return ordering
  
if __name__ == '__main__':
	graph = {}
	array = []
	with open('stage1.csv', 'rb') as f:
		reader = csv.reader(f)
		array = list(reader)
		
	#graph[0] = []
	for i in range(len(array)):
		graph[i+1] = map(int, array[i])
	#print graph
#	graph = {
#		0:[], # I want to start index from 1 instead of 0
#		1:[2, 3, ],
#		2:[1, 3, ],
#		3:[1, 2, 4, ],
#		4:[3, 5, 6, ],
#		5:[4, 6, ],
#		6:[4, 5, ],
#	}
	find_cliques(graph)