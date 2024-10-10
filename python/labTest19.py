isCollect = True
input_num = 0
sum = 0
factorial = 1

#입력 값이 0이거나 음수인 경우 예외 처리
while(isCollect):
    input_num = int(input('insert n : '))
    
    if input_num > 0:
        isCollect = False

#덧셈
for n in range(1, input_num+1):
    sum += n
    
print('sum :', sum)

#팩토리얼
for n in range(1, input_num+1):
    factorial *= n
    
print('factorial :', factorial)



#화씨 섭씨 변환
for i in range(0, 101, 10):
    print(i, '->', round((i-32)*5/9, 2))