import math
import time
from typing import List, Tuple, Dict, Any, Optional

Point = Tuple[float, float]

def euclidean_distance(p1: Point, p2: Point) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def closest_pair_brute_force(points: List[Point]) -> Tuple[Point, Point, float]:
    min_dist = float('inf')
    p1_best, p2_best = points[0], points[1]
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                p1_best, p2_best = points[i], points[j]
    return p1_best, p2_best, min_dist

def _closest_pair_rec(Px: List[Point], Py: List[Point], trace: Optional[List[Dict[str, Any]]] = None) -> Tuple[Point, Point, float]:
    n = len(Px)
    
    if n <= 3:
        p1, p2, dist = closest_pair_brute_force(Px)
        if trace is not None:
            trace.append({
                "type": "base_case",
                "points": Px,
                "closest": (p1, p2),
                "dist": dist
            })
        return p1, p2, dist

    mid = n // 2
    mid_point = Px[mid]
    mid_x = mid_point[0]

    Lx = Px[:mid]
    Rx = Px[mid:]

    # Divide Py into Ly and Ry using set for fast lookup
    left_set = set(Lx)
    Ly = [p for p in Py if p in left_set]
    Ry = [p for p in Py if p not in left_set]

    p1_l, p2_l, d_l = _closest_pair_rec(Lx, Ly, trace)
    p1_r, p2_r, d_r = _closest_pair_rec(Rx, Ry, trace)

    if d_l < d_r:
        best_p1, best_p2, delta = p1_l, p2_l, d_l
    else:
        best_p1, best_p2, delta = p1_r, p2_r, d_r

    # Build Strip
    strip = [p for p in Py if abs(p[0] - mid_x) < delta]

    strip_p1, strip_p2, strip_min = None, None, delta
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < strip_min:
            d = euclidean_distance(strip[i], strip[j])
            if d < strip_min:
                strip_min = d
                strip_p1, strip_p2 = strip[i], strip[j]
            j += 1

    if strip_p1 is not None and strip_p2 is not None and strip_min < delta:
        best_p1, best_p2, delta = strip_p1, strip_p2, strip_min

    if trace is not None:
        trace.append({
            "type": "recursive_merge",
            "mid_x": mid_x,
            "delta": delta,
            "strip": strip,
            "best_pair": (best_p1, best_p2),
            "dist": delta
        })

    return best_p1, best_p2, delta

def solve_closest_pair(points: List[Point], capture_trace: bool = False) -> Dict[str, Any]:
    start_time = time.perf_counter()
    
    Px = sorted(points, key=lambda p: (p[0], p[1]))
    Py = sorted(points, key=lambda p: (p[1], p[0]))
    
    trace = [] if capture_trace else None
    p1, p2, min_dist = _closest_pair_rec(Px, Py, trace)
    
    elapsed_time = time.perf_counter() - start_time
    
    return {
        "point1": p1,
        "point2": p2,
        "distance": min_dist,
        "time": elapsed_time,
        "trace": trace
    }