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

def vogel_alg(S, C, D):
    # Create copies of the supply and demand lists to avoid altering the originals
    supply = S[:]
    demand = D[:]
    allocations = []  # Store final allocations as [row, column, allocated_amount]

    # Continue allocating until the total supply and demand are satisfied
    while sum(supply) > 0 and sum(demand) > 0:
        row_penalties = []
        col_penalties = []

        # Calculate penalties for each row based on cost differences
        for i in range(len(supply)):
            if supply[i] > 0:  # Only calculate penalty if there is remaining supply
                # Gather available costs in this row (ignoring exhausted columns)
                row_costs = sorted([C[i][j] for j in range(len(demand)) if demand[j] > 0])

                # Calculate penalty as difference between two smallest costs, if possible
                if len(row_costs) > 1:
                    row_penalties.append((row_costs[1] - row_costs[0], i))  # Penalty = second smallest - smallest
                elif len(row_costs) == 1:
                    row_penalties.append((row_costs[0], i))  # Only one cost left; penalty is that cost itself

        # Calculate penalties for each column based on cost differences
        for j in range(len(demand)):
            if demand[j] > 0:  # Only calculate penalty if there is remaining demand
                # Gather available costs in this column (ignoring exhausted rows)
                col_costs = sorted([C[i][j] for i in range(len(supply)) if supply[i] > 0])

                # Calculate penalty as difference between two smallest costs, if possible
                if len(col_costs) > 1:
                    col_penalties.append((col_costs[1] - col_costs[0], j))  # Penalty = second smallest - smallest
                elif len(col_costs) == 1:
                    col_penalties.append((col_costs[0], j))  # Only one cost left; penalty is that cost itself

        # Determine which has the higher penalty: a row or a column
        max_row_penalty = max(row_penalties, key=lambda x: x[0]) if row_penalties else None
        max_col_penalty = max(col_penalties, key=lambda x: x[0]) if col_penalties else None

        # Compare penalties to decide whether to allocate based on a row or column
        if max_row_penalty and max_col_penalty:
            if max_row_penalty[0] >= max_col_penalty[0]:
                # Higher penalty row found; select the cell with the lowest cost in this row
                i = max_row_penalty[1]
                j = min(range(len(demand)), key=lambda x: C[i][x] if demand[x] > 0 else float('inf'))
            else:
                # Higher penalty column found; select the cell with the lowest cost in this column
                j = max_col_penalty[1]
                i = min(range(len(supply)), key=lambda x: C[x][j] if supply[x] > 0 else float('inf'))
        elif max_row_penalty:
            # Only row penalties available; allocate based on this row
            i = max_row_penalty[1]
            j = min(range(len(demand)), key=lambda x: C[i][x] if demand[x] > 0 else float('inf'))
        elif max_col_penalty:
            # Only column penalties available; allocate based on this column
            j = max_col_penalty[1]
            i = min(range(len(supply)), key=lambda x: C[x][j] if supply[x] > 0 else float('inf'))
        else:
            continue

        # Allocate as much as possible to the selected cell
        allocation_amount = min(supply[i], demand[j])
        allocations.append([j + 1, i + 1, allocation_amount])

        # Adjust remaining supply and demand
        supply[i] -= allocation_amount
        demand[j] -= allocation_amount

    return allocations

def test(n):
    name="test"+str(n)+".txt"
    S=[]
    C=[]
    D=[]
    f=open(name,'r')
    line=f.readline()
    line=line.split(' ')
    for i in line:
        S.append(int(i))
    for i in range(3):
        line=f.readline()
        line=line.split(' ')
        C.append([])
        for j in range(len(line)):
            C[i].append(int(line[j]))
    line=f.readline()
    line=line.split(' ')
    for i in line:
        D.append(int(i))
    f.close()
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
        print()
        print("VOGEL:")
        ans = vogel_alg(S, C, D)
        print_solution(ans)

for i in range(5):
    test(i+1)
