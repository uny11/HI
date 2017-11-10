
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np
import scipy as sp

# We load the data with load_iris from sklearn
data = load_iris()
features = data['data']
feature_names = data['feature_names']
target = data['target']

# for t,marker,c in list(zip(range(3),">ox","rgb")):
#     # We plot each class on its own to get different colored markers
#     plt.scatter(features[target == t,0],
#                 features[target == t,1],
#                 marker=marker,
#                 c=c)
#
# plt.show()

plength = features[:, 2]
# use numpy operations to get setosa features
is_setosa = (labels == 'setosa')
# This is the important step:
max_setosa =plength[is_setosa].max()
min_non_setosa = plength[~is_setosa].min()
print('Maximum of setosa: {0}.'.format(max_setosa))
print('Minimum of others: {0}.'.format(min_non_setosa))
