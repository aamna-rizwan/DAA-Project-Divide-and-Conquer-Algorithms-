from closest_pair import solve_closest_pair, closest_pair_brute_force
from karatsuba import solve_karatsuba

def validate():
    print("Validating Closest Pair...")
    test_pts = [(0.0, 0.0), (5.0, 5.0), (1.0, 1.0), (2.0, 2.0), (10.0, 10.0)]
    rec_res = solve_closest_pair(test_pts)
    bf_res = closest_pair_brute_force(test_pts)
    assert abs(rec_res["distance"] - bf_res[2]) < 1e-6, "Closest pair distance mismatch!"
    print("Closest Pair algorithm validated successfully!")

    print("Validating Karatsuba...")
    num1, num2 = "12345678901234567890", "98765432109876543210"
    k_res = solve_karatsuba(num1, num2)
    expected = str(int(num1) * int(num2))
    assert k_res["product"] == expected, "Karatsuba output mismatch!"
    print("Karatsuba algorithm validated successfully!")

if __name__ == "__main__":
    validate()