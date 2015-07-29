import json
from pprint import pprint

# This class provides the utility to load attribute definitions 
# from cvs file named "${attrName}.cvs" and attribute probability distribution
# from json file "attrite_distribution.json".

class Attribute():
	# dictionary from attribute representation to semantic meaning
	# e.g., at pattern analysis step we want to know who is "U-23".
	rep_to_sem = {}
	
	# dictionary from attribute semantic meaning to representation
	# e.g., when paring behavior pattern definition, we need know
	# how to represent user "Tom".
	sem_to_rep = {}
	
	# record all attributes
	distribution = {}
	
	def __init__(self):
		pass
	
	def load_dist_json(self):
		# load attribute distribution file
		json_data=open('input/attribute_distribution.json')
		self.distribution = json.load(json_data)
		#pprint(attrs)
		json_data.close()
		
	def load_attr_cvs(self):
		for key in self.distribution.keys():
			file = "input/" + key + ".csv"
			with open(file, 'rb') as csvfile:
				for line in csvfile.readlines():
					item = line.rstrip('\r\n').split(',')
					self.rep_to_sem[item[1]] = item[0]
					self.sem_to_rep[item[0]] = item[1]
			csvfile.close()
		
if __name__ == '__main__':
	attribute = Attribute()
	attribute.load_dist_json()
	attribute.load_attr_cvs()
	print "============="
	print attribute.sem_to_rep
	print "============="
	print attribute.rep_to_sem
	print "============="
	print attribute.distribution
	