import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

from sklearn.linear_model import LinearRegression


arr_degree = np.array([-25.0, -25.0, 0., 25.0, 25.0])
#arr_posX = np.array([[3.0], [41.0], [50.0], [82.0], [81.0]])
arr_posX = np.array([3.0, 41.0, 50.0, 82.0, 81.0])

arr_degree = arr_degree.reshape(-1, 1)
#arr_posX = arr_posX.reshape(-1,1)

print('arr_degree: \n', arr_degree)
print('arr_posX: \n', arr_posX)


plt.scatter(arr_degree, arr_posX)

model_lr = LinearRegression()
model_lr.fit(arr_degree, arr_posX)

plt.plot(arr_degree, model_lr.predict(arr_degree), color='r', linestyle='solid')
plt.show()
