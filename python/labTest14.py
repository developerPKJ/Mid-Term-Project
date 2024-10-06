import random

quality = random.choice([True, False])

if quality:
    price = random.randrange(100,2000,100)
    print(quality, price)
    
    if price < 1000:
        print('yes')
    else:
        print('no')
else:
    print(quality)
    print('no')