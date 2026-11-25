import time
from typing import Dict, Any, List, Optional

def _add_str(num1: str, num2: str) -> str:
    i, j = len(num1) - 1, len(num2) - 1
    carry = 0
    res = []
    while i >= 0 or j >= 0 or carry:
        n1 = ord(num1[i]) - 48 if i >= 0 else 0
        n2 = ord(num2[j]) - 48 if j >= 0 else 0
        s = n1 + n2 + carry
        carry = s // 10
        res.append(chr(48 + (s % 10)))
        i -= 1
        j -= 1
    return "".join(reversed(res)).lstrip('0') or '0'

def _sub_str(num1: str, num2: str) -> str:
    i, j = len(num1) - 1, len(num2) - 1
    borrow = 0
    res = []
    while i >= 0:
        n1 = ord(num1[i]) - 48 - borrow
        n2 = ord(num2[j]) - 48 if j >= 0 else 0
        if n1 < n2:
            n1 += 10
            borrow = 1
        else:
            borrow = 0
        res.append(chr(48 + (n1 - n2)))
        i -= 1
        j -= 1
    return "".join(reversed(res)).lstrip('0') or '0'

def _schoolbook_mult(x: str, y: str) -> str:
    return str(int(x) * int(y))

def _karatsuba_rec(x: str, y: str, depth: int = 0, trace: Optional[List[Dict[str, Any]]] = None) -> str:
    x = x.lstrip('0') or '0'
    y = y.lstrip('0') or '0'

    if x == '0' or y == '0':
        return '0'

    # Base case threshold
    if len(x) <= 32 or len(y) <= 32:
        return _schoolbook_mult(x, y)

    n = max(len(x), len(y))
    m = n // 2

    x_pad = x.zfill(n)
    y_pad = y.zfill(n)

    high1, low1 = x_pad[:-m], x_pad[-m:]
    high2, low2 = y_pad[:-m], y_pad[-m:]

    z2 = _karatsuba_rec(high1, high2, depth + 1, trace)
    z0 = _karatsuba_rec(low1, low2, depth + 1, trace)
    
    lh1_lh2 = _karatsuba_rec(_add_str(high1, low1), _add_str(high2, low2), depth + 1, trace)
    z1 = _sub_str(_sub_str(lh1_lh2, z2), z0)

    # Combine: z2 * 10^(2m) + z1 * 10^m + z0
    term1 = (z2 + '0' * (2 * m)) if z2 != '0' else '0'
    term2 = (z1 + '0' * m) if z1 != '0' else '0'

    res = _add_str(_add_str(term1, term2), z0)

    if trace is not None and depth <= 2:
        trace.append({
            "depth": depth,
            "x": x, "y": y,
            "high1": high1, "low1": low1,
            "high2": high2, "low2": low2,
            "z2": z2, "z1": z1, "z0": z0,
            "result": res
        })

    return res

def solve_karatsuba(x: str, y: str, max_digits: int = 100000, capture_trace: bool = False) -> Dict[str, Any]:
    start_time = time.perf_counter()

    # Block ONLY if BOTH numbers exceed 100,000 digits (e.g. im04: 1,000,000 x 1,000,000)
    if len(x) > max_digits and len(y) > max_digits:
        return {
            "product": None,
            "time": 0.0,
            "limited": True,
            "reason": f"Input size ({len(x):,} x {len(y):,} digits) exceeds the Python execution limit of {max_digits:,} digits."
        }

    trace = [] if capture_trace else None
    product = _karatsuba_rec(x, y, 0, trace)
    elapsed_time = time.perf_counter() - start_time

    return {
        "product": product,
        "time": elapsed_time,
        "limited": False,
        "trace": trace
    }
