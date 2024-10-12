mydict = {"cat":12, "dog":6, "elephant":23}

mydict.update({"rabbit":10, "monkey":30, "bear":3})

for key in list(mydict.keys()):
    if mydict[key] < 10:
        mydict.pop(key)
        
for key in reversed(mydict):
    print(f'{key}는 {mydict[key]}마리')