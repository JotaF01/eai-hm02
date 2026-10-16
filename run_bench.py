import json, csv, os
import numpy as np
from optimizers import pso, de
from benchmarks import sphere, rastrigin

N_DIM, LB, UB = 10, -5.12, 5.12
POP, GENS = 30, 50
BUDGET = POP * (1 + GENS)
SEEDS = list(range(30))
PARAMS = {"PSO": dict(w=0.7, c1=1.4, c2=1.4), "DE": dict(F=0.5, CR=0.9)}
FUNCS = {"Sphere": sphere, "Rastrigin": rastrigin}

os.makedirs("results", exist_ok=True)
raw, table = [], []

for fname, func in FUNCS.items():
    for mname in ["PSO", "DE"]:
        finals, histories = [], []
        for s in SEEDS:
            if mname == "PSO":
                f, x, evals, hist = pso(func, N_DIM, LB, UB, N=POP, T=GENS, seed=s, **PARAMS["PSO"])
            else:
                f, x, evals, hist = de(func, N_DIM, LB, UB, NP=POP, G=GENS, seed=s, **PARAMS["DE"])
            assert evals == BUDGET, f"{mname} spent {evals} evaluations, expected {BUDGET}"
            finals.append(float(f)); histories.append([float(h) for h in hist])
            raw.append({"function": fname, "method": mname, "seed": s, "evals": evals,
                        "final_best": float(f), "x_best": x.tolist(), "history": histories[-1]})
        a = np.array(finals)
        table.append({"function": fname, "method": mname, "best": a.min(), "worst": a.max(),
                      "mean": a.mean(), "std": a.std(ddof=1)})
        np.savetxt(f"results/conv_{fname}_{mname}.dat",
                   np.column_stack([np.arange(GENS + 1), np.mean(histories, axis=0)]),
                   header="generation mean_best_so_far")
        print(f"{fname:9s} {mname:3s}  evals per run = {evals}  (assert 1530 OK)")

config = {"n": N_DIM, "bounds": [LB, UB], "bounds_handling": "clip (both methods)",
          "pop": POP, "generations": GENS, "budget": BUDGET, "seeds": SEEDS, "params": PARAMS}
json.dump({"config": config, "runs": raw}, open("results/part1_raw.json", "w"), indent=1)

with open("results/part1_table.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=table[0].keys()); w.writeheader(); w.writerows(table)

print("\n| function | method | best | worst | mean | std |")
print("|---|---|---|---|---|---|")
for r in table:
    print(f"| {r['function']} | {r['method']} | {r['best']:.3e} | {r['worst']:.3e} | {r['mean']:.3e} | {r['std']:.3e} |")