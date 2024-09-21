avg_distance = 149597870.70
light_speed = 299792.458

total_sec = avg_distance / light_speed
min = int(total_sec // 60)
hour = int(min // 60)
sec = total_sec % 60

print(f'태양과 지구 사이의 평균 거리는 약 {avg_distance:.2f}킬로미터입니다.\n태양에서 지구까지 빛이 도달하는 시간은 약 {hour}시간 {min}분 {sec:.2f}초입니다.')