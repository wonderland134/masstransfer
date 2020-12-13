import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Calculation_tool():
	def __init__(self):
		pass

	def interpolation(self, target, x_array, y_array):
		#interpolation tool, target value -> x, find y corresponding to target by y_array
		for i in range(len(x_array)-1):
			if (target-x_array[i+1])*(target-x_array[i])<=0:
				return (y_array[i+1]/y_array[i])*(target-x_array[i])+y_array[i]

	def non_linear_regression(self, variables, constants, equation, data, bound, init):
		#variables in list [x1, x2, x3 ...]
		#constants in list [k1, k2, k3 ...]
		#equation in sympy equation k1*x1+k2/x2 ... etc
		#data sequence must be matched variable sequence last is dependent variable data [data_x1, data_x2, data_x3 ... data_y] -> by n x m numpy array
		#bound : np.array([(k1_min, k1_max), (k2_min, k2_max)....])
		#init : [k1_0, k2_0, k3_0 ...]
		#all symbols must be expressed by sympy symbols


		def v_squared(variables, constants, equation, data):
			temp = []
			exp, cal = sp.symbols(('exp', 'cal'))
			det = (exp-cal)**2/(len(data)-1-len(constants))
			
			for i in range(len(data[-1])):
				temp.append(det.subs(exp, data[-1][i]))
			
			cal_temp = []
			for i in range(len(variables)):
				if i == 0:
					for j in range(len(data[0])):
						cal_temp.append(equation.subs(variables[i], data[i][j]))
				else:
					for j in range(len(data[0])):
						cal_temp[j] = cal_temp[j].subs(variables[i], data[i][j])
			
			v_squared = 0
			for i in range(len(temp)):
				v_squared += temp[i].subs(cal, cal_temp[i])
			
			return v_squared

		def Do_NLR(variables, constants, equation, data, bound, init):
			
			def func(params):
				det = v_squared(variables, constants, equation, data)
				text = str(constants)[1:-1]
				text_conv = ''
				i_before = 0
				for i in range(len(text)):
					if text[i] == ',':
						text_conv += text[i_before:i]+'_'
						i_before = i
					elif i == len(text)-1:
						text_conv += text[i_before:i+1]+'_'
				
				exec(text_conv + '= params')
				
				temp = det
				for i in range(len(constants)):
					temp = temp.subs(constants[i], eval(str(constants[i])+'_'))
	
				return temp
			
			result = minimize(func, x0 = init, bounds = bound)
			return result
		
		result = Do_NLR(variables, constants, equation, data, bound, init)
		print(result)
		return result.x

if __name__ == "__main__":
	
	r_exp = [71, 71.3, 41.6, 19.7, 42, 17.1, 71.8, 142, 284, 47, 71.3, 117, 127, 131, 133, 41.8]
	PT_exp = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 5, 10, 15, 20, 1]
	PH_exp = [1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 1, 1, 1]
	PM_exp = [1, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
	PB_exp = [0, 0, 1, 4, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]	
	
	
	#variables
	r, PT, PH, PM, PB = sp.symbols(('r', 'PT', 'PH', 'PM', 'PB'))
	
	#constants
	k, KB, KT = sp.symbols(('k', 'KB', 'KT'))
	
	variables = [PT, PH, PM, PB]
	constants = [k, KB, KT]
	equation = k*PH*PT/(1+KB*PB+KT*PT)
	data = np.array([PT_exp, PH_exp, PM_exp, PB_exp, r_exp])
	bound = np.array([(0, 200), (0, 2), (0, 2)])
	init = [144, 1.4, 1.03]

	calc = Calculation_tool()
	result = calc.non_linear_regression(variables, constants, equation, data, bound, init)
	print(result)
