import numpy as np

def sphere(X):
    return np.sum(X*X, axis=1)
def rastrigin(X):
    n = X.shape[1]
    return 10*n + np.sum(X**2 -10*np.cos(2*np.pi*X), axis=1)

if __name__=="__main__":
    print(sphere(np.array([[1.0,2.0]])))
    print(rastrigin(np.zeros((1,10))))
    print(rastrigin(np.ones((1,2))))