import requests
import tkinter as tk
from tkinter import messagebox

# OpenWeatherMap API 키
API_KEY = "2604fb21af6eb97a4271a1048c1667d1"

# 날씨 정보를 가져오는 기본 클래스
class WeatherAppBase:
    def __init__(self, master, city_label_text, y_offset):
        self.master = master

        # 도시 입력
        self.city_label = tk.Label(master, text=city_label_text)
        self.city_label.pack(pady=(y_offset, 5))
        self.city_entry = tk.Entry(master)
        self.city_entry.pack(pady=5)

        # 검색 버튼
        self.search_button = tk.Button(master, text="날씨 확인", command=self.show_weather)
        self.search_button.pack(pady=10)

        # 결과 출력
        self.weather_result = tk.StringVar()
        self.result_label = tk.Label(master, textvariable=self.weather_result, justify="left")
        self.result_label.pack(pady=10)

    # 날씨 정보를 가져오는 함수
    def get_weather(self, city_name):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric",
            "lang": "kr"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return None

    # 날씨 정보를 보여주는 함수 (추상 메서드로 설정)
    def show_weather(self):
        raise NotImplementedError("Subclasses should implement this method")

# WeatherAppBase를 상속받는 클래스
class WeatherApp(WeatherAppBase):
    def show_weather(self):
        city_name = self.city_entry.get()

        if not city_name:
            messagebox.showwarning("입력 오류", "도시 이름을 입력하세요!")
            return

        # 도시 날씨 정보 가져오기
        weather_data = self.get_weather(city_name)
        if weather_data and weather_data["cod"] == 200:
            main_weather = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            self.weather_result.set(f"도시: {city_name}\n날씨: {main_weather}\n온도: {temperature}°C\n습도: {humidity}%")
        else:
            self.weather_result.set("날씨 정보를 가져올 수 없습니다. 도시 이름을 확인하세요!")

# Tkinter GUI 실행
if __name__ == "__main__":
    root = tk.Tk()
    root.title("날씨 정보 앱")
    root.geometry("300x450")

    # 첫 번째 도시 날씨 정보 객체 생성
    app1 = WeatherApp(root, "첫 번째 도시 이름을 입력하세요:", 10)

    # 두 번째 도시 날씨 정보 객체 생성
    app2 = WeatherApp(root, "두 번째 도시 이름을 입력하세요:", 30)

    root.mainloop()
