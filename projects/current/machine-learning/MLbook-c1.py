
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
inflection = 3.5*7*24 # calculate the inflection point in hours
xa = x[:int(inflection)] # data before the inflection point
ya = y[:int(inflection)]
xb = x[int(inflection):] # data after
yb = y[int(inflection):]

fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
f1 = sp.poly1d(fp1)
print('error f1: ',error(f1, x, y))
fx = sp.linspace(0,x[-1], 1000) # generate X-values for plotting
# f2p = sp.polyfit(x, y, 2)
# f2 = sp.poly1d(f2p)
# print('error f2: ',error(f2, x, y))
f4p = sp.polyfit(x, y, 4)
f4 = sp.poly1d(f4p)
print('error f4: ',error(f4, x, y))
fa = sp.poly1d(sp.polyfit(xa, ya, 1))
fb = sp.poly1d(sp.polyfit(xb, yb, 1))
fa_error = error(fa, xa, ya)
fb_error = error(fb, xb, yb)
print("Error inflection=%f" % (fa_error + fb_error))


# Dibuja un bonito grafico
plt.plot(fx, f1(fx), f4(x), linewidth=4)
plt.legend(["d=%i" % f1.order, "d=%u" % f4.order], loc="upper left")
plt.scatter(x,y)
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/hour")
plt.xticks([w*7*24 for w in range(10)],['week %i'%w for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
plt.show()
