itemset=['A-11', 'L-11']
eventfile = "output/events.txt"
support = 0
linecount = 0
with open(eventfile, 'rb') as file:
	for line in file.readlines():
		linecount = linecount + 1
		find = 0
		attributes = line.split(' ')
		for item in itemset:
			for i in range(len(attributes)):
				if (item == attributes[i]):
					find = find +1
					break
		if (find == len(itemset)):
			print line
			support = support + 1
file.close()
relative = float(support)/linecount
print support
print linecount
print relative