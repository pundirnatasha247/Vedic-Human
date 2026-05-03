🌿 Vedic Human – AI Powered Yoga Trainer

(In-House Project)

📌 Overview

Vedic Human is an AI-powered web application that helps users perform yoga correctly through real-time posture analysis and feedback. It integrates traditional Vedic wellness practices with modern technologies like Artificial Intelligence and Computer Vision.

The system uses pose detection models to analyze user movements via webcam and provides accuracy scores, posture correction suggestions, and performance tracking.

🎯 Objectives
Promote a healthy lifestyle through yoga
Provide real-time posture correction using AI
Make yoga training accessible and affordable
Track user performance and improvement over time
🚀 Key Features
🔐 User Authentication System (Login/Register)
🧘 Live Yoga Session using Webcam
🤖 AI Pose Detection (MoveNet / MediaPipe)
📊 Real-Time Feedback & Accuracy Score
📈 Progress Tracking & Session History
📚 Yoga Library Section (poses & guides)
💻 Responsive & User-Friendly Interface
🛠️ Tech Stack
Frontend
HTML
CSS
JavaScript
Backend
Python (Flask)
Database
SQLite / MySQL
AI / Computer Vision
OpenCV
MediaPipe / MoveNet
Webcam Integration
🏗️ System Architecture

User → Frontend → Flask Backend → AI Model → Database → Feedback to User

📂 Updated Project Structure
VedicHuman/
│
├── app.py
│
├── templates/
│   ├── login.html 
|   ├── signup.html
│   ├── dashboard.html
│   ├── session.html
│   ├── progress.html    
│   └── library.html       
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── models/
│   └── pose_detection.py
│
├── database/
│   └── db.sqlite3
│
└── README.md
🔄 Working Flow
User logs into the system
Starts a yoga session
Webcam captures live posture
AI model analyzes pose in real time
System generates feedback & accuracy score
Data is stored for progress tracking
User can view performance in Progress Page
User can explore poses in Library Section
📊 Future Enhancements
🎤 Voice Assistant Integration
🧠 Personalized Yoga Plans (AI-based)
📱 Mobile Application
☁️ Cloud-based Analytics
⌚ Wearable Device Integration
👩‍💻 Developed By
Natasha Pundir
Aanvi Rawat
Sakshi
📜 License

This project is for educational purposes only.

🙌 Acknowledgements
OpenCV
MediaPipe
Flask Framework
