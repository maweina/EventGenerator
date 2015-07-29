import pdb

sequence=['L-1', 'L-3', 'L-4']
eventfile = "output/events.txt"
support = 0
seq_count = 1
seq_id = 1
sequences = []
with open(eventfile, 'rb') as file:
	for line in file.readlines():
		items = line.split(' ')
		#new sequence
		if (items[0] != seq_id):
			#pdb.set_trace()
			seq_id = items[0]
			seq_count = seq_count + 1
			num = 0
			flag = 0
			for event in sequences:
				attrs = event.split(' ')
				for item in attrs:
					if (item == 'L-1'):
						#print attrs
						flag = 1
						break
					num = num
				if (flag):
					flag = 0;
					break
			for j in range(num, len(sequences)):
				attrs = sequences[j].split(' ')
				for item in attrs:
					if (item == 'L-3'):
						#print attrs
						flag = 1
						break
					num = num + 1
				if (flag):
					#print attrs
					flag = 0;
					break
					
			for j in range(num, len(sequences)):
				attrs = sequences[j].split(' ')
				for item in attrs:
					if (item == 'L-4'):
						flag = 1
						break
					num = num + 1
				if (flag):
					print attrs
					break
			
			if (flag):
				support = support + 1
				
			sequences = []
			
		sequences.append(line)

file.close()
relative = float(support)/seq_count
print support
print seq_count
print relative