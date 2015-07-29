import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import scipy

# poisson function, parameter lamb is the fit parameter
def poisson(k, lamb):
    return (lamb**k/scipy.misc.factorial(k)) * np.exp(-lamb)

lamb = 10 # mean
s = np.random.poisson(lamb, 1000) # 1000 random number following poisson distribution

plt.xlabel('Time')
plt.ylabel('Probability')
plt.title('Probability Distribution of Time (lamb=%d)'%lamb)

count, bins, ignored = plt.hist(s, 24, range=[0,24], normed=True)
plt.grid(True)
plt.plot(bins, poisson(bins, lamb), linewidth=2, color='r')

pp = PdfPages('output/time.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()

#============ Action probability distribution	
lamb = 1 # mean
s = np.random.poisson(lamb, 1000) # 1000 random number following poisson distribution

plt.clf()
plt.xlabel('Action')
plt.ylabel('Probability')
plt.title('Probability Distribution of Action (lamb=%d)'%lamb)

count, bins, ignored = plt.hist(s, 5, range=[0,5], normed=True)
plt.grid(True)
plt.plot(bins, poisson(bins, lamb), linewidth=2, color='r')

pp = PdfPages('output/action.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()

#============ Location probability distribution	
lamb = 7 # mean
s = np.random.poisson(lamb, 1000) # 1000 random number following poisson distribution

plt.clf()
plt.xlabel('Location')
plt.ylabel('Probability')
plt.title('Probability Distribution of Location (lamb=%d)'%lamb)

count, bins, ignored = plt.hist(s, 15, range=[0,15], normed=True)
plt.grid(True)
plt.plot(bins, poisson(bins, lamb), linewidth=2, color='r')

pp = PdfPages('output/location.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()
