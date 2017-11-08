
import scipy as sp
import matplotlib.pyplot as plt

def error(f, x, y):
    return sp.sum((f(x)-y)**2)

data = sp.genfromtxt("webtraffic.tsv", delimiter="\t")

# print(data[:10])
# print(data.shape)

x = data[:,0]
y = data[:,1]

x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

# # Dibuja un bonito grafico
# plt.scatter(x,y)
# plt.title("Web traffic over the last month")
# plt.xlabel("Time")
# plt.ylabel("Hits/hour")
# plt.xticks([w*7*24 for w in range(10)],
# ['week %i'%w for w in range(10)])
# plt.autoscale(tight=True)
# plt.grid()
# plt.show()

fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)

print("Model parameters: %s" % fp1)
print(residuals)

f1 = sp.poly1d(fp1)
print(error(f1, x, y))
