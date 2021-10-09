import numpy as np
from csv import reader
from csv import writer
import matplotlib.pyplot as plt 

ds = []
suscase = [] #S0
actcase = [] #S1	
remcase = [] #S2
p01_ar = []
p11_ar = []
p01 = 0
p11 = 0
pmat = np.zeros([3,3])
s = [1,0,0]
probs = []

with open ('mycsv.csv', 'r') as datafile:
	reader = reader(datafile, quotechar='"')
	for i in reader:
		ds.append(i)

noc = len(ds)
for i in range (0,noc):
	for j in range(0,len(ds[i])):
		ds[i][j] = int(ds[i][j])

ds = np.array(ds)

for i in range(noc):
	suscase.append(ds[i][4])
	actcase.append(ds[i][1])
	remcase.append(ds[i][2]+ds[i][3])

suscase = np.array(suscase) #S0
actcase = np.array(actcase) #S1
remcase = np.array(remcase) #S2

for i in range(noc-1):
	temp01_ar = (actcase[i+1] - actcase[i] + remcase[i+1] - remcase[i])/suscase[i]
	p01_ar.append(temp01_ar)
	temp11_ar = (actcase[i] - remcase[i+1] + remcase[i])/actcase[i]
	p11_ar.append(temp11_ar)

p01_ar = np.array(p01_ar)
p11_ar = np.array(p11_ar)

for i in range (noc-1):
	p01 += p01_ar[i]
	p11 += p11_ar[i]

p01 = p01/(noc-1)
p11 = p11/(noc-1)

# Probability Transition Matrix
pmat[0][1] = p01
pmat[1][1] = p11
pmat[0][0] = 1 - pmat[0][1]
pmat[2][2] = 1
pmat[1][2] = 1 - pmat[1][1] 

print("State transition probability matrix, P = ")
print(pmat)
days = []
pred_ac = []
pred_rc = []
tempa = s
for i in range(184):
	tempb = np.dot(tempa,pmat)
	pred_ac.append(suscase[i]*tempb[1])
	pred_rc.append(suscase[i]*tempb[2])
	tempa = tempb
	days.append(i)

plt.semilogy(days,pred_ac)
plt.semilogy(days,actcase)
plt.legend(["Predicted Active Cases", "Active Cases observed"], loc ="upper left") 
plt.xlabel("Number of days")
plt.ylabel("Number of active cases")
plt.show()

plt.semilogy(days,pred_rc)
plt.semilogy(days,remcase)
plt.legend(["Predicted Removed Cases", "Removed Cases observed"], loc ="upper left") 
plt.xlabel("Number of days")
plt.ylabel("Number of removed cases")
plt.show()