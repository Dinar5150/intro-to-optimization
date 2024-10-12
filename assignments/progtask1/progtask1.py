# INPUT PROCESSOR BLOCK
# while True: # Read a matrix until the epsilon is given
#    inputVector = list(map(float, input().split()))
#    A.append(inputVector)
#    if len(inputVector) <= 1 and len(A) > 2: # "> 2" is here to make sure we don't confuse b with eps
#        if len(inputVector) == 1: eps = A.pop()[0]
#        else: A.pop()
#
#        b = A.pop()
#        break

EPS_DEF = 0.01

# Function to print the initial problem
def print_problem(C, A, b, is_max_problem):
    # Target function line
    print(f"{"max" if is_max_problem else "min"} z = ", end = "")  # Target function line
    print(f"{C[0]} * x1", end = "")
    for i in range(1, len(C)):
        print(f" {"+" if C[i] >= 0 else "-"} {abs(C[i])} * x{i + 1}", end = "")

    print("\nsubject to the constraints:", end = "")  # Constraints lines
    for i in range(len(A)):
        print(f"\n  {A[i][0]} * x1", end = "")
        for j in range(1, len(A[i])):
            print(f" {"+" if A[i][j] >= 0 else "-"} {abs(A[i][j])} * x{j + 1}", end = "")
        print(f" <= {b[i]}", end = "")
    print("\n", end = "")


# Function to form a table
def form_tableau(C, A, b, is_max_problem):
    if is_max_problem:
        tableau = [[-i for i in C]]
    else:
        tableau = [C[:]] # Copy C into tableau in order to avoid modifications to C

    for i in range(len(A) + 1):
        tableau[0].append(0.0)

    for i in range(len(A)):
        tableau.append(A[i][:]) # Copy A into tableau in order to avoid modifications to A
        for j in range(len(C), len(C) + len(A)):
            if j == len(A[0]) + i:
                tableau[i + 1].append(1.0)
            else:
                tableau[i+1].append(0.0)
        tableau[i+1].append(b[i])

    return tableau

# Check the data on dimension correctness
def check_correctness():
    if len(A) != len(b): return False
    for i in A:
        if len(i) != len(C): return False

    for i in b:
        if i < 0: return False

    return True

def find_ind_of_min_neg(arr):
    min_ind = 0
    for i in range(len(arr)):
        if arr[i] < arr[min_ind]: min_ind = i
    if arr[min_ind] < 0: return min_ind
    else: return -1

def ratios(tableau, ind):
    min_value = float('inf')
    out = 0
    for i in range(1,len(tableau)):
        if tableau[i][ind] <= 0: continue
        x=tableau[i][-1]/tableau[i][ind]
        if 0 < x < min_value:
            out = i
            min_value = x
    return out

def iterate(tableau, en, out):
    for i in range(len(tableau)):
        if i == out: continue
        k = tableau[i][en] / tableau[out][en]
        for j in range(len(tableau[i])):
            tableau[i][j] = tableau[i][j] - k * tableau[out][j]
    k = tableau[out][en]
    for i in range(len(tableau[out])):
        tableau[out][i] = tableau[out][i] / k

def simplex(is_max_problem, C, A, b, eps = EPS_DEF):
    # Print the initial problem
    print_problem(C, A, b, is_max_problem)

    if not check_correctness():
        print("Method not applicable!")
        return

    # Form the tableau for the simplex method
    tableau = form_tableau(C, A, b, is_max_problem)
    ans = [0] * len(C)

    # prev_value = float('inf')  # Initialize previous optimal value as infinity (needed for the eps check block bellow)

    # Apply the simplex method
    entering_ind = find_ind_of_min_neg(tableau[0])
    print("solver_state: ", end = "")
    while entering_ind != -1:
        out = ratios(tableau, entering_ind)
        if out in ans:
            for i in range(len(ans)):
                if ans[i] == out:
                    ans[i] = 0
                    break
        if 0 <= entering_ind < len(C): ans[entering_ind] = out

        if out == 0:
            print("unbounded")
            return
        else:
            iterate(tableau, entering_ind, out)

        entering_ind = find_ind_of_min_neg(tableau[0])

        # BLOCK TO CHECK THE EPS BETWEEN ITERATIONS AND BREAK IF NEEDED (DEGENERACY CHECK)

        # # Check the difference in the objective function value
        # current_value = tableau[0][-1]
        # if abs(current_value - prev_value) < eps:
        #     break # Stop the iteration if difference is below eps
        #
        # prev_value = current_value  # Update for next iteration

    if not is_max_problem: tableau[0][-1] = -tableau[0][-1]

    # Print the answer
    for i in range(len(ans)):
        if ans[i] > 0:
            ans[i] = tableau[ans[i]][-1]
    print("solved")
    print(f"x*: [{', '.join(str(round(i / eps) * eps) for i in ans)}]")
    print("z:", round(tableau[0][-1] / eps) * eps)

# first test
print("=== FIRST TEST ===")
C=[2,1]
A=[ [1,-1],
    [2,0]]
b=[8,4]
simplex(True, C, A, b) # returns list [state(string), x*(array), z(float)]

#second test
print("\n=== SECOND TEST ===")
C = [4, 1, 3, 5]
A = [[-4, 6, 5, 4],
    [-3, -2, 4, 1],
    [-8, -3, 3, 2]]
b = [20, 10, 20]
simplex(True, C, A, b)

#third test
print("\n=== THIRD TEST ===")
C = [3, 2, 5]
A = [[1, 2, 1],
    [3, 0, 2],
    [1, 4, 0]]
b = [430, 460, 420]
simplex(True, C, A, b)

# fourth test
print("\n=== FOURTH TEST ===")
C=[9,10,16]
A=[ [18,15,12],
    [6,4,8],
    [5,3,3]]
b=[360,192,180]
simplex(True, C, A, b)

# fifth test
print("\n=== FIFTH TEST ===")
C=[-2,2,-6]
A=[ [2,1,-2],
    [1,2,4],
    [1,-1,2]]
b=[24,23,10]
simplex(False, C, A, b)