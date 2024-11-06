# Print the initial problem where S - supply array, C - cost matrix, D - demand array
def print_problem(S, C, D):
    # Header for destinations and supply
    print(f"{'':<8}|{' Destinations' + (len(D) * 9 - 12) * ' '}|")
    print(f"{'Sources':<8}|", end=" ")
    for i in range(len(D)):
        print(f"{i+1:<8}", end=" ")
    print(f"| {'Supply':<7}")
    print("-" * 8 + "+" + "-" * (len(D) * 9 + 1) + "+" + "-" * 8)

    # Rows for sources, cost matrix, and supply
    for i in range(len(S)):
        print(f"{i+1:<8}|", end=" ")
        for j in range(len(D)):
            print(f"{C[i][j]:<8}", end=" ")
        print(f"| {S[i]:<7}")

    # Footer for demand row
    print("-" * 8 + "+" + "-" * (len(D) * 9 + 1) + "+" + "-" * 8)
    print(f"{'Demand':<8}|", end=" ")
    for d in D:
        print(f"{d:<8}", end=" ")
    print("|")

# Print the initial feasible solution - ans
def print_solution(ans):
    for i in ans:
        print(f"x_{i[0]},{i[1]} = {i[2]}")

# Check if problem is balanced, returns true if okay. S - supply array, C - cost matrix, D - demand array
def check_problem(S, D):
    if sum(S) != sum(D):
        print("The problem is not balanced!")
        return False
    return True

# applying north-west algorithm on problem, returning initial feasible solution in form: [row, column, amount]; S-supply array, C-cost matrix, D-demand array
def north_west_alg(S, C, D):
    S = S[:]
    D = D[:]
    ind = [0, 0]
    x_0 = []
    while sum(S) > 0:
        if S[ind[0]] > 0 and D[ind[1]] > 0:
            x = min(S[ind[0]], D[ind[1]])
            x_0.append([ind[0] + 1, ind[1] + 1, x])
            S[ind[0]] -= x
            D[ind[1]] -= x
        if D[ind[1]] == 0:
            ind[1] += 1
        elif S[ind[0]] == 0:
            ind[0] += 1
    return x_0


def russel_alg(S, C, D):
    # Copy the supply and demand arrays to avoid modifying the originals
    supply = S[:]
    demand = D[:]
    allocation = []  # Holds the final allocations in the format [destination, source, allocated amount]

    while sum(supply) > 0 and sum(demand) > 0:
        # Calculate row and column maximum values
        row_max = [max(costs) if supply[i] > 0 else float('-inf') for i, costs in enumerate(C)]
        col_max = [max([C[i][j] for i in range(len(supply))]) if demand[j] > 0 else float('-inf') for j in range(len(demand))]

        # Initialize the most negative opportunity cost
        most_neg = float('inf')
        i_new, j_new = None, None

        # Find the cell with the most negative opportunity cost
        for i in range(len(supply)):
            for j in range(len(demand)):
                if supply[i] > 0 and demand[j] > 0:  # Only consider cells where supply and demand are positive
                    delta = C[i][j] - (row_max[i] + col_max[j])
                    if delta < most_neg:
                        most_neg = delta
                        i_new, j_new = i, j

        # Allocate the minimum of supply or demand for the selected cell
        if i_new is not None and j_new is not None:
            allocation_value = min(supply[i_new], demand[j_new])
            allocation.append([j_new + 1, i_new + 1, allocation_value])

            # Update supply and demand
            supply[i_new] -= allocation_value
            demand[j_new] -= allocation_value

    return allocation

# Example data
S = [10, 20, 40]
D = [5, 15, 30, 20]
C = [[1, 4, 2, 8],
     [9, 3, 7, 1],
     [6, 2, 5, 9]]

# Execute the functions
print_problem(S, C, D)
if check_problem(S, D):
    print()
    print("NORTH-WEST:")
    ans = north_west_alg(S, C, D)
    print_solution(ans)
    print()
    print("RUSSEL:")
    ans = russel_alg(S, C, D)
    print_solution(ans)
