work_time = int(input("근무시간 : "))
money_by_worktime = int(input('시간당 임금 : '))

if work_time > 40:
    print(money_by_worktime * (work_time - 40) * 1.5 + money_by_worktime * 40)
else:
    print(money_by_worktime * work_time)