import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# time = 4 min and 60min
#

class emulate():
	def __init__(self, D, label):
		self.label = label
		self.D = D 							#in cm^2/s
		self.L = 0.3							#in cm
		self.x_array = np.linspace(0, self.L, 100) #about distance
		self.t_array = np.array([4, 60])*60 #about time
		self.y_array = np.zeros((np.size(self.t_array), np.size(self.x_array))) #about normalized intensity
		self.intensity_coeff = 21000
        
	def calc(self):
		x_array = self.x_array
		y_array = self.y_array
		t_array = self.t_array
		D = self.D
		
		for i in range(len(t_array)):
			for j in range(len(x_array)):
				z = x_array[j]/(2*(D*t_array[i])**0.5)
				y_array[i,j] = sp.erfc(z)
		
		self.y_array = y_array

	def plotting(self):
		x_array = self.x_array*10000
		y_array = self.y_array*self.intensity_coeff
		t_array = self.t_array

		plt.close()
		for i in range(len(t_array)):
			plt.plot(x_array, y_array[i], label = 't = {} min'.format(t_array[i]/60))
		plt.grid()
		plt.xlabel('distance (um)')
		plt.ylabel('intensity')
		plt.title(self.label)
		plt.legend()
		plt.ylim([0,25000])
		plt.xlim([0,3000])
		plt.show()

if __name__ == '__main__':
	test = emulate(1.8*10**-6, 'Emulated by erfc')
	test.calc()
	test.plotting()