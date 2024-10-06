user_list = '김철수', '홍길동', '김영희'

name = input("name : ")

if name in user_list:
    password = input('password : ')
    if password == '12345678':
        print('access')
    else:
        print('deny')
else:
    print('deny')