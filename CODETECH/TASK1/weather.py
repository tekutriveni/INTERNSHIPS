#weather app
import tkinter as tk
from tkinter import messagebox
import requests
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline
import numpy as np

# API Key
API_KEY = '1b81fec5d9e4f964c749a2709fded546'

# Main function to fetch and display weather
def fetch_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or 'list' not in data:
        messagebox.showerror("Error", f"Could not fetch data: {data.get('message', 'Unknown error')}")
        return

    # Data extraction
    dates = []
    temps = []
    humidity = []
    wind_speed = []

    for forecast in data['list']:
        dt = datetime.datetime.fromtimestamp(forecast['dt'])
        dates.append(dt.strftime('%Y-%m-%d'))  # Date only
        temps.append(forecast['main']['temp'])
        humidity.append(forecast['main']['humidity'])
        wind_speed.append(forecast['wind']['speed'])

    # Convert dates to numeric x-axis
    x = np.arange(len(dates))

    # Function to smooth line
    def smooth_line(x, y):
        if len(x) < 4:
            return x, y
        x_new = np.linspace(x.min(), x.max(), 300)
        spline = make_interp_spline(x, y, k=3)
        y_smooth = spline(x_new)
        return x_new, y_smooth

    # Clear previous plots
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Create figure and subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 9), dpi=100)
    fig.subplots_adjust(hspace=0.6)

    # Styling
    font_title = {'fontsize': 14, 'fontweight': 'bold', 'color': 'darkblue'}
    font_label = {'fontsize': 12, 'fontweight': 'bold'}

    # Temperature Plot
    x_smooth, temp_smooth = smooth_line(x, temps)
    axs[0].plot(x_smooth, temp_smooth, color='red')
    axs[0].set_title(f'Temperature Forecast for {city}', **font_title)
    axs[0].set_ylabel('°C', **font_label)
    axs[0].set_xticks(x[::4])
    axs[0].set_xticklabels(dates[::4], rotation=45, ha='right', fontsize=9)

    # Humidity Plot
    x_smooth, hum_smooth = smooth_line(x, humidity)
    axs[1].plot(x_smooth, hum_smooth, color='blue')
    axs[1].set_title('Humidity Forecast', **font_title)
    axs[1].set_ylabel('%', **font_label)
    axs[1].set_xticks(x[::4])
    axs[1].set_xticklabels(dates[::4], rotation=45, ha='right', fontsize=9)

    # Wind Speed Plot
    x_smooth, wind_smooth = smooth_line(x, wind_speed)
    axs[2].plot(x_smooth, wind_smooth, color='green')
    axs[2].set_title('Wind Speed Forecast', **font_title)
    axs[2].set_ylabel('m/s', **font_label)
    axs[2].set_xlabel('Date', **font_label)
    axs[2].set_xticks(x[::4])
    axs[2].set_xticklabels(dates[::4], rotation=45, ha='right', fontsize=9)

    # Embed the plot in the GUI
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# GUI Setup
root = tk.Tk()
root.title("Smooth Weather Forecast App")
root.geometry("1000x750")

# Input field
city_entry = tk.Entry(root, font=("Arial", 14), width=30)
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")

# Button
get_weather_btn = tk.Button(root, text="Get Forecast", command=fetch_weather, font=("Arial", 12))
get_weather_btn.pack(pady=5)

# Frame for plots
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Run the app
root.mainloop()