user_dict = {}

while True:
    email = input('이메일 입력(q입력시 종료): ').lower()
    if email == 'q':
        break
    
    #잘못된 입력 처리
    try:
        name, domain = email.split("@")
    except ValueError:
        print('input error')
        continue
    
    #중복 저장 안함
    if domain not in user_dict:
        user_dict[domain] = set()

    user_dict[domain].add(name)
    
print(f'users 출력\n{user_dict}')