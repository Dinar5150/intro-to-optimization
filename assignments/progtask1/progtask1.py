#while True: # Read a matrix until the epsilon is given
#    inputVector = list(map(float, input().split()))
#    A.append(inputVector)
#    if len(inputVector) <= 1 and len(A) > 2: # "> 2" is here to make sure we don't confuse b with eps
#        if len(inputVector) == 1: eps = A.pop()[0]
#        else: A.pop()
#
#        b = A.pop()
#        break

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

# Check the data on dimension correctness
def check_dimension_correctness():
    if len(A) != len(b): return False
    for i in A:
        if len(i) != len(C): return False
    return True

def minimal(list):
    min=0
    for i in range(list):
        if list[min]<list[i]: min = i
    if list[min]<0: return min
    else: return -1

def relations(tableu, ind):
    min=100000
    indVar=0
    for i in range(len(tableu)):
        if tableu[i][ind]<0: continue
        x=tableu[i][len(tableu[i])]/tableu[i][ind]
        if 0<x<min: 
            indVar=i
            min=x
    if min==100000:
        return -1

def simplex(tableu):
    min = minimal(tableu[0])
    while min!=-1:
        ind = relations(tableu,min)

        min = minimal(tableu[0])

A = []

eps = 0.001 # Default epsilon value

