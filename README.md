# 🎮 Tic-Tac-Toe AI

### Minimax vs Alpha-Beta Pruning

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-WebApp-green)
![AI](https://img.shields.io/badge/AI-Minimax%20Algorithm-orange)
![Status](https://img.shields.io/badge/Project-Complete-brightgreen)

🚀 **Live Demo:** https://tic-tac-toe-ai-sdvc.onrender.com
💻 **GitHub Repo:** https://github.com/shaileshmathivanan/tic-tac-toe-ai

---

## 📌 AI Lab Assignment

**Interactive Game AI – Tic-Tac-Toe System using Adversarial Search Algorithms**

---

## 🧠 Problem Description

A gaming system requires an intelligent opponent capable of making optimal decisions in a Tic-Tac-Toe game.

Traditional rule-based approaches lack strategic depth. This project implements an AI-based solution using **Minimax Algorithm** and **Alpha-Beta Pruning** to ensure optimal gameplay.

The AI evaluates all possible moves and always selects the best one, making it **unbeatable**.

---

## 🌐 System Overview

This is a **web-based Tic-Tac-Toe game** where a human player competes against an AI.

The system also provides **real-time comparison** between two algorithms:

* ⏱ Execution Time
* 🌳 Nodes Explored
* ⚡ Performance Efficiency

---

## 🏗 System Architecture

* **Game Engine (ai.py)**
  Implements Minimax and Alpha-Beta algorithms

* **Web Server (app.py)**
  Flask backend handling routes and APIs

* **Frontend (HTML, CSS, JavaScript)**
  Interactive UI for gameplay

* **Comparison Module**
  Displays algorithm performance metrics

---

## ⚙️ Algorithms Used

### 🔹 Minimax Algorithm

* Explores all possible game states
* Assumes opponent plays optimally
* Selects best move

**Evaluation Scores:**

* Win → +10
* Draw → 0
* Loss → -10

---

### 🔹 Alpha-Beta Pruning

* Optimized version of Minimax
* Skips unnecessary branches
* Faster decision making
* Same optimal result

---

## ✨ Features

* 🎯 Unbeatable AI Opponent
* 🔄 Two AI Modes (Minimax & Alpha-Beta)
* 📊 Real-Time Algorithm Comparison
* ⏱ Execution Time Measurement
* 🌳 Nodes Explored Visualization
* 🎮 Interactive Web Interface
* 🔗 API-based Backend Integration

---

## 📸 Screenshots

### 🎯 Game Interface

![Game UI](screenshots/game.png)

### 📊 Algorithm Comparison

![Stats](screenshots/stats.png)

---

## 🚀 Execution Steps

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run Application

```bash
python app.py
```

### 3️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 🌍 Live Demo

👉 [Click here to play](https://tic-tac-toe-ai-sdvc.onrender.com)

---

## 🧪 Sample Output

* AI selects optimal move
* Alpha-Beta explores fewer nodes than Minimax
* Faster execution with same result

---

## 💻 Technologies Used

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

---

## 📚 Key Learnings

* Implementation of Minimax Algorithm
* Optimization using Alpha-Beta Pruning
* Flask Web Development
* API communication between frontend and backend

---

## 🔮 Future Enhancements

* Multiplayer mode
* Improved UI/UX design
* Larger grid (4x4, 5x5)
* Machine learning-based AI

---

## 👨‍💻 Author

**Shailesh M**
GitHub: https://github.com/shaileshmathivanan

---

## 📜 License

This project is for educational purposes.
