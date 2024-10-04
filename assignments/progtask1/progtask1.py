# Input processor

C = list(map(float, input().split()))

A = []

eps = 0.001 # Default epsilon value

while True: # Read a matrix until the epsilon is given
    inputVector = list(map(float, input().split()))
    A.append(inputVector)
    if len(inputVector) <= 1 and len(A) > 2:
        if len(inputVector) == 1: eps = A.pop()[0]
        else: A.pop()

        b = A.pop()
        break

# Print the initial problem function
def print_problem(is_max_problem):
    print(f"{"max" if is_max_problem else "min"} z = ", end="") # Target function line

    print(f"{C[0]} * x1", end="")
    for i in range(1, len(C)):
        print(f" {"+" if C[i] >= 0 else "-"} {abs(C[i])} * x{i+1}", end="")

    print("\nsubject to the constraints:", end="") # Constraints lines
    for i in range(len(A)):
        print("\n\t", end="")

        print(f"{A[i][0]} * x1", end="")
        for j in range(1, len(A[i])):
            print(f" {"+" if A[i][j] >= 0 else "-"} {abs(A[i][j])} * x{j+1}", end="")

        print(f" <= {b[i]}", end="")

print_problem(True)

# Function to form a table
def form_tableau(is_max_problem):
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

form_tableau(True)