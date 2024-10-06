price = int(input('food price : '))

tip = int(input('choice tip option 1.10\% 2.20\% 3.30\% (1/2/3) : '))

if tip == 1:
    tip = 0.1
elif tip == 2:
    tip = 0.2
elif tip == 3:
    tip = 0.3
else:
    print('wrong')
    tip = 0.2

print(price + price * tip)