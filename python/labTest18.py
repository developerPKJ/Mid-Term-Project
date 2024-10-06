weight = int(input('weight(kg) : '))
height = float(input('height(m) : '))

bmi = weight//height**2

print('bmi :', bmi)

if bmi < 18.5:
    print('저체중')
elif bmi < 23:
    print('정상')
elif bmi < 25:
    print('과체중')
elif bmi < 30:
    print('h1')
elif bmi < 40:
    print('h2')
else:
    print('too heavy')