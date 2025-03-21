import galois
from collections import Counter
import itertools

# Define GF(2)
GF2 = galois.GF(2)

# User input for functions F_0 and F_1
def user_defined_F():
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
F_0, F_1 = user_defined_F()

def compute_c_derivative(xa, x, c0, c1):
    """
    Computes the c-differential: D_c F(x, a) = F(x + a) + c * F(x).
    """
    x_a0, x_a1 = GF2(xa[0]), GF2(xa[1])  # Convert to GF(2)
    x0, x1 = GF2(x[0]), GF2(x[1])  # Convert to GF(2)
    c0, c1 = GF2(c0), GF2(c1)  # Convert to GF(2)

    # Compute F(x + a)
    Fx_a0 = F_0(x_a0, x_a1)
    Fx_a1 = F_1(x_a0, x_a1)

    # Compute c * F(x)
    c_Fx0 = (c0 * F_0(x0, x1)) + (c1 * F_1(x0, x1))  # Addition in GF(2)
    c_Fx1 = (c0 * F_1(x0, x1)) + (c1 * F_0(x0, x1)) + (c1 * F_1(x0, x1))

    # Compute D_c F(x, a) = F(x + a) + c * F(x)
    D_c_F0 = Fx_a0 + c_Fx0  # Addition in GF(2)
    D_c_F1 = Fx_a1 + c_Fx1

    return (int(D_c_F0), int(D_c_F1))

# Generate all possible values for a, x, and c
a_values = [(GF2(a0), GF2(a1)) for a0 in range(2) for a1 in range(2)]
x_values = [(GF2(x0), GF2(x1)) for x0 in range(2) for x1 in range(2)]
c_values = [(GF2(c0), GF2(c1)) for c0 in range(2) for c1 in range(2)]

# Compute D_c F for all a, x, and (c0, c1) combinations
results = []
total_counter = Counter()
a_counters = {tuple(map(int, a)): Counter() for a in a_values}

for a in a_values:
    a_tuple = tuple(map(int, a))
    for x in x_values:
        x_tuple = tuple(map(int, x))
        x_a = (int(x[0] + a[0]), int(x[1] + a[1]))  # Compute x + a using GF(2) addition
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