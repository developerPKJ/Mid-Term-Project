import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import webbrowser

API_KEY = "2604fb21af6eb97a4271a1048c1667d1"

# 날씨 정보 기본 클래스
class WeatherAppBase:
    def __init__(self, window, city_text, y_offset):
        self.window = window

        # 날씨 지도 링크 버튼 (공통으로 사용할 버튼)
        if not hasattr(self.window, 'map_button_added'):
            self.map_button = tk.Button(window, text="날씨 지도 보기", command=self.open_weather_map)
            self.map_button.pack(pady=5)
            self.window.map_button_added = True

        # 도시 입력
        self.city_label = tk.Label(window, text=city_text)
        self.city_label.pack(pady=(y_offset, 5))
        self.city_entry = tk.Entry(window)
        self.city_entry.pack(pady=5)

        # 검색 버튼
        self.search_button = tk.Button(window, text="날씨 확인", command=self.show_weather)
        self.search_button.pack(pady=5)

        # 결과 출력
        self.weather_result = tk.StringVar()
        self.result_label = tk.Label(window, textvariable=self.weather_result, justify="center")
        self.result_label.pack(pady=10)

        # 이미지 출력
        self.weather_image_label = tk.Label(window)
        self.weather_image_label.pack(pady=5)

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

    # 날씨 정보를 보여주는 함수(다형성 구현 부분)
    def show_weather(self):
        raise NotImplementedError("이것은 추상메소드입니다.")

    # 날씨 지도 링크 열기 함수
    def open_weather_map(self):
        url = "https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat=37.3994&lon=126.9843&zoom=5"
        webbrowser.open(url)

# WeatherAppBase를 상속받는 클래스
class WeatherApp(WeatherAppBase):
    def show_weather(self):  # 오버라이딩
        city_name = self.city_entry.get()

        if not city_name:
            messagebox.showwarning("Error", "도시 이름을 입력하세요")
            return

        # 도시 날씨 정보 가져오기
        weather_data = self.get_weather(city_name)
        if weather_data and weather_data["cod"] == 200:  # 200 = 정상 상태 코드
            main_weather = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            icon_code = weather_data["weather"][0]["icon"]
            self.weather_result.set(f'도시: {city_name}\n날씨: {main_weather}\n온도: {temperature}°C\n체감 온도: {feels_like}°C\n습도: {humidity}%\n바람 세기: {wind_speed}m/s')

            # 날씨 아이콘 가져오기
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            try:
                icon_response = requests.get(icon_url)
                icon_response.raise_for_status()
                icon_image = Image.open(io.BytesIO(icon_response.content))
                icon_photo = ImageTk.PhotoImage(icon_image)  # TK 이미지 사용 위한 변환
                self.weather_image_label.config(image=icon_photo)
                self.weather_image_label.image = icon_photo
            except requests.exceptions.RequestException as e:
                self.weather_image_label.config(image='')
                self.weather_result.set("날씨 아이콘을 가져올 수 없습니다")
        else:
            self.weather_result.set("날씨 정보를 가져올 수 없습니다")
            self.weather_image_label.config(image='')

# Tkinter GUI 실행
if __name__ == "__main__":
    root = tk.Tk()
    root.title("날씨 정보 앱")
    root.geometry("300x720")

    # 첫 번째 도시 날씨 정보 객체 생성
    app1 = WeatherApp(root, "첫 번째 도시 이름을 입력하세요:", 5)

    # 두 번째 도시 날씨 정보 객체 생성
    app2 = WeatherApp(root, "두 번째 도시 이름을 입력하세요:", 15)

    root.mainloop()
