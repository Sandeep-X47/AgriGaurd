# 🌿 AgriGuard - Crop Disease Predictor

AgriGuard is a smart crop disease prediction tool that helps farmers and agricultural experts predict disease risks based on temperature and humidity.

## 🚀 Features
- 📊 **Predict Disease Risk** based on temperature & humidity.
- ☁ **Fetch Live Weather Data** to get real-time inputs.
- 🎨 **Image Recognition** .
- 📈 **Visualize Trends** with real-time risk analysis graphs.
- 🔊 **Text-to-Speech (TTS)** for audio alerts.
- 📂 **Save Predictions** in CSV for future reference.

## 🛠 Technologies Used
- **Frontend:** Tkinter (Python GUI)
- **Backend:** Flask
- **Machine Learning:** Scikit-Learn (Linear Regression)
- **Data Visualization:** Matplotlib
- **Live Weather API:** wttr.in
- **Text-to-Speech:** pyttsx3

## 📦 Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/YOUR_USERNAME/AgriGuard-Web.git
   cd AgriGuard-Web
   ```

2. **Create a Virtual Environment (Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On MacOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```sh
   python app.py
   ```

5. **Open in Browser**
   - Visit `http://127.0.0.1:5000/`

## 🌍 Deployment
### Deploying on Render
1. **Push your project to GitHub**
2. **Go to [Render](https://render.com/)**
3. **Create a new Web Service** & connect GitHub
4. **Set build command:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Set start command:**
   ```sh
   gunicorn app:app
   ```
6. **Deploy & Get Your Public URL**

## 🎯 Usage
- Select your **crop type** from the dropdown
- Enter **temperature** & **humidity** manually or fetch live data
- Click **Predict Disease** to analyze the risk
- View **graphical trends** and **hear the risk level** with TTS
- Save predictions for **future reference**

## 📜 License
This project is open-source and available under the MIT License.

---
👨‍💻 Made with ❤️ by Sandeep

