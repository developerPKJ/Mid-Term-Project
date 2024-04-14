from queue import Queue
import time
import threading
import random

# 프로세스 클래스 정의
class Process:
    def __init__(self, name, burst_time):
        self.pid = random.randint(1000, 9999)  # PID를 랜덤하게 생성
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.finished = False
        self.status = "대기"  # 초기 상태는 대기

    def work(self, quantum):
        if self.status != "실행":  # 프로세스 실행 상태로 변경
            self.status = "실행"
            print(f"Process {self.pid} ({self.name}) is running.")
        actual_work_time = min(self.remaining_time, quantum)
        time.sleep(actual_work_time)
        self.remaining_time -= actual_work_time
        if self.remaining_time <= 0:
            self.finished = True
            self.status = "종료"
            print(f"Process {self.pid} ({self.name}) has finished.")
        else:
            self.status = "대기"  # 작업이 끝나면 다시 대기 상태로
            print(f"Process {self.pid} ({self.name}) is waiting.")
        
            
def add_process_dynamically(process_queue):
    while True:
        user_input = input("Add new process (Format: Name BurstTime) or type 'exit': \n")
        if user_input.lower() == 'exit':
            break
        name, burst_time = user_input.split()
        burst_time = int(burst_time)
        new_process = Process(name, burst_time)
        process_queue.put(new_process)
        print(f"Added new process {name} with burst time {burst_time}.")


# 라운드 로빈 스케줄링 함수 정의
def round_robin(time_quantum, process_queue):
    # 모든 프로세스가 완료될 때까지 반복
    while not process_queue.empty():
        current_process = process_queue.get()
        current_process.work(time_quantum)

        # 프로세스가 아직 완료되지 않았다면 다시 큐에 추가
        if not current_process.finished:
            process_queue.put(current_process)
            

# 메인 함수 정의
def main():
    # 예시 데이터로 초기화
    initial_process_list = [
        Process('I/O', 5),               # 입출력 작업
        Process('Calculation', 10),      # 계산 작업
        Process('Image Creation', 15),   # 이미지 생성 작업
        Process('Reading', 20)           # 글자 읽는 작업
    ]

    time_quantum = 1  # 타임 퀀텀 설정
    process_queue = Queue()  # 프로세스 큐 생성
    for process in initial_process_list:
        process_queue.put(process)

    # 새로운 프로세스 추가를 위한 별도의 스레드 시작
    add_process_thread = threading.Thread(target=add_process_dynamically, args=(process_queue,))
    add_process_thread.start()

    # 라운드 로빈 스케줄링을 위한 별도의 스레드 시작
    rr_thread = threading.Thread(target=round_robin, args=(time_quantum, process_queue))
    rr_thread.start()

    # 두 스레드가 완료될 때까지 기다립니다.
    rr_thread.join()
    add_process_thread.join()


# 프로그램의 진입점
if __name__ == "__main__":
    main()  # 메인 함수 호출
    print("all process finished")