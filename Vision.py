import tkinter as tk
from tkinter import messagebox, ttk, Frame, Canvas, Scrollbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import csv
import pyttsx3
import requests
from PIL import Image, ImageTk

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Sample dataset for prediction
temp_humidity_data = np.array([[30, 80], [32, 85], [28, 75], [35, 90], [40, 95]])
disease_risk = np.array([0.7, 0.8, 0.5, 0.9, 1.0])

# Train a simple regression model
model = LinearRegression()
model.fit(temp_humidity_data, disease_risk)

# GUI Setup
root = tk.Tk()
root.title("🌿 AgriGuard - Crop Disease Predictor")
root.geometry("700x600")
root.configure(bg="#e8f5e9")  # Light green background

# Dark Mode Toggle
is_dark_mode = False

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    bg_color = "#263238" if is_dark_mode else "#e8f5e9"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    root.configure(bg=bg_color)
    scrollable_frame.configure(bg=bg_color)
    for widget in scrollable_frame.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
            widget.configure(bg=bg_color, fg=text_color)

# Scrollable Main Frame
main_frame = Frame(root, bg="#e8f5e9")
main_frame.pack(fill="both", expand=True)

canvas = Canvas(main_frame, bg="#e8f5e9")
scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#ffffff", padx=20, pady=20)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Function to fetch real-time weather data
def fetch_weather():
    try:
        response = requests.get("https://wttr.in/?format=%t+%h", timeout=5)
        data = response.text.split()
        temp_entry.delete(0, tk.END)
        temp_entry.insert(0, data[0].replace("°C", ""))
        humidity_entry.delete(0, tk.END)
        humidity_entry.insert(0, data[1].replace("%", ""))
    except Exception:
        messagebox.showerror("Error", "Could not fetch live data. Check your internet connection.")

# Function to predict disease risk
def predict_disease():
    try:
        temp = float(temp_entry.get())
        humidity = float(humidity_entry.get())
        crop = crop_var.get()

        risk = model.predict([[temp, humidity]])[0]

        if risk < 0.5:
            result = f"{crop}: 🌱 Low Risk - Healthy"
            color = "green"
        elif risk < 0.8:
            result = f"{crop}: ⚠️ Medium Risk - Possible Infection"
            color = "orange"
        else:
            result = f"{crop}: 🚨 High Risk - Immediate Action Needed!"
            color = "red"

        result_label.config(text=result, fg=color)
        engine.say(result)
        engine.runAndWait()

        with open("predictions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([crop, temp, humidity, risk])

        plot_trend(temp, humidity, risk)
    except Exception:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Function to plot trends
def plot_trend(temp, humidity, risk):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(temp_humidity_data[:, 0], disease_risk, color='blue', label='Existing Data')
    ax.scatter(temp, risk, color='red', label='Your Prediction')
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Disease Risk")
    ax.legend()
    ax.grid()

    global canvas_widget
    if 'canvas_widget' in globals():
        canvas_widget.get_tk_widget().destroy()

    canvas_widget = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(pady=10)

# Stylish Heading
tk.Label(scrollable_frame, text="🌾 AgriGuard - Crop Disease Predictor", 
         font=("Arial", 18, "bold"), fg="#2E7D32", bg="#ffffff").pack(pady=10)

# Dark Mode Toggle Button
tk.Button(scrollable_frame, text="🌙 Toggle Dark Mode", command=toggle_dark_mode,
          bg="#424242", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(pady=5)

# Crop Selection
tk.Label(scrollable_frame, text="Select Crop:", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=5)
crop_var = ttk.Combobox(scrollable_frame, values=["Wheat", "Rice", "Corn", "Barley", "Soybean"], font=("Arial", 12))
crop_var.pack()
crop_var.set("Wheat")

# Temperature Input
tk.Label(scrollable_frame, text="🌡 Temperature (°C):", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=5)
temp_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=20, relief="solid", bd=1)
temp_entry.pack()

# Humidity Input
tk.Label(scrollable_frame, text="💧 Humidity (%):", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=5)
humidity_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=20, relief="solid", bd=1)
humidity_entry.pack()

# Predict Button
predict_button = tk.Button(scrollable_frame, text="🔍 Predict Disease", command=predict_disease,
                           bg="#388E3C", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised")
predict_button.pack(pady=10)

# Live Weather Button
tk.Button(scrollable_frame, text="☁ Fetch Live Weather", command=fetch_weather, bg="#1976D2", 
          fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised").pack(pady=5)

# Result Label
result_label = tk.Label(scrollable_frame, text="", font=("Arial", 14, "bold"), bg="#ffffff", wraplength=500)
result_label.pack(pady=10)

# Run GUI
root.mainloop()
