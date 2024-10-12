user_input = input('학번과 이름, 학과번호를 순서대로 입력하시오( ex. 123456홍길동01 ) : ')

department_num = user_input[-2:]
student_num = user_input[0:6]
student_name = user_input[6:-2]

print(f'학과번호: {department_num}, 학번: {student_num}, 이름: {student_name}')