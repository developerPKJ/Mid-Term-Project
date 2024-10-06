import random

seq = '쫄면', '육계장', '비빔밥'

print(random.choice(seq))




option = ['L', 'R', 'C']
com = random.choice(option)
user = random.choice(option)

print(com, user)

if com == user:
    print('수비성공')
else:
    print('수비실패')