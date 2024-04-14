from multiprocessing import Process, Queue
import multiprocessing
import time
import random
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# process의 정보 저장
class PCB:
    def __init__(self, name, burst_time):
        self.pid = random.randint(1000, 9999)
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.status = "대기"


# 동적으로 프로세스 추가
def add_process_dynamically(process_queue):
    def add_process():
        name = name_var.get()
        burst_time = burst_time_var.get()
        
        # 종료를 원하는 경우 아무것도 입력하지 않음
        if name and burst_time:
            try:
                burst_time = int(burst_time)
                new_process = PCB(name, burst_time)
                process_queue.put(new_process)
                print(f"새 프로세스 추가, 이름 : {name}, Burst time : {burst_time}")
                name_entry.delete(0, tk.END)
                burst_time_entry.delete(0, tk.END)
            
            except ValueError:
                print("유효한 시간 값 입력하시오")
                
        else:
            print("프로세스 이름과 Burst time을 입력하시오")
    
    # 프로세스 종료        
    def exit_process_addition():
        process_queue.put(None) # 종료 신호를 큐에 추가
        root.destroy()          # tkinter 창 닫기
        
        
# 프로세스 상태를 업데이트하고 그래프에 반영하는 함수
def update_process_status(process_queue, graph_queue):
    process_list = []
    while True:
        if not process_queue.empty():
            task = process_queue.get()
            if task is None:  # 종료 조건
                graph_queue.put(None)
                break
            process_list.append(task)
        
        # 프로세스 상태 업데이트 로직
        for process in process_list:
            # 프로세스 상태를 업데이트하는 로직 구현
            pass
        
        # 그래프 업데이트를 위한 상태 정보 전송
        graph_queue.put(process_list)
        time.sleep(1)  # 상태 업데이트 주기

# 그래프를 그리는 함수
def draw_graph(graph_queue):
    fig, ax = plt.subplots()
    bars = []

    def init():
        ax.clear()
        ax.set_ylim(0, 10)
        ax.set_xlim(0, 10)
        return bars
    
    def update(frame):
        ax.clear()
        if frame is None:
            plt.close(fig)
            return bars
        
        # 프로세스 상태에 따라 바 색상 업데이트
        for process in frame:
            # process 상태에 따른 바 그리기
            pass
        return bars

    ani = FuncAnimation(fig, update, init_func=init, frames=graph_queue.get, repeat=False)
    plt.show()


    # 창 이름
    root = tk.Tk()
    root.title("새 프로세스 추가")
    
    # 창 사이즈 설정
    root.geometry("300x150")

    # 이하 창에서 받은 이름, burst time 값으로 새로운 프로세스 객체 생성
    name_var = tk.StringVar()
    burst_time_var = tk.StringVar()
    
    message_label = tk.Label(root, text="즉시 종료를 원하면 Exit 버튼을 누르시오", fg="red")
    message_label.pack(pady=10)  # 메시지의 위치 조정 및 여백 추가

    tk.Label(root, text="프로세스 이름:").pack()
    name_entry = tk.Entry(root, textvariable=name_var)
    name_entry.pack()

    tk.Label(root, text="Burst time:").pack()
    burst_time_entry = tk.Entry(root, textvariable=burst_time_var)
    burst_time_entry.pack()
    
    button_frame = tk.Frame(root)
    button_frame.pack(expand=True, fill=tk.X)
    
    # 수정된 버튼 패킹 부분
    tk.Button(button_frame, text="Add", command=add_process).pack(side=tk.LEFT, padx=60)
    tk.Button(button_frame, text="Exit", command=exit_process_addition).pack(side=tk.RIGHT, padx=60)
    
    root.mainloop()


# 라운드 로빈 스케줄링 함수 정의
def round_robin(process_queue, timer_interrupt):
    process_list = []
    
    # 모든 프로세스가 완료될 때까지 반복
    while True:
        if not process_queue.empty():
            new_process = process_queue.get()
            if new_process is None:  # 종료 신호 확인
                break
            process_list.append(new_process)
        
        if process_list:
            current_process = process_list.pop(0)
            current_process.status = "실행"
            print(f"{current_process.pid} ({current_process.name}) 실행 시작.")
            actual_work_time = min(current_process.remaining_time, timer_interrupt) #남은시간 vs 타이머 인터럽트 시간 중 짧은거
            time.sleep(actual_work_time)
            current_process.remaining_time -= actual_work_time
            
            if current_process.remaining_time > 0:
                current_process.status = "대기"
                process_list.append(current_process)
                print(f"{current_process.pid} ({current_process.name}) 대기로 전환.")
            else:
                current_process.status = "종료"
                print(f"{current_process.pid} ({current_process.name}) 종료.")

def main():
    process_queue = multiprocessing.Queue()
    graph_queue = multiprocessing.Queue()
    timer_interrupt = 1     #타이머 인터럽트 값 설정

    # 예시 프로세스 데이터 설정 및 초기화
    initial_process_list = [
        PCB('I/O', 3),
        PCB('Calculation', 5),
        PCB('Image Creation', 8),
        PCB('Reading', 15)
    ]
    for process in initial_process_list:
        process_queue.put(process)

    # 프로세스 추가를 위한 별도의 프로세스 생성 및 시작
    input_process = Process(target=add_process_dynamically, args=(process_queue,))
    input_process.start()

    # 라운드 로빈 스케줄링을 위한 별도의 프로세스 생성 및 시작
    scheduling_process = Process(target=round_robin, args=(process_queue, timer_interrupt))
    scheduling_process.start()
    
    # 프로세스 상태 업데이트 프로세스
    update_process = multiprocessing.Process(target=update_process_status, args=(process_queue, graph_queue,))
    update_process.start()

    # 그래프 그리기 프로세스
    graph_process = multiprocessing.Process(target=draw_graph, args=(graph_queue,))
    graph_process.start()

    input_process.join()
    scheduling_process.join()
    update_process.join()
    graph_process.join()
    
# main 함수
if __name__ == "__main__":
    main()
    print("모든 프로세스 종료.")