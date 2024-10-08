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
def print_problem(C,A,b,flag):
    # Target function line
    print("z = ",end="")
    print(f"{C[0]} * x1", end="")
    for i in range(1, len(C)):
        print(f" {"+" if C[i] >= 0 else "-"} {abs(C[i])} * x{i+1}", end="")
    print(f"->{"max" if flag else "min"}",end="\n")

    print("subject to the constraints:", end="") # Constraints lines
    for i in range(len(A)):
        print(f"\n\t{A[i][0]} * x1", end="")
        for j in range(1, len(A[i])):
            print(f" {"+" if A[i][j] >= 0 else "-"} {abs(A[i][j])} * x{j+1}", end="")

        print(f" <= {b[i]}", end="")
    print("\n")

# Function to form a table
def form_tableau(C,A,b,flag):
    if flag:
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
    for i in range(len(list)):
        if list[i]<list[min]: min = i
    if list[min]<0: return min
    else: return -1

def relations(tableau, ind):
    min=100000
    out=0
    for i in range(1,len(tableau)):
        if tableau[i][ind]<=0: continue
        x=tableau[i][-1]/tableau[i][ind]
        if 0<x<min: 
            out=i
            min=x
    return out

def iterate(tableau, en, out):
    for i in range(len(tableau)):
        if i==out:continue
        k=tableau[i][en]/tableau[out][en]
        for j in range(len(tableau[i])):
            tableau[i][j]=tableau[i][j]-k*tableau[out][j]

def simplex(C,A,b,eps,flag):
    # printing problem
    print_problem(C,A,b,flag)

    # forming tableu
    tableau=form_tableau(C,A,b,flag)

    # applying simplex
    en = minimal(tableau[0])
    while en!=-1:
        out = relations(tableau,en)
        if out==0:
            print("Unboundness!\nSimplex is not applicable\n")
            return ["unbounded",[],[]]
        else:
            iterate(tableau, en, out)

        en = minimal(tableau[0])
    if flag==False: tableau[0][-1]=-1*tableau[0][-1]
    return ['solved',tableau[0][0:len(C):],tableau[0][-1]]

eps_def = 0.001 # Default epsilon value

# first test
print("first test")
C=[3,9]
A=[ [1,4],
    [1,2]]
b=[8,4]
print(simplex(C,A,b,eps_def,True))

# second test
print("\nsecond test")
C=[2,4]
A=[ [1,2],
    [1,1]]
b=[5,4]
print(simplex(C,A,b,eps_def,True))

# third test
print("\nthird test")
C=[2,1]
A=[ [1,-1],
    [2,0]]
print(simplex(C,A,b,eps_def,True))
b=[8,4]

# fourth test
print("\nfourth test")
C=[9,10,16]
A=[ [18,15,12],
    [6,4,8],
    [5,3,3]]
b=[360,192,180]
print(simplex(C,A,b,eps_def,True))

# fifth test
print("\nfifth test")
C=[-2,2,-6]
A=[ [2,1,-2],
    [1,2,4],
    [1,-1,2]]
b=[24,23,10]
print(simplex(C,A,b,eps_def,False))
