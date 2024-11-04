def print_problem(S, C, D):
    print("\t|\tDestinations\t\t|Supply")
    print("Sources\t|", end="")
    for i in range(len(D)):
        print(i+1, end="\t")
    print("|\n", end="")
    print("--------|-------------------------------|----")
    for i in range(len(S)):
        print(i+1, end="\t")
        print("|", end="")
        for j in range(len(D)):
            print(C[i][j],end="\t")
        print("|", end="")
        print(S[i])
    print("--------|-------------------------------|----")
    print("Demand\t|", end="")
    for i in range(len(D)):
        print(D[i], end="\t")
    print("|\n", end="")

def check_problem(S, C, D):
    if sum(S)!=sum(D):
        print("The problem is not balanced!")
        return false
    return true
