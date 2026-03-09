# 🧩 8 Puzzle Game (Python Tkinter)

A **feature-rich 8 Puzzle Game** built with **Python and Tkinter GUI**.
This project includes an **interactive puzzle board, Manhattan distance heuristic, A* auto solver, timer, sound effects, and high score tracking**.

It is designed as a **simple AI + GUI project** demonstrating search algorithms and user interaction.


---

# 🚀 Features

✅ Interactive **3x3 puzzle board**
✅ **Move counter**
✅ **Real-time timer**
✅ **Manhattan Distance heuristic display**
✅ **A* Search Auto Solver 🤖**
✅ **Sound effects for moves and win**
✅ **High score saving system**
✅ **Restart option**
✅ Clean **Tkinter GUI interface**

---

# 🧠 Algorithm Used

### A* Search Algorithm

The puzzle solver uses the A* (A-Star) search algorithm, which finds the shortest path to the solution.

Evaluation function:

```
f(n) = g(n) + h(n)
```

Where:

* **g(n)** → Cost from start state
* **h(n)** → Manhattan Distance heuristic

---

### Manhattan Distance Heuristic

The Manhattan distance calculates how far each tile is from its goal position.

```
distance = |x1 - x2| + |y1 - y2|
```

This helps guide the search efficiently.

---

# 🖥️ Tech Stack

* **Python 3**
* **Tkinter (GUI)**
* **Heapq (Priority Queue for A*)**
* **Winsound (Sound Effects)**
* **Random**
* **OS module**

---

# 📂 Project Structure

```
8-puzzle-pro/
│
├── puzzle.py          # Main game code
├── highscore.txt      # Saved high score
└── README.md          # Project documentation
```

---

# ▶️ How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Gautamdutta-star/Eight_puzzle.git
```

### 2️⃣ Navigate to the Project Folder

```bash
cd 8puzzle
```

### 3️⃣ Run the Game

```bash
python 8puzzle.py
```

---

# 🎮 How to Play

1. Click a tile adjacent to the empty space.
2. The tile will move into the empty position.
3. Rearrange the numbers to match the goal state:

```
1 2 3
4 5 6
7 8 _
```

4. Try to solve with **minimum moves and time**.

---

# 🤖 Auto Solver

Click **"Auto Solve 🤖"** and the game will automatically solve the puzzle using the **A* algorithm**.

---

# 🏆 High Score System

The game saves the **best move count and time** inside:

```
highscore.txt
```

You can view it using the **"View High Score"** button.

---

# 🔊 Sound Effects

* Move sound when tiles move
* Winning sound when puzzle is solved

Uses **Windows Beep API (`winsound`)**.

---

# 📚 Educational Purpose

This project demonstrates:

* Artificial Intelligence Search Algorithms
* Heuristic Functions
* Python GUI Development
* Event-driven programming

Perfect for **AI / Python / Data Structures students**.

---

# 🔮 Future Improvements

* Dark mode UI
* Better puzzle themes
* Move animations
* Leaderboard system
* Mobile version using **Kivy**
* Export to **Android APK**

---

# 👨‍💻 Author

**Gautam Dutta**

B.Tech CSE | KIIT University
