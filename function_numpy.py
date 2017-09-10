import numpy as np


a = np.array([1,2,3,4,5])


a.dtype

a = np.array([1,2,3,4,5],dtype=np.float64)


a.ndim, a.shape, a.size

b = np.array([[1,2,3,4,5],[6,7,8,9,10]],dtype=np.float64)



b.dtype

b.ndim, b.shape, b.size

np.zeros((3,3),'d')

np.empty((4,4),'d')

np.linspace(0,10,5)

np.arange(0,10,2)

np.random.standard_normal((2,4))

a = np.random.standard_normal((2,3))
b = np.random.standard_normal((2,3))

np.vstack([a,b])

np.hstack([a,b])

a.transpose()

np.save('example.npy',a)

a1 = np.load('example.npy')

a1

#Part 2 Math with numpy



import numpy as np
import matplotlib.pyplot as pp

x = np.linspace(0,10,40)
x
sinx = np.sin(x)
pp.plot(x,sinx)

cosx = np.cos(x)

pp.plot(x,sinx)
pp.plot(x,cosx)
pp.legend(['sin(x)','cos(x)'])

y = sinx * cosx
z = cosx**2 - sinx**2
pp.plot(x,y)
pp.plot(x,z)



np.dot(sinx,cosx)
np.outer(sinx,cosx)

v = np.linspace(0,10,5)
v + 1

vv = np.outer(v,v)
vv + v

vv + v[:,np.newaxis]


#part3, index and slicing


v = np.linspace(0,10,5)

v[0]

v[1]

v[-1]

v[5]

vv = np.random.random((5,4))

vv

vv[0,0]

vv[4,3]

ll = [[1,2,3],[4,5,6],[7,8,9]]

ll[1,2]

ll[1][2]

v[2:4]

vv[2:5,1]

vv[2:5,1:2]

vv[2:-1,:]

vv[:,::2]

# copy is not made during slicing, so any modification on slice index also modfices the orginal
v2 = v[2:4]

v2[0] = 0

v

v3 = v[2:4].copy()

v3[0] = 1

v

v[[1,2,3]]

bool_index = v > 0

v[bool_index]

vv[vv > 0.5] = vv[vv > 0.5] * 2

vv