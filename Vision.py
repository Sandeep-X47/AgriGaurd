import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import csv
import pyttsx3
import requests
from PIL import Image, ImageTk
import cv2
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions, MobileNetV2

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load pre-trained image model
image_model = MobileNetV2(weights="imagenet")

# Sample dataset for prediction
temp_humidity_data = np.array([[30, 80], [32, 85], [28, 75], [35, 90], [40, 95]])
disease_risk = np.array([0.7, 0.8, 0.5, 0.9, 1.0])

# Train a simple regression model
model = LinearRegression()
model.fit(temp_humidity_data, disease_risk)

# Crop-specific risk adjustment factors and solutions
crop_risk_factors = {
    "Wheat": {"factor": 0.9, "low": 0.4, "medium": 0.7},
    "Rice": {"factor": 1.2, "low": 0.5, "medium": 0.75},
    "Corn": {"factor": 0.7, "low": 0.3, "medium": 0.6},
    "Barley": {"factor": 1.0, "low": 0.45, "medium": 0.72},
    "Soybean": {"factor": 1.1, "low": 0.48, "medium": 0.74},
}

symptom_options = ["None", "Yellow Leaves", "Wilted Plant", "Fungal Spots", "Black Rot", "Stunted Growth"]

# Fetch weather data
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

# Predict disease risk
def predict_disease():
    try:
        temp = float(temp_entry.get())
        humidity = float(humidity_entry.get())
        crop = crop_var.get()
        symptom = symptom_var.get()

        crop_data = crop_risk_factors.get(crop, {"factor": 1.0, "low": 0.5, "medium": 0.75})
        risk = model.predict(np.array([[temp, humidity]]))[0] * crop_data["factor"]

        if risk < crop_data["low"]:
            result = f"{crop}: 🌱 Low Risk - Healthy"
            color = "green"
            solution_text = "Ensure regular watering and basic care."
        elif risk < crop_data["medium"]:
            result = f"{crop}: ⚠ Medium Risk - Possible Infection"
            color = "orange"
            solution_text = "Use organic manure or fertilizers to boost plant health."
        else:
            result = f"{crop}: 🚨 High Risk - Immediate Action Needed!"
            color = "red"
            solution_text = "Apply appropriate pesticides or fungicides."

        result_label.config(text=result, fg=color)
        engine.say(result)
        engine.runAndWait()

        with open("predictions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([crop, symptom, temp, humidity, risk, solution_text])

        plot_trend(temp, humidity, risk)
        show_solution_box(solution_text)
    except Exception as e:
        messagebox.showerror("Input Error", f"Please enter valid numerical values. Error: {e}")

# Plot trend graph in graph_frame
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

    canvas_widget = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(pady=10)

# Show solution box dynamically
def show_solution_box(solution_text):
    solution_label.pack(pady=5)
    solution_result.config(text=solution_text, wraplength=500)
    solution_result.pack(pady=5)

# Image recognition function
def recognize_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        img = cv2.imread(file_path)
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = preprocess_input(img)
        img = np.expand_dims(img, axis=0)

        preds = image_model.predict(img)
        label = decode_predictions(preds, top=1)[0][0][1]

        messagebox.showinfo("Image Recognition", f"🧠 Predicted: {label}")
        engine.say(f"This looks like {label}")
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"Could not process the image.\n{e}")

# GUI Setup
root = tk.Tk()
root.title("🌿 AgriGuard - Crop Disease Predictor")
root.state("zoomed")
root.update_idletasks()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load background image
bg_img = Image.open("Background.jpg").resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_img)

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add background image to canvas
canvas_bg = canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Add scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame = tk.Frame(canvas, bg="#000000", padx=20, pady=20)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollable_frame.bind("<Configure>", on_frame_configure)

# Create two columns: form on left, graph on right
form_frame = tk.Frame(scrollable_frame, bg="#000000")
form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

graph_frame = tk.Frame(scrollable_frame, bg="#000000")
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Form UI Elements
tk.Label(form_frame, text="🌾 AgriGuard - Crop Disease Predictor", font=("Arial", 18, "bold"), fg="#4caf50", bg="#000000").pack(pady=10)

tk.Label(form_frame, text="Select Crop:", font=("Arial", 12, "bold"), bg="#000000", fg="white").pack(pady=5)
crop_var = ttk.Combobox(form_frame, values=list(crop_risk_factors.keys()), font=("Arial", 12))
crop_var.pack(pady=5)
crop_var.set("Wheat")

tk.Label(form_frame, text="Select Symptoms:", font=("Arial", 12, "bold"), bg="#000000", fg="white").pack(pady=5)
symptom_var = ttk.Combobox(form_frame, values=symptom_options, font=("Arial", 12))
symptom_var.pack(pady=5)
symptom_var.set("None")

tk.Label(form_frame, text="🌡 Temperature (°C):", font=("Arial", 12, "bold"), bg="#000000", fg="white").pack(pady=5)
temp_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
temp_entry.pack(pady=5)

tk.Label(form_frame, text="💧 Humidity (%):", font=("Arial", 12, "bold"), bg="#000000", fg="white").pack(pady=5)
humidity_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
humidity_entry.pack(pady=5)

def on_hover(e):
    predict_btn.config(bg="#45a049")
def on_leave(e):
    predict_btn.config(bg="#4caf50")

predict_btn = tk.Button(form_frame, text="🔍 Predict Disease", command=predict_disease, bg="#4caf50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, pady=5)
predict_btn.pack(pady=10)
predict_btn.bind("<Enter>", on_hover)
predict_btn.bind("<Leave>", on_leave)

upload_btn = tk.Button(form_frame, text="🖼 Upload Leaf Image", command=recognize_image, bg="#2196f3", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, pady=5)
upload_btn.pack(pady=10)

result_label = tk.Label(form_frame, text="", font=("Arial", 14, "bold"), bg="#000000", fg="white", wraplength=500)
result_label.pack(pady=10)

solution_label = tk.Label(form_frame, text="💊 Suggested Solution:", font=("Arial", 12, "bold"), bg="#000000", fg="white")
solution_result = tk.Label(form_frame, text="", font=("Arial", 12), bg="#000000", fg="white", wraplength=500)

# Auto-fetch weather
fetch_weather()

root.mainloop()
