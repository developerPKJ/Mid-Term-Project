word = input('문자열 입력: ')

if len(word)%2 == 0:
    print(word[len(word)//2-1 : len(word)//2+1:])
else:
    print(word[len(word)//2])