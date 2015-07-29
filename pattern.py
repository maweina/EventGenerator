import json
from pprint import pprint
from attribute import Attribute

# This class provides the utility to load behaviour pattern definitions 
# from json file "patterns.json".
#

class Pattern():
	patterns = {}
	dict_attr = {}
	
	def __init__(self, dict):
		self.dict_attr = dict
		
	def load(self):
		# load pattern definition file
		json_data=open('input/patterns.json')
		data = json.load(json_data)
		#pprint(data)
		json_data.close()
		
		for entity in data:
			if "actor" in entity:
				isRole = False
				users = []
				for item in entity["actor"]:
					for key, value in item.iteritems():
						if key == "user":
							users.append(value)
						elif key == "role":
							isRole = True
							self.insert_pattern(None, value, entity)
				if isRole == False:
					self.insert_pattern(users, None, entity)
			else:
				self.insert_pattern(None, None, entity)
		
	def insert_pattern(self, users, role, entity):
		actor = [];
		itemset = []
		sequence = []
		gap = []
		groupSupport = 0
		userSupport = 0
		duration = -1
		
		if users != None:
			for eachUser in users:
				actor.append(self.dict_attr[eachUser])
		if role != None:
			itemset.append(self.dict_attr[role])
					
		if "context" in entity:
			for key, value in entity["context"].iteritems():
				itemset.append(self.dict_attr[value])
					
		if "sequence" in entity:
			for item in entity["sequence"]:
				if "gap" in item:
					gap.append(item["gap"]);
				else:
					gap.append(-1);
						
				oneset = []
				for key, value in item.iteritems():
					if key != "gap":
						oneset.append(self.dict_attr[value])
				sequence.append(oneset)
				
		if "groupSupport" in entity:
			groupSupport = entity["groupSupport"]
				
		if "userSupport" in entity:
			userSupport = entity["userSupport"]
				
		if "duration" in entity:
			duration = entity["duration"]
		
		self.patterns[entity["id"]] = {}
		self.patterns[entity["id"]]["user"] = actor
		self.patterns[entity["id"]]["itemset"] = itemset
		self.patterns[entity["id"]]["sequence"] = sequence
		self.patterns[entity["id"]]["gap"] = gap
		self.patterns[entity["id"]]["groupSupport"] = groupSupport
		self.patterns[entity["id"]]["userSupport"] = userSupport
		self.patterns[entity["id"]]["duration"] = duration
	
if __name__ == '__main__':
	attribute = Attribute()
	attribute.load_dist_json()
	attribute.load_attr_cvs()
	
	pattern = Pattern(attribute.sem_to_rep)
	pattern.load()
	#print pattern.patterns
	print json.dumps(pattern.patterns)
	