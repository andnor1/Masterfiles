import galois
from collections import Counter
import itertools

# Define GF(3)
GF3 = galois.GF(3)

# Function to take user input for F_0 and F_1
def get_user_defined_functions():
    print("Enter the function for F_0(x0, x1) using x0, x1:")
    F_0_expr = input("F_0: ")
    print("Enter the function for F_1(x0, x1) using x0, x1:")
    F_1_expr = input("F_1: ")
    
    def F_0(x0, x1):
        return eval(F_0_expr)
    
    def F_1(x0, x1):
        return eval(F_1_expr)
    
    return F_0, F_1

# Get user-defined functions
F_0, F_1 = get_user_defined_functions()

def product(u, v):
    """Defines the product (u0,u1) * (v0,v1) over GF(3) with polynomial x^2 + 2x + 1."""
    u0, u1 = u
    v0, v1 = v
    return (u0 * v0 + u1 * v1, u0 * v1 + u1 * v0 + u1 * v1)

def compute_c_derivative(xa, x, c0, c1):
    """
    Computes the c-differential: D_c F(x, a) = F(x + a) - c * F(x).
    """
    x_a0, x_a1 = GF3(xa[0]), GF3(xa[1])
    x0, x1 = GF3(x[0]), GF3(x[1])
    c0, c1 = GF3(c0), GF3(c1)

    # Compute F(x + a)
    Fx_a0 = F_0(x_a0, x_a1)
    Fx_a1 = F_1(x_a0, x_a1)

    # Compute c * F(x) using the defined product
    c_Fx0, c_Fx1 = product((c0, c1), (F_0(x0, x1), F_1(x0, x1)))

    # Compute D_c F(x, a) = F(x + a) - c * F(x)
    D_c_F0 = Fx_a0 - c_Fx0  # Subtraction in GF(3)
    D_c_F1 = Fx_a1 - c_Fx1

    return (int(D_c_F0), int(D_c_F1))

# Generate all possible values for a, x, and c
a_values = [(GF3(a0), GF3(a1)) for a0 in range(3) for a1 in range(3)]
x_values = [(GF3(x0), GF3(x1)) for x0 in range(3) for x1 in range(3)]
c_values = [(GF3(c0), GF3(c1)) for c0 in range(3) for c1 in range(3)]

# Compute D_c F for all a, x, and (c0, c1) combinations
results = []
total_counter = Counter()
a_counters = {tuple(map(int, a)): Counter() for a in a_values}

for a in a_values:
    a_tuple = tuple(map(int, a))
    for x in x_values:
        x_tuple = tuple(map(int, x))
        x_a = (int(x[0] + a[0]), int(x[1] + a[1]))  # Compute x + a using GF(3) addition
        for c0, c1 in c_values:
            c_tuple = (int(c0), int(c1))
            D_c_F = compute_c_derivative(x_a, x, c0, c1)
            results.append((c_tuple, a_tuple, x_tuple, D_c_F))
            a_counters[a_tuple][tuple(D_c_F)] += 1  # Counter for each a
            total_counter[tuple(D_c_F)] += 1  # Total counter

# Sort results by c -> a -> x
results.sort()

# Display results
print("\n## Final Results (binary):")
previous_a = None
for c_tuple, a_tuple, x_tuple, (expr1, expr2) in results:
    if previous_a is not None and previous_a != a_tuple:
        print()  # Add space between different a values
    print(f"c = {c_tuple}, a = {a_tuple}, x = {x_tuple}: (D_c_F0 = {expr1}, D_c_F1 = {expr2})")
    previous_a = a_tuple

# Display count of different results per a
print("\n## Result Counts Per a:")
for a, counter in sorted(a_counters.items()):
    print(f"For a = {a}:")
    for key, count in sorted(counter.items()):
        print(f"  Result {key}: {count} occurrences")
    print()

# Display total count of different results
print("\n## Total Result Counts:")
for key, count in sorted(total_counter.items()):
    print(f"Result {key}: {count} occurrences")
 