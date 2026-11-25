import json, random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

SEEDS = {
    "cp01": 41001, "cp02": 41002, "cp03": 41003, "cp04": 41004, "cp05": 41005,
    "cp06": 41006, "cp07": 41007, "cp08": 41008, "cp09": 41009, "cp10": 41010,
    "im01": 52001, "im02": 52002, "im03": 52003, "im04": 52004, "im05": 52005,
    "im06": 52006, "im07": 52007, "im08": 52008, "im09": 52009, "im10": 52010,
}

CP_SIZES = {
    "cp01": 1000, "cp02": 10000, "cp03": 100000, "cp04": 1000000, "cp05": 1000000,
    "cp06": 50000, "cp07": 50000, "cp08": 50000, "cp09": 50000, "cp10": 101
}

IM_SIZES = {
    "im01": 1000, "im02": 10000, "im03": 100000, "im04": 1000000, "im05": (1000000, 10),
    "im06": 50000, "im07": 50000, "im08": 50000, "im09": 50000, "im10": 101
}

def generate_cp_file(filename: str, n: int, seed: int):
    random.seed(seed)
    path = DATASETS_DIR / f"{filename}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{n}\n")
        if filename == "cp06":  # Duplicate points test
            for _ in range(n - 2):
                f.write(f"{random.uniform(-1000, 1000):.4f} {random.uniform(-1000, 1000):.4f}\n")
            f.write("12.3456 78.9012\n12.3456 78.9012\n")
        elif filename == "cp07":  # Vertical line test
            for _ in range(n):
                f.write(f"500.0000 {random.uniform(-1000, 1000):.4f}\n")
        else:
            for _ in range(n):
                f.write(f"{random.uniform(-1000, 1000):.4f} {random.uniform(-1000, 1000):.4f}\n")

def generate_im_file(filename: str, size: Any, seed: int):
    random.seed(seed)
    path = DATASETS_DIR / f"{filename}.txt"
    if isinstance(size, tuple):
        s1, s2 = size
    else:
        s1, s2 = size, size

    def rand_digits(d):
        return "".join([str(random.randint(1, 9))] + [str(random.randint(0, 9)) for _ in range(d - 1)])

    num1 = rand_digits(s1)
    num2 = rand_digits(s2) if filename != "im09" else "0"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{num1}\n{num2}\n")

def main():
    print("Generating input datasets...")
    for key, seed in SEEDS.items():
        if key.startswith("cp"):
            generate_cp_file(key, CP_SIZES[key], seed)
        elif key.startswith("im"):
            generate_im_file(key, IM_SIZES[key], seed)
    
    (DATASETS_DIR / "seeds.json").write_text(json.dumps(SEEDS, indent=2), encoding="utf-8")
    print(f"Generated 20 datasets in '{DATASETS_DIR}' along with seeds.json.")

if __name__ == "__main__":
    main()
