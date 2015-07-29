import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from attribute import Attribute
import random

# normal function, parameter mu and sigma is the fit parameter
def normal(k, mu, sigma):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (k - mu)**2 / (2 * sigma**2) )
	
attribute = Attribute()
attribute.load_dist_json()

for key, value in attribute.distribution.iteritems(): 
	name = key
	type = value["type"]
	domain = int(value["domain"])
	
	# only draw normal distribution
	if (type != "normal" and type != "random"):
		continue;
		
	mu = int(value["mu"])
	sigma = int(value["sigma"])
	#s = np.random.normal(mu, sigma, 1000) # 1000 random number following normal distribution
	
	s = []
	eventfile = "output/events.txt"
	with open(eventfile, 'rb') as file:
		for line in file.readlines():
			attrs = line.split(' ')
			for i in range(3, len(attrs)):
				if (attrs[i].startswith(value['represent'])):
					s.append(int(attrs[i].split('-')[1]))
	file.close()
	
	plt.clf()
	plt.xlabel(name)
	plt.ylabel('probability')
	plt.title('Probability distribution of %s (mu=%d,sigma=%d)'%(name, mu, sigma))
	
	plt.grid(True)
	count, bins, ignored = plt.hist(s, domain, range=[0,domain], normed=True, color='g')
	if (type != "random"):
		plt.plot(bins, normal(bins, mu, sigma), linewidth=2, color='r')

	pp = PdfPages('evaluate/%s.pdf' % (name))
	plt.savefig(pp, format='pdf')
	pp.savefig()
	pp.close()

