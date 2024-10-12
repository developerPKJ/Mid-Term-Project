numList = tuple(range(2, 101, 2))
n = 1

for i in numList:
    print(i, end=" ")
    
    if n % 5 == 0:
        print('\n')
        
    n += 1