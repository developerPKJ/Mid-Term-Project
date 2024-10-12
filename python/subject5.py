using_elec = int(input('전기 사용량을 입력하세요. '))
isBig = input('다자녀 가정인가요? (예 or 아니오) ')
print('=====================================================')

basic_fee = 910
fee = 99.3
total_fee = basic_fee + fee * using_elec

if isBig == '예':
    isBig = True
    total_fee = round(total_fee * 0.8)
else:
    isBig = False
    total_fee = round(total_fee)
    

print(f'사용량: {using_elec}kwh')
print(f'기본요금: {basic_fee}원')
print(f'단가: {fee}원')

if isBig:
    print(f'전기 요금(다자녀 할인 적용): {total_fee}원')
else:
    print(f'전기 요금: {total_fee}원')