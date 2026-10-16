import numpy as np

def pso(func, n, lb, ub, N=30, T=50, w=0.7,c1=1.4, c2=1.4, seed=0):
    rng = np.random.default_rng(seed)
    evals = 0
    x = lb +rng.random((N,n))*(ub-lb)
    v = np.zeros((N,n))
    fx = func(x); evals+=N

    pbest = x.copy()
    f_pbest = fx.copy()
    g = np.argmin(f_pbest)
    gbest = pbest[g].copy()
    f_gbest = f_pbest[g]
    history = [f_gbest]

    for t in range(T):
        r1 = rng.random((N,n))
        r2 = rng.random((N,n))
        v = w*v+c1*r1*(pbest-x)+c2*r2*(gbest-x)
        x = np.clip(x+v,lb,ub)
        fx = func(x);evals+=N

        besto = fx< f_pbest
        pbest[besto]=x[besto]
        f_pbest[besto]=fx[besto]

        g = np.argmin(f_pbest)
        if f_pbest[g]<f_gbest:
            gbest = pbest[g].copy()
            f_gbest = f_pbest[g]
        history.append(f_gbest)

    return f_gbest,gbest,evals,history

if __name__ == "__main__":
    from benchmarks import sphere
    f, xbest,evals, _ = pso(sphere, n=10, lb=-5.12,ub=5.12, seed=0)
    print("f =", f, " evals", evals)
    assert evals == 1530
    f2, *_ = pso(sphere, n=10, lb=-5.12,ub=5.12, seed=0)
    print("reproducible:", f == f2)