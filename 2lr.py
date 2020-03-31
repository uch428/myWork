from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt



X = np.array([-25.0, -25.0, 0., 25.0, 25.0])
y = np.array([[3.0], [41.0], [50.0], [82.0], [81.0]])

X = X.reshape(-1,1)







print('X: \n', X)
print('y: \n', y)

plt.scatter(X,y)

model = LinearRegression()
model.fit(X,y)

plt.plot(X, model.predict(X))
plt.show()
