import pandas as pd
from pathlib import Path
from helpers import load_closest_pair_dataset, load_karatsuba_dataset
from closest_pair import solve_closest_pair
from karatsuba import solve_karatsuba

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def benchmark_all():
    cp_results = []
    print("--- Benchmarking Closest Pair ---")
    for i in range(1, 11):
        name = f"cp{i:02d}"
        file_path = DATASETS_DIR / f"{name}.txt"
        if not file_path.exists():
            continue
        pts = load_closest_pair_dataset(file_path)
        if len(pts) > 100000:
            print(f"Skipping {name} (N={len(pts):,}) for quick benchmark.")
            continue
        res = solve_closest_pair(pts)
        cp_results.append({
            "File": name,
            "Points": len(pts),
            "Distance": round(res["distance"], 6),
            "Time (s)": round(res["time"], 6)
        })
        print(f"{name}: N={len(pts):,} | Time: {res['time']:.4f}s")

    pd.DataFrame(cp_results).to_csv(RESULTS_DIR / "cp_results.csv", index=False)

    im_results = []
    print("\n--- Benchmarking Karatsuba ---")
    for i in range(1, 11):
        name = f"im{i:02d}"
        file_path = DATASETS_DIR / f"{name}.txt"
        if not file_path.exists():
            continue
        n1, n2 = load_karatsuba_dataset(file_path)
        if len(n1) > 100000 or len(n2) > 100000:
            print(f"Skipping {name} (Digits={len(n1):,}) - exceeds benchmark threshold.")
            continue
        res = solve_karatsuba(n1, n2)
        im_results.append({
            "File": name,
            "Digits A": len(n1),
            "Digits B": len(n2),
            "Time (s)": round(res["time"], 6)
        })
        print(f"{name}: Digits=({len(n1):,}, {len(n2):,}) | Time: {res['time']:.4f}s")

    pd.DataFrame(im_results).to_csv(RESULTS_DIR / "im_results.csv", index=False)
    print("\nResults saved to 'results/' directory.")

if __name__ == "__main__":
    benchmark_all()