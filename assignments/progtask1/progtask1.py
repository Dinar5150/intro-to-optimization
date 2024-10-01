# Input processor

C = list(map(float, input().split()))

tableMin = [C] # Initialize a table

while True: # Read a matrix til the epsilon is given
    a = list(map(float, input().split()))
    tableMin.append(a)
    if len(a) == 1:
        eps = tableMin[-1]
        tableMin.pop()
        b = tableMin[-1]
        tableMin.pop()
        break

for i in range(len(tableMin[1])-len(tableMin[0])): # Fill the first row with 0's
    tableMin[0].append(float(0))

for i in range(len(tableMin)): # Build the table
    tableMin[i].append(b[i]) # Put the right values into the table
    if len(tableMin[i]) != len(tableMin[0]):
        print("The method is not applicable!") # Check that constraints are of equal length
        exit(0)

def hasBasicVariable(table, row):
    for i in range(len(table[0])-1):
        if table[row][i] == 1:
            for j in range(len(table)):
                if j == row:
                    continue
                if table[j][i] != 0:
                    break
            else:
                return True
    return False

for i in range(1, len(tableMin)): # Check that each constraint has a basic variable
    if not hasBasicVariable(tableMin, i):
        print("The method is not applicable!")
        exit(0)

tableMax = tableMin[:]
tableMax[0] = [-i for i in tableMin[0]] # Create a table for maximization problem