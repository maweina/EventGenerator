import numpy as np
import random
from attribute import Attribute
from pattern import Pattern
from sequencepat import Sequencepat
import random
import pdb

class Eventgen():
	attributes = {}
	patterns = {}
	sequences = {}
	
	# global parameter
	avg_event_per_day =10;
	avg_event_days = 30;
	
	def __init__(self, attr, pat, seq):
		self.attributes = attr
		self.patterns = pat
		self.sequences = seq
		
	def get_normal_int (self, mu, sigma, min, max):
		x = int(random.normalvariate(mu, sigma))
		if (x < min or x > max):
			x = mu
		return x
	
	# select an attribute value 
	# attribute probability distribution can be normal, guss, beta or gamma distribution
	def get_attribute_value (self, attr_name):
		# undefined attribute
		if (not self.attributes[attr_name]):
			return
		
		# randomly select an integer following defined distribution
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
		# event format is:
		# "sequence_id event_id num-attrs attr-1 attr-2 attr-3 ... attr-n"
		file=open('output/events.txt', 'w')
		pfile = open('output/pattern.txt', 'w')
		afile = open('output/actionEvents.txt', 'w')
		lfile = open('output/locationEvents.txt', 'w')
		tfile = open('output/timeEvents.txt', 'w')
		
		seq_id = 1
		pnum = 1
		for i in range(1, int(self.attributes["user"]["domain"]) + 1):
			# dict to store the patters have to be inserted into the events of a specific day
			# key is date, value is a list of patterns
			day_seq = {}
			
			# selected days having events
			selected_days = []
			
			# generate events for one user
			user = self.attributes["user"]["represent"] + str(i)
			
			# number of days of this user has access request
			# num_days must be inside the domain of attribute "date"
			#num_days = self.get_normal_int(self.avg_event_days, 1.0, 1, int(self.attributes["date"]["domain"]))
			num_days = self.avg_event_days

			# select days
			#for j in range(num_days):
			#	selected_days.append(self.get_attribute_value("date"))			
			#selected_days = sorted(list(set(selected_days)))
			#num_days = len(selected_days)
			
			#selected_days = []
			#while len(selected_days) < num_days:
				#selected = random.randrange(1, int(self.attributes["date"]["domain"]))
				#if selected not in selected_days:
					#selected_days.append(selected)
			#selected_days = sorted(list(set(selected_days)))
			
			selected_days = []
			for j in range(num_days):
				selected_days.append(j+1)
			
			# if this user is selected to insert pattern
			# select %SUPPORT of days from "selected_days" to insert pattern
			if (user in self.sequences):
				# multiple patterns may be inserted
				for key, value in self.sequences[user].items():
					#support = self.patterns[key]["support"]
					#num_day_seq = int(float(support)*float(num_days))+1
					#selected_seq_days = []
					#pdb.set_trace()
					#while len(selected_seq_days) < num_day_seq:
					#	temp = random.choice(selected_days)
					#	if (temp not in selected_seq_days):
					#		selected_seq_days.append(temp)
					#selected_seq_days = sorted(selected_seq_days)
					#for dd in selected_seq_days:
					#	if (dd not in day_seq):
					#		day_seq[dd] = []
					#	if (value not in day_seq[dd]):
					#		day_seq[dd].append(value)
					for dd in selected_days:
						if (dd not in day_seq):
							day_seq[dd] = []
						if (value not in day_seq[dd]):
							day_seq[dd].append(value)
			
			#pdb.set_trace()
			# generated event day by day
			#pdb.set_trace()
			for date in selected_days:
				events = []
				selected_hours = []
				seq_event_index = []
				num_seq_events = 0
				
				# number of events of this user this day
				#num_events = self.get_normal_int(self.avg_event_per_day, 1.0, 1, 1000)
				num_events = self.avg_event_per_day
				
				# expand num_events if the accumulated assigned sequence length is greater
				# than num_events
				if (date in day_seq):
					for seq_event in day_seq[date]:
						#pdb.set_trace()
						num_seq_events += len(seq_event)
					if num_seq_events > num_events:
						num_events = num_seq_events + 3
				#print ("%s:%s" % (num_seq_events, num_events))
				
				# select hours of events per day
				for d in range(num_events):
					selected_hours.append(self.get_attribute_value("time"))
				selected_hours = sorted(selected_hours)
						
				# add user, day, hour to events
				day = self.attributes["date"]["represent"] + str(date)
				for k in range(len(selected_hours)):
					hour = self.attributes["time"]["represent"] + str(selected_hours[k])
					events.append([user, day, hour])
				
				# select events to insert pattern
				if (date in day_seq):
					for d in range(num_seq_events):
						while 1:
							my_hour = random.choice(selected_hours)
							my_hour_index = selected_hours.index(my_hour)
							# handle duplicated hours
							dup_index = -1
							for index in seq_event_index:
								if (my_hour_index == index):
									dup_index = index
							if dup_index != -1:
								try:
									my_hour_index = selected_hours.index(my_hour, dup_index + 1)
								except ValueError:
									continue;
							seq_event_index.append(my_hour_index)
							seq_event_index = sorted(list(set(seq_event_index)))
							break
					#pdb.set_trace()
					d = 0
					for seqs in day_seq[date]:
						for seq_event in seqs:
							for item in seq_event:
								if item.startswith("T-"):
									events[seq_event_index[d]].pop()
								events[seq_event_index[d]].append(item)
							#record pattern
							pfile.write("U-"+str(i)+ " "+str(day)+" T-"+str(selected_hours[seq_event_index[d]])+" " + str(seq_event) + "\n")
							d = d + 1
							if (d > len(seq_event_index)-1):
								break
						pfile.write("=====P" + str(pnum) + "=======\n")
						pnum = pnum + 1
						if (d > len(seq_event_index)-1):
							break

				
				# add left attribute values of event
				for d in range(num_events):
					for name in self.attributes.keys():
						attr = self.attributes[name]
						found = False
						for item in events[d]:
							if (item.startswith(attr["represent"])):
								found = True
								break
						if (not found):
							events[d].append(str(attr["represent"]) + str(self.get_attribute_value(name)))

				# sort attribute in events
				#events = sorted(events)
				
				# fix "T-8 is greater than T-12 in default sorted function
				#pdb.set_trace()
				#for k in range(len(events)):
				#	for l in range(k+1, len(events)):
				#		if (int(events[k][2].split('-')[1]) > int(events[l][2].split('-')[1])):
				#			temp = events[k]
				#			events[k] = events[l]
				#			events[l] = temp
				
				s = 1
				for event in events:
					#line = " ".join(str(x) for x in event) + "\n"
					line = ""
					for item in event:
						if item.startswith("L-") or item.startswith("A-") or item.startswith("T-"):
							line = line + str(item) + " "
							
					line = line + "\n"
					file.write(line)
					s = s+1
					
					for item in event:
						if item.startswith("L-"):
							lfile.write(str(item) + " ")
						elif item.startswith("A-"):
							afile.write(str(item) + " ")
						elif item.startswith("T-"):
							tfile.write(str(item) + " ")
							
				lfile.write("\n")
				afile.write("\n")
				tfile.write("\n")
					
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
	