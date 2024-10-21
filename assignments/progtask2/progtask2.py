import math
import numpy as np

EPS_DEF = 0.001

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

# Check the data on dimension correctness
def check_correctness(C, A, b):
    if len(A) != len(b): return False
    for i in A:
        if len(i) != len(C): return False

    for i in b:
        if i < 0: return False

    return True

def interior_point(is_max_problem, C, A, b, eps = EPS_DEF, x = None):
    if  not is_max_problem:
        C = [-i for i in C]

    # Print the initial problem
    if x is None:
        x = [1] * len(C)
    print_problem(C, A, b, is_max_problem)

    if not check_correctness(C, A, b):
        print("Method not applicable!")
        return

    # Initialize and format data to NumPy format
    for i in range(len(A)):
        s = 0
        for j in range(len(A[i])):
            s += A[i][j] * x[j]
        if b[i] - s >= 0:
            x.append(b[i] - s)
        else:
            print("The method is not applicable!")
            return

    C += [0] * len(A)
    C = np.array(C)
    A = np.array(A, float)
    A = np.hstack((A, np.eye(len(A)))) # Add identity matrix from the right to the A matrix
    x = np.array(x, float)

    print("solver_state: ", end="")

    while True:
        # This piece of code was taken from the lab example
        v = x
        D = np.diag(x)
        AA = np.dot(A, D)
        cc = np.dot(D, C)
        I = np.eye(len(C))
        F = np.dot(AA, np.transpose(AA))
        FI = np.linalg.inv(F)
        H = np.dot(np.transpose(AA), FI)
        P = np.subtract(I, np.dot(H, AA))
        cp = np.dot(P, cc)
        nu = np.absolute(np.min(cp))

        if math.isnan(nu):
            print("unbounded")
            return

        y = np.add(np.ones(len(C), float), (ALPHA / nu) * cp)
        yy = np.dot(D, y)

        x = yy

        if np.linalg.norm(np.subtract(yy, v)) < eps:
            print("solved")
            print(f"x*: [{', '.join(str(round(i / eps) * eps) for i in x[:-len(A)])}]")
            print("z:", round(np.dot(C, x) / eps) * eps)
            return

def perform_tests():
    print(f"ALPHA = {ALPHA}", end = "\n\n")
    print("=== FIRST TEST ===")
    C = [2,1]
    A = [[1,-1],
         [2,0]]
    b=[8,4]
    interior_point(True, C, A,  b)

    print("\n=== SECOND TEST ===")
    C = [4, 1, 3, 5]
    A = [[-4, 6, 5, 4],
        [-3, -2, 4, 1],
        [-8, -3, 3, 2]]
    b = [20, 10, 20]
    interior_point(True, C, A, b)

    print("\n=== THIRD TEST ===")
    C = [3, 2, 5]
    A = [[1, 2, 1],
         [3, 0, 2],
         [1, 4, 0]]
    b = [430, 460, 420]
    interior_point(True, C, A, b)

    print("\n=== FOURTH TEST ===")
    C=[9,10,16]
    A=[ [18,15,12],
        [6,4,8],
        [5,3,3]]
    b=[360,192,180]
    interior_point(True, C, A, b)

    print("\n=== FIFTH TEST ===")
    C = [-2,2,-6]
    A = [[2,1,-2],
       [1,2,4],
       [1,-1,2]]
    b = [24,23,10]
    interior_point(False, C, A, b)

ALPHA = 0.5
perform_tests()
print()
ALPHA = 0.9
perform_tests()