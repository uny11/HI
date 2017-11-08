
# import numpy as np
# import timeit

# a = np.array( [0,1,2,3,4,5] )
# b = a.reshape( (3,2) )
# b[1] [0] = 77
# c = a.reshape((3,2)).copy()
# c[0] [0] = -99
#
# print(a.dtype)
# print(type(a))
# # print(a > 4)
# # print(a[a>4])

# c = np.array([1, 2, np.NAN, 3, 4])
# print(c)
# print(np.isnan(c))
# print(c[~np.isnan(c)])

# normal_py_sec = timeit.timeit('sum(x*x for x in range(1000))', number=10000)
# naive_np_sec = timeit.timeit('sum(na*na)', setup="import numpy as np; na=np.arange(1000)",number=10000)
# good_np_sec = timeit.timeit('na.dot(na)',setup="import numpy as np; na=np.arange(1000)",number=10000)
# print("Normal Python: %f sec"%normal_py_sec)
# print("Naive NumPy: %f sec"%naive_np_sec)
# print("Good NumPy: %f sec"%good_np_sec)

import scipy, numpy

print(scipy.version.full_version)

print(scipy.dot is numpy.dot)
