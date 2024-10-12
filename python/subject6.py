input_num = int(input('10진수 입력: '))
num_list = []

while input_num > 0:
    num_list.append(input_num % 2)
    input_num //= 2

num_list.reverse()
print(num_list)