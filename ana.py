import numpy as np
import matplotlib.pyplot as plt

def find_in(array, target):
	for i in range(len(array)):
		if (target-array[i])<=0:
			return i
L=4
x_array = np.load('x_array.npy')

t_end = 3600			#s
nt = 100000
t_array = np.linspace(0, t_end, nt)

t_1 = 4 * 60
t_2 = 60 * 60

ti_1 = find_in(t_array, t_1)
ti_2 = find_in(t_array, t_2)

xi_1 = find_in(x_array, 0.9)
xi_2 = find_in(x_array, 1.3)

c1 = np.load('4.0min_sample.npy')
c2 = np.load('60.0min_sample.npy')

plt.close()
plt.plot(x_array*10000, c1, label = 't = {} min'.format(t_1/60))
plt.plot(x_array*10000, c2, label = 't = {} min'.format(t_2/60))
plt.plot([10000, 10000], [0, 1], label = 'interface')
plt.grid()
plt.legend()
plt.xlabel('distance in um')
plt.ylabel('Normalized Concentration')
plt.xlim([10000-1000, 10000+3000])
plt.show()

plt.close()
plt.plot(x_array, np.zeros_like(x_array)+1, 'rx')
plt.xlabel('x in cm')
plt.show()