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

def de(func, n,lb, ub, NP=30, G=50, F=0.5, CR=0.9, seed=0):
    rng=np.random.default_rng(seed)
    evals=0

    pop = lb+rng.random((NP,n))*(ub-lb)
    fpop = func(pop); evals+=NP
    history =[fpop.min()]

    for gen in range(G):
        trials = np.empty_like(pop)

        for i in range(NP):
            cands = [k for k in range (NP) if k != i]
            r1,r2,r3 = rng.choice(cands, size=3, replace=False)
            don = pop[r1]+F*(pop[r2]-pop[r3])
            j_rand = rng.integers(n)

            cross = rng.random(n)<CR
            cross[j_rand] = True
            trial = np.where(cross, don, pop[i])
            trials[i] = np.clip(trial, lb, ub)
        ftrials = func(trials); evals += NP

        best = ftrials < fpop
        pop[best] = trials[best]
        fpop[best] = ftrials[best]
        history.append(fpop.min())
    b = np.argmin(fpop)
    return fpop[b],pop[b].copy(), evals, history

if __name__ == "__main__":
    from benchmarks import sphere
    f, xbest,evals, _ = pso(sphere, n=10, lb=-5.12,ub=5.12, seed=0)
    print("f =", f, " evals", evals)
    assert evals == 1530
    f2, *_ = pso(sphere, n=10, lb=-5.12,ub=5.12, seed=0)
    print("reproducible:", f == f2)

    f, xbest,evals, _ = de(sphere, n=10, lb=-5.12,ub=5.12, seed=0)
    print("DE f=", f, " evals", evals)
    assert evals == 1530
    f2, *_ = de(sphere, n=10, lb=-5.12,ub=5.12, seed=0)
    print("reproducible:", f == f2)

    