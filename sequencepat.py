import numpy as np
import random
from attribute import Attribute
from pattern import Pattern
import json

class Sequencepat():
	attributes = {}
	patterns = {}
	exp_sequences = {}
	
	def __init__(self, attr, pat):
		self.attributes = attr
		self.patterns = pat

	def expand(self):		
		for key,value in self.patterns.iteritems():
			expanded = []
			for seq_item in value["sequence"]:
				new_seq_item = seq_item
				for item in value["itemset"]:
					new_seq_item.append(item)
				expanded.append(new_seq_item)
			if (len(value["sequence"]) == 0):
				new_seq_item = []
				for item in value["itemset"]:
					new_seq_item.append(item)
				expanded.append(new_seq_item)
				
			selected_users = []
			num_users = 0
			if len(value["user"]) > 0:
				num_users = len(value["user"])
				selected_users = value["user"]
			else:
				num_users = float(self.attributes["user"]["domain"])*float(value["groupSupport"])
				while len(selected_users) < num_users:
					selected = random.randrange(1, int(self.attributes["user"]["domain"]))
					selected_user = self.attributes["user"]["represent"] + str(selected)
					if selected_user not in selected_users:
						selected_users.append(selected_user)
			
			for user in selected_users:
				if user not in self.exp_sequences:
					self.exp_sequences[user] = {}
				self.exp_sequences[user][key] = expanded

if __name__ == '__main__':
	attribute = Attribute()
	attribute.load_dist_json()
	attribute.load_attr_cvs()
	
	pattern = Pattern(attribute.sem_to_rep)
	pattern.load()
	
	expanded_seq = Sequencepat(attribute.distribution, pattern.patterns)
	expanded_seq.expand()
	#print expanded_seq.exp_sequences
	print json.dumps(expanded_seq.exp_sequences)

