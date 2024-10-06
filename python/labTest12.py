import random

sunny = random.randrange(2)
time = random.randrange(1,24)

print(sunny, time)

if sunny == 1 and 6<=time<=9:
    print('ring')
else:
    print('not ring')