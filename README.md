# 🌿 VedicHuman — Yog At Ease

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![MoveNet](https://img.shields.io/badge/MoveNet-Pose%20Estimation-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

> **VedicHuman is a web-based yoga platform that uses real-time pose detection to help users practice yoga and track their progress.**

## ✨ Features

- 🧘 **Real-Time Yoga Pose Detection** using TensorFlow.js and MoveNet
- 📷 **Webcam-Based Practice** directly in the browser
- 📐 **Pose Validation** using body keypoints, joint angles and positional rules
- ⏱️ **Hold-Time Tracking** for yoga poses
- 📚 **Yoga Library** with pose information and guidance
- 👤 **User Authentication** with Flask sessions
- 📊 **Progress Dashboard** with sessions, practice time and streaks
- 🔥 **Streak & Milestone Tracking**
- 💾 **SQLite Database** for users and practice history

## 🧠 How It Works

```text
Webcam
   ↓
TensorFlow.js
   ↓
MoveNet Pose Detection
   ↓
17 Body Keypoints
   ↓
Pose Validation
   ↓
Hold Timer & Feedback
   ↓
Flask Backend
   ↓
SQLite
   ↓
Progress & Streaks
```

The project uses **pre-trained MoveNet for pose estimation**. Custom JavaScript logic evaluates the detected keypoints using joint angles and relative positions to determine whether the selected yoga pose is being performed correctly.

## 🧘 Supported Poses

- 🌳 Tree Pose — Vrikshasana
- ⚔️ Warrior Pose — Virabhadrasana
- 🏔️ Mountain Pose — Tadasana
- 🙏 Namaste — Pranamasana

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Frontend** | HTML, CSS, JavaScript |
| **AI / Pose Detection** | TensorFlow.js, MoveNet |
| **Backend** | Python, Flask |
| **Database** | SQLite |
| **Web APIs** | MediaDevices API, Canvas API |

## 📂 Project Structure

```text
VedicHuman/
│
├── static/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── session.html
│   ├── library.html
│   └── progress.html
│
├── app.py
├── requirements.txt
├── Procfile
└── README.md
```

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/sakshigupta023/VedicHuman.git
cd VedicHuman
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

Allow webcam access when starting a yoga session.

## 🎯 Key Technical Highlights

- Client-side pose inference using **TensorFlow.js + MoveNet**
- Real-time webcam processing without OpenCV
- Custom geometric pose-validation logic
- Flask-based authentication and REST endpoints
- SQLite-based session and progress persistence
- Automated streak and milestone calculation

## 👥 Contributors

- Aanvi Rawat
- Natasha Pundir
- Sakshi Gupta

---

### 📜 License

Developed as an academic/in-house project.
