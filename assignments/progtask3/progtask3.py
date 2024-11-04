# printing problem; S-supply array, C-cost matrix, D-demand array
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

# printing feaseble solution; ans - feaseble solution
def print_solution(ans):
    for i in ans:
        print(f"x_{i[0]},{i[1]}={i[2]}")
# checking if problem is balances, returns true; S-supply array, C-cost matrix, D-demand array
def check_problem(S, C, D):
    if sum(S)!=sum(D):
        print("The problem is not balanced!")
        return False
    return True

# applying north-west algorithm on problem, returning initial feaseble solurion in look: [row, column, amount]; S-supply array, C-cost matrix, D-demand array
def north_west_alg(S, C, D):
    ind=[0,0]
    x_0=[]
    while sum(S)>0:
        if S[ind[0]]>0 and D[ind[1]]>0:
            x=min(S[ind[0]],D[ind[1]])
            x_0.append([ind[0]+1,ind[1]+1,x])
            S[ind[0]]-=x
            D[ind[1]]-=x
        if D[ind[1]]==0:
            ind[1]+=1
        elif S[ind[0]]==0:
            ind[0]+=1
    return x_0

S=[10,20,40]
D=[5,15,30,20]
C=[[1,4,2,8],
   [9,3,7,1],
   [6,2,5,9]]
print_problem(S, C, D)
if check_problem(S, C, D):
    ans=north_west_alg(S, C, D)
    print_solution(ans)
    
