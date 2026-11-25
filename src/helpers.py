import sys
from pathlib import Path
from typing import List, Tuple

# Increase max integer string conversion digits for safety
sys.set_int_max_str_digits(2000000)

def load_closest_pair_dataset(file_path: Path) -> List[Tuple[float, float]]:
    """Reads a Closest Pair dataset file containing N (x, y) coordinates."""
    points = []
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        if not first_line:
            return points
        n = int(first_line)
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                points.append((float(parts[0]), float(parts[1])))
    return points

def load_karatsuba_dataset(file_path: Path) -> Tuple[str, str]:
    """Reads an Integer Multiplication dataset file containing two large decimal strings."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) >= 2:
        return lines[0], lines[1]
    elif len(lines) == 1:
        return lines[0], ""
    return "", ""