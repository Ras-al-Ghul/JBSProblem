import sys

def extract(bs, user):
	print(len(user))
	print(len(bs))
	u = ['u' + str(x) for x in user]
	b = ['b' + str(x) for x in bs]
	entities = u + b
	entities.sort(key=lambda x: int(x[1:]))
	for i in entities:
		print(i)
	print()
    
