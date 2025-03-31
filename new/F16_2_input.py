import galois
from collections import Counter
import itertools

# Define GF(2)
GF2 = galois.GF(2)
elements = [GF2(0), GF2(1)]

# User input for functions F_0 through F_3
def user_defined_F():
    print("Enter the function for F_0(x0, x1, x2, x3) using x0, x1, x2, x3:")
    F_0_expr = input("F_0: ")
    print("Enter the function for F_1(x0, x1, x2, x3) using x0, x1, x2, x3:")
    F_1_expr = input("F_1: ")
    print("Enter the function for F_2(x0, x1, x2, x3) using x0, x1, x2, x3:")
    F_2_expr = input("F_2: ")
    print("Enter the function for F_3(x0, x1, x2, x3) using x0, x1, x2, x3:")
    F_3_expr = input("F_3: ")

    def F_0(x0, x1, x2, x3): return eval(F_0_expr)
    def F_1(x0, x1, x2, x3): return eval(F_1_expr)
    def F_2(x0, x1, x2, x3): return eval(F_2_expr)
    def F_3(x0, x1, x2, x3): return eval(F_3_expr)

    return F_0, F_1, F_2, F_3

# Get user-defined functions
F_0, F_1, F_2, F_3 = user_defined_F()

def product(u, v):
    """Defines the product (u0, u1, u2, u3) * (v0, v1, v2, v3) over GF(2) with x^4 + x^3 + 1."""
    u0, u1, u2, u3 = u
    v0, v1, v2, v3 = v
    return (
        u0*v0 + u2*v2 + u1*v3 + u3*v1 + u2*v3 + u3*v2 + u3*v3,
        u0*v1 + u1*v0 + u2*v3 + u3*v2 + u3*v3,
        u1*v1 + u2*v0 + u0*v2 + u3*v3,
        u2*v1 + u1*v2 + u0*v3 + u3*v0 + u2*v2 + u1*v3 + u3*v1 + u2*v3 + u3*v2 + u3*v3
    )

def compute_c_derivative(xa, x, c0, c1, c2, c3):
    x_a0, x_a1, x_a2, x_a3 = GF2(xa[0]), GF2(xa[1]), GF2(xa[2]), GF2(xa[3])
    x0, x1, x2, x3 = GF2(x[0]), GF2(x[1]), GF2(x[2]), GF2(x[3])
    c0, c1, c2, c3 = GF2(c0), GF2(c1), GF2(c2), GF2(c3)

    Fx_a = (
        F_0(x_a0, x_a1, x_a2, x_a3),
        F_1(x_a0, x_a1, x_a2, x_a3),
        F_2(x_a0, x_a1, x_a2, x_a3),
        F_3(x_a0, x_a1, x_a2, x_a3)
    )
    Fx = (
        F_0(x0, x1, x2, x3),
        F_1(x0, x1, x2, x3),
        F_2(x0, x1, x2, x3),
        F_3(x0, x1, x2, x3)
    )

    cFx = product((c0, c1, c2, c3), Fx)
    DcF = tuple(int(fx_a + cf_x) for fx_a, cf_x in zip(Fx_a, cFx))
    return DcF

# Generate all a, x, c combinations
a_values = list(itertools.product(elements, repeat=4))
x_values = list(itertools.product(elements, repeat=4))
c_values = list(itertools.product(elements, repeat=4))

results = []
total_counter = Counter()
a_counters = {tuple(map(int, a)): Counter() for a in a_values}

for a in a_values:
    a_tuple = tuple(map(int, a))
    for x in x_values:
        x_tuple = tuple(map(int, x))
        x_a = tuple(int(x[i] + a[i]) for i in range(4))
        for c in c_values:
            c_tuple = tuple(map(int, c))
            DcF = compute_c_derivative(x_a, x, *c)
            results.append((c_tuple, a_tuple, x_tuple, DcF))
            a_counters[a_tuple][DcF] += 1
            total_counter[DcF] += 1

# Sort results by c -> a -> x
results.sort()

print("\n## Final Results (binary):")
previous_a = None
for c_tuple, a_tuple, x_tuple, (e0, e1, e2, e3) in results:
    if previous_a is not None and previous_a != a_tuple:
        print()
    print(f"c = {c_tuple}, a = {a_tuple}, x = {x_tuple}: (D_c_F = {e0, e1, e2, e3})")
    previous_a = a_tuple

print("\n## Result Counts Per a:")
for a, counter in sorted(a_counters.items()):
    print(f"For a = {a}:")
    for key, count in sorted(counter.items()):
        print(f"  Result {key}: {count} occurrences")
    print()

print("\n## Total Result Counts:")
for key, count in sorted(total_counter.items()):
    print(f"Result {key}: {count} occurrences")
