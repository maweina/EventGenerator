import numpy as np
import random
from attribute import Attribute
from pattern import Pattern
from sequencepat import Sequencepat
import random
import pdb
from copy import deepcopy

class Eventgen():
	attributes = {}
	patterns = {}
	sequences = {}
	
	# global parameter
	num_events_per_day =10;
	num_days_per_user = 10;
	
	def __init__(self, attr, pat, seq):
		self.attributes = attr
		self.patterns = pat
		self.sequences = seq
		
	# select an attribute value 
	# attribute probability distribution can be normal, guss, beta or gamma distribution
	def get_attribute_value (self, attr_name):
		# undefined attribute
		if (not self.attributes[attr_name]):
			return
		
		# randomly select an integer following defined distribution
		x = 0
		if (self.attributes[attr_name]["type"] == "normal"):	
			x = int(random.normalvariate(float(self.attributes[attr_name]["mu"]), float(self.attributes[attr_name]["sigma"])))
		elif (self.attributes[attr_name]["type"] == "guss"):
			x = int(random.gauss(float(self.attributes[attr_name]["mu"]), float(self.attributes[attr_name]["sigma"])))
		
		# set attribute value as mean if it is out of scope
		if (x < 1 or x > int(self.attributes[attr_name]["domain"])):
			x = int(self.attributes[attr_name]["mu"])
		return x	
		
	# generate event dataset
	def gen(self):
		# event format: "sequence_id event_id num-attrs attr-1 attr-2 attr-3 ... attr-n"
		# pattern.txt records the embedded patterns
		file=open('output/events.txt', 'w')
		pfile = open('output/pattern.txt', 'w')
		
		seq_id = 1
		pnum = 1
		# generate events user by user
		for i in range(1, int(self.attributes["user"]["domain"]) + 1):
			user = self.attributes["user"]["represent"] + str(i)
			
			num_days = self.num_days_per_user
			
			# dict to store the patters have to be inserted into a specific day and hour
			# day_seq format: {day: [sequence, sequence, ...]}
			day_seq = {}
			
			
			# pdb.set_trace()
			# if this user is selected to insert pattern
			# select %SUPPORT of days to insert pattern
			if (user in self.sequences):
				# multiple patterns may be inserted
				for key, value in self.sequences[user].items():
					support = self.patterns[key]["userSupport"]
					num_day_seq = int(float(support)*float(num_days))+1
					duration = int(self.patterns[key]["duration"])
					gap = self.patterns[key]["gap"]
					selected_seq_days = []
					while len(selected_seq_days) < num_day_seq:
						temp = random.randint(1, num_days)
						if (temp not in selected_seq_days):
							selected_seq_days.append(temp)
					selected_seq_days = sorted(selected_seq_days)
					
					# selected_seq_days is a list of days to insert pattern
					for dd in selected_seq_days:
						tmp_seq = deepcopy(value)
							
						if (dd not in day_seq):
							day_seq[dd] = []
						if (tmp_seq not in day_seq[dd]):
							selectHours = 1
							# not select hours if sequence pattern already has time attribute
							for item in tmp_seq[0]:
								if item.startswith("T-"):
									selectHours = 0
									break
							# select hours for events of sequence
							if selectHours == 1:
								# start time of the sequence pattern
								start = int(self.get_attribute_value("time"))
								if duration != -1:
									end = start + duration
								else:
									end = 24
								if end > 24:
									start = 24 - duration
									end = 24
								tmp_seq[0].insert(0, "T-" + str(start))
								last_timestamp = start
								for index, subseq in enumerate(tmp_seq[1:]):
									if int(gap[index]) != -1:
										timestamp = random.randint(last_timestamp, last_timestamp+int(gap[index]))
									else:
										timestamp = random.randint(last_timestamp, end)
									tmp_seq[index+1].insert(0, "T-" + str(timestamp))
									last_timestamp = timestamp
							day_seq[dd].append(tmp_seq)
			
			# generated event day by day
			for date in range(1, num_days + 1):
				events = []
				num_seq_events = 0
				# number of events of this user this day
				num_events = self.num_events_per_day
				
				# expand num_events if the accumulated assigned sequence length is greater
				# than num_events
				if (date in day_seq):
					for seq_event in day_seq[date]:
						num_seq_events += len(seq_event)
					if num_seq_events > num_events:
						num_events = num_seq_events
				
				# add user, day, hour to non-pattern events
				day = self.attributes["date"]["represent"] + str(date)
				for k in range(num_events - num_seq_events):
					time = self.attributes["time"]["represent"] + str(self.get_attribute_value("time"))
					events.append([user, day, time])
				
				if (date in day_seq):
					for seq in day_seq[date]:
						#record pattern
						pfile.write("=====P" + str(pnum) + "=======\n")
						for seq_event in seq:
							seq_event.insert(0, self.attributes["date"]["represent"] + str(date))
							seq_event.insert(0, user)
							pfile.write(str(seq_event))
							#pdb.set_trace()
							pfile.write("\n")
						pnum = pnum + 1
						events.extend(seq)

				# add left attribute values of event
				for event in events:
					for name in self.attributes.keys():
						attr = self.attributes[name]
						found = False
						for item in event:
							if (item.startswith(attr["represent"])):
								found = True
								break
						if (not found):
							event.append(str(attr["represent"]) + str(self.get_attribute_value(name)))
				
				# output ordered attribute for each event
				ordered_events = {}
				for event in events:
					tmp = []
					orderbytime = None
					for item in event:
						if item.startswith("U-"):
							tmp.append(item)
							break
					for item in event:
						if item.startswith("D-"):
							tmp.append(item)
							break
					for item in event:
						if item.startswith("T-"):
							tmp.append(item)
							orderbytime = int(item[2:])
							break
					for item in event:
						if item.startswith("R-"):
							tmp.append(item)
							break
					for item in event:
						if item.startswith("L-"):
							tmp.append(item)
							break
					for item in event:
						if item.startswith("A-"):
							tmp.append(item)
							break
					for item in event:
						if item.startswith("P-"):
							tmp.append(item)
							break
					if orderbytime not in ordered_events:
						ordered_events[orderbytime] = []
					ordered_events[orderbytime].append(tmp)
					
				s = 1
				for key, value in ordered_events.items():
					for event in value:
						line = str(seq_id) + " " + str(s) + " " + str(len(self.attributes)) + " " + " ".join(str(x) for x in event) + "\n"
						file.write(line)
						s = s+1
				seq_id = seq_id + 1
				
		file.close()
		pfile.close()

if __name__ == '__main__':
	attribute = Attribute()
	attribute.load_dist_json()
	attribute.load_attr_cvs()
	
	pattern = Pattern(attribute.sem_to_rep)
	pattern.load()
	
	expanded_seq = Sequencepat(attribute.distribution, pattern.patterns)
	expanded_seq.expand()
	
	event_gen = Eventgen(attribute.distribution, pattern.patterns, expanded_seq.exp_sequences)
	event_gen.gen()
	