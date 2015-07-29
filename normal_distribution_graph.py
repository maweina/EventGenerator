import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from attribute import Attribute

# normal function, parameter mu and sigma is the fit parameter
def normal(k, mu, sigma):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (k - mu)**2 / (2 * sigma**2) )
	
attribute = Attribute()
attribute.load_dist_json()

for key, value in attribute.distribution.iteritems(): 
	name = key
	type = value["type"]
	domain = int(value["domain"])
	
	# only draw normal and random distribution
	if (type != "normal" and type != "random"):
		continue;
		
	mu = int(value["mu"])
	sigma = int(value["sigma"])
	
	s = []
	if (type == "random"):
		for i in range(1000):
			s.append(np.random.randint(1, domain))
	else:
		s = np.random.normal(mu, sigma, 1000) # 1000 random number following normal distribution
		
	plt.clf()
	plt.xlabel(name)
	plt.ylabel('probability')
	plt.title('Probability distribution of %s (mu=%d,sigma=%d)'%(name, mu, sigma))
	
	plt.grid(True)
	count, bins, ignored = plt.hist(s, domain, range=[0,domain], normed=True)
	if (type != "random"):
		plt.plot(bins, normal(bins, mu, sigma), linewidth=2, color='r')

	pp = PdfPages('output/%s.pdf' % (name))
	plt.savefig(pp, format='pdf')
	pp.savefig()
	pp.close()

