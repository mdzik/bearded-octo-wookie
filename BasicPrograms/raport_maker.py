



import bearded_octo_wookie.RaportMaker as plt
import numpy as np


plt.raport.path = '/tmp/raport.npz'

x = np.linspace(0,1)

plt.figure()

plt.plot(x,np.sin(x),'o', ms=30)

plt.title('asasas')

x = 2. * x
plt.plot(x,np.sin(x),'x-', ms=30)

plt.figure()
plt.loglog(x,x**2,'-', label='15')
plt.legend(loc=0)
plt.show()