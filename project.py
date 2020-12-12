import numpy as np
import matplotlib.pyplot as plt

def find_in(array, target):
	for i in range(len(array)):
		if (target-array[i])<=0:
			return i


'''
Basis setup below
'''

intensity_coeff = 42500

target_time = np.array([4*60, 60*60])

D = 2.2*10**-6 		#cm^2/s
L = 4 					#cm
x_array = np.hstack([np.arange(0,0.6,0.1), np.arange(0.6,1.4,0.001), np.arange(1.4,L+0.2,0.2)])
np.save('x_array.npy', x_array)

nt = 100000
t_array = np.linspace(0, target_time[-1], nt)
dt = t_array[1] - t_array[0]

C_init = 1
C_lim = 0

C_array = np.zeros_like(x_array)+(C_init+C_lim)/2		#mol/ml

x_interface = find_in(x_array, 1)
C_array[0:x_interface] = C_init
C_array[x_interface:-1] = C_lim

target_time_i = np.zeros_like(target_time)
for i in range(len(target_time)):
    target_time_i[i] = find_in(t_array, target_time[i])

xi_1 = find_in(x_array, 1)
xi_2 = find_in(x_array, 1.3)


'''
Main calculation below
'''
#C_array[t][x], C_array[i][j]

#C[i+1][j] = dt/dx^2 * D * (C[i][j+1]-2*C[i][j]+C[i][j-1])+C[i][j] 
plt.close()
progress = int(0)
print(str(progress) + '% done')
i = 0
for i in range(len(t_array)):
    C_bef = C_array	
    C_bef[0] = C_init
    C_bef[len(C_bef)-1] = C_lim
    progress_temp = int(i/len(t_array)*100)
    if progress_temp != progress:
        progress = progress_temp
        print('{}'.format(progress) + '% done')
		
    while True:
        C_next = C_bef

        for j in range(1, len(x_array)-1):
            dx_av = (x_array[j+1]-x_array[j-1])/2
            C_next[j] = dt/dx_av * D * ((C_bef[j+1]-C_bef[j])/(x_array[j+1]-x_array[j])-(C_bef[j]-C_bef[j-1])/(x_array[j]-x_array[j-1]))+C_bef[j]
            
        det = (C_next - C_bef)/(C_bef+(C_init+C_lim)/2)

        if abs(det.max()) < 0.00001:
            C_array = C_next
            break
        else:
            C_bef = C_next

    flag = -1
    for j in range(len(target_time_i)):
        if i == target_time_i[j]:
            flag = target_time_i[j]
            target_time_i = np.delete(target_time_i, j)
            break

    if flag != -1:
        t = np.round_(t_array[flag]/60,0)
        np.save('{}min_sample.npy'.format(t), C_array)
        plt.plot((x_array[xi_1:xi_2]-x_array[xi_1])*10000, C_array[xi_1:xi_2]*intensity_coeff, label = 't = {} min'.format(t))
        flag = -1

plt.xlabel('Distance in um')
plt.ylabel('Intensity')
plt.title('Emulation')
plt.xlim([0,3000])
plt.ylim([0,25000])
plt.legend()
plt.grid()
plt.show()