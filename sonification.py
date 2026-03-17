import tkinter as tk
from tkinter import messagebox

def run_program():
    try:
        import requests
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from scipy.io.wavfile import write
        import sounddevice as sd

        API_KEY = "1facbeee6551f361723b2fe2aa762bc6"

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat=55.75&lon=37.62&appid={API_KEY}&units=metric&lang=ru"

        sample_rate = 44100

        response = requests.get(url)
        data = response.json()

        time = []
        temperature = []
        humidity = []
        wind = []

        for item in data["list"]:
            time.append(item["dt_txt"])
            temperature.append(item["main"]["temp"])
            humidity.append(item["main"]["humidity"])
            wind.append(item["wind"]["speed"])

        df = pd.DataFrame({
            "time": pd.to_datetime(time),
            "temperature": temperature,
            "humidity": humidity,
            "wind": wind
        })

        print(df.head())

        plt.figure(figsize=(12,6))

        plt.plot(df["time"], df["temperature"], label="Температура °C")
        plt.plot(df["time"], df["humidity"], label="Влажность %")
        plt.plot(df["time"], df["wind"], label="Ветер м/с")

        plt.title("Изменение погодных данных")
        plt.xlabel("Время")
        plt.ylabel("Значение")
        plt.legend()
        plt.grid(True)

        plt.xticks(rotation=45)

        plt.show()

        audio = np.array([])

        for i in range(len(df)):
            temp = df["temperature"][i]
            hum = df["humidity"][i]
            wind_speed = df["wind"][i]
            
            frequency = 200 + temp * 10
            volume = hum / 100
            duration = 0.3 + wind_speed / 10

            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = volume * np.sin(2 * np.pi * frequency * t)

            audio = np.concatenate((audio, wave))

        audio_int16 = np.int16(audio / np.max(np.abs(audio)) * 32767)

        write("weather_sonification.wav", sample_rate, audio_int16)

        print("Файл weather_sonification.wav сохранён")

        time_audio = np.linspace(0, len(audio)/sample_rate, len(audio))

        df_audio = pd.DataFrame({
            "time": time_audio,
            "amplitude": audio
        })

        plt.figure(figsize=(12,5))

        plt.plot(df_audio["time"], df_audio["amplitude"])

        plt.title("Визуализация сонифицированного сигнала")
        plt.xlabel("Время (сек)")
        plt.ylabel("Амплитуда")

        plt.grid(True)

        plt.show()

        messagebox.showinfo("Готово")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))



root = tk.Tk()
root.title("Сонификация погоды")
root.geometry("300x200")

label = tk.Label(root, text="Сонификация данных", font=("Arial", 14))
label.pack(pady=20)

btn = tk.Button(root, text="Запустить программу", command=run_program, bg="green", fg="white")
btn.pack(pady=20)

root.mainloop()