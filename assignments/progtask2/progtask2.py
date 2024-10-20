import numpy as np

EPS_DEF = 0.00001

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
    if (is_max_problem):
        alpha = ALPHA
    else:
        alpha = -ALPHA

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
            return
            # TODO method not applicable

    C += [0] * len(A)
    C = np.array(C)
    A = np.array(A, float)
    A = np.hstack((A, np.eye(len(A)))) # Add identity matrix from the right to the A matrix
    b = np.array(b, float)
    x = np.array(x, float)
    D = np.diag(x)

    c = 0

    while True:
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
        y = np.add(np.ones(len(C), float), (alpha / nu) * cp)
        yy = np.dot(D, y)
        x = yy

        print(x)
        c += 1

        if c == 5:
            break

        # At = np.dot(A, D)
        # Ct = np.dot(D, C)
        #
        # P = np.subtract(
        #     np.eye(len(C)),
        #     np.dot(
        #         np.transpose(At),
        #         np.dot(
        #             np.linalg.inv(
        #                 np.dot(
        #                     At,
        #                     np.transpose(At))),
        #             At)))
        #
        # c_p = np.dot(P, Ct)
        # nu = np.absolute(np.min(c_p))
        #
        # x_new = np.add(np.array([1] * len(c_p), float), np.dot(alpha / nu, c_p))
        # x_dif = np.linalg.norm(np.subtract(x_new, x))
        #
        # x = x_new

        # print(x)

        # if x_dif < EPS_DEF:
        #     print(x)
        #     return

def perform_tests():
    C = [9, 10, 16]
    A = [
        [18, 15, 12],
        [6, 4, 8],
        [5, 3, 3]
    ]
    b = [360, 192, 180]

    interior_point(True, C, A, b)

    # # first test
    # print("=== FIRST TEST ===")
    # C = [2,1]
    # A = [[1,-1],
    #      [2,0]]
    # b=[8,4]
    # interior_point(True, C, A,  b) # returns list [state(string), x*(array), z(float)]
    #
    # #second test
    # print("\n=== SECOND TEST ===")
    # C = [4, 1, 3, 5]
    # A = [[-4, 6, 5, 4],
    #     [-3, -2, 4, 1],
    #     [-8, -3, 3, 2]]
    # b = [20, 10, 20]
    # interior_point(True, C, A, b)
    #
    # #third test
    # print("\n=== THIRD TEST ===")
    # C = [3, 2, 5]
    # A = [[1, 2, 1],
    #      [3, 0, 2],
    #      [1, 4, 0]]
    # b = [430, 460, 420]
    # interior_point(True, C, A, b)
    #
    # # fourth test
    # print("\n=== FOURTH TEST ===")
    # C=[9,10,16]
    # A=[ [18,15,12],
    #     [6,4,8],
    #     [5,3,3]]
    # b=[360,192,180]
    # interior_point(True, C, A, b)
    #
    # # fifth test
    # print("\n=== FIFTH TEST ===")
    # C = [-2,2,-6]
    # A = [[2,1,-2],
    #    [1,2,4],
    #    [1,-1,2]]
    # b = [24,23,10]
    # interior_point(False, C, A, b)

ALPHA = 0.5
perform_tests()

ALPHA = 0.9
perform_tests()

