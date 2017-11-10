
import scipy as sp
import matplotlib.pyplot as plt

def xp_levelup (level):
    xp = (level + 3.0) * 25.0
    return xp

x = sp.array( [i for i in range(81)] )
x = x[x>0]
y = xp_levelup(x)
z = sp.array( [sum(y[:(i+1)]) for i in range(80)] )

print(x)
print(y)
print(z)

# Dibuja un bonito grafico
plt.plot(x, z, linewidth=1)
plt.legend(["XP", "XPcum"], loc="upper left")
plt.scatter(x,z)
plt.title("XP evolution")
plt.xlabel("Levels")
plt.ylabel("Points XP")
plt.xticks(x)
plt.autoscale(tight=True)
plt.grid()
plt.show()
