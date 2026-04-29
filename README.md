# Tic-Tac-Toe AI — Minimax vs Alpha-Beta Pruning

An interactive **web-based Tic-Tac-Toe** game where you play against an
unbeatable AI opponent. The AI is implemented twice — once with the classic
**Minimax** algorithm and once with **Minimax + Alpha-Beta Pruning** — and the
UI shows a live comparison of the two on every move:

- ⏱️ **Execution time** — which one is faster
- 🌳 **Nodes explored** — how many game states each algorithm checked

> Inspired by the playful UI of [poki.com/tic-tac-toe](https://poki.com/en/g/tic-tac-toe-3).

---

## ✨ Features

- Clean, responsive web UI (Flask + HTML/CSS/JS — no frameworks)
- Unbeatable AI (you can win at most a draw)
- Choose which algorithm the AI uses for its moves (Minimax or Alpha-Beta)
- Choose to play first (X) or second (O)
- Live **side-by-side comparison** of Minimax vs Alpha-Beta on every move,
  including:
  - nodes explored
  - execution time
  - speed-up factor
  - nodes saved (count and %)
- Per-game **history table** of every AI move's stats
- Score tracker (You / AI / Draw)

---

## 🗂️ Project Structure

```
tic-tac-toe-ai/
├── app.py                # Flask web server (routes + JSON API)
├── ai.py                 # Minimax & Alpha-Beta implementations
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html        # Game UI
└── static/
    ├── style.css         # Styling
    └── script.js         # Front-end game logic
```

---

## 🚀 Getting Started (VS Code)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/tic-tac-toe-ai.git
cd tic-tac-toe-ai
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Now open **http://127.0.0.1:5000** in your browser and play!

---

## 🧠 How the AI Works

### Minimax

A recursive search of the entire game tree. The AI assumes both players play
optimally:

- **Maximizer** (AI): picks the move with the **highest** score
- **Minimizer** (human): picks the move with the **lowest** score

Scores at terminal states:

| Outcome  | Score |
|----------|------:|
| AI wins  |  `+10` |
| Draw     |   `0` |
| AI loses | `−10` |

Implemented in `ai.py` → `best_move_minimax()`.

### Alpha-Beta Pruning

Same Minimax search, but maintains two bounds — `alpha` (best score the
maximizer can guarantee so far) and `beta` (best score the minimizer can
guarantee so far). Whenever `alpha >= beta`, the rest of the branch can't
affect the final decision, so it is **pruned**. The result is identical to
Minimax but **far fewer nodes** are explored.

Implemented in `ai.py` → `best_move_alphabeta()`.

### Comparison

For every AI move the server runs **both** algorithms on the same board
position and returns:

```json
{
  "minimax":   { "nodes": 549946, "time_ms": 412.8, "move": 0 },
  "alphabeta": { "nodes":  18297, "time_ms":  14.1, "move": 0 },
  "speedup":   29.3,
  "nodes_saved": 531649,
  "nodes_saved_pct": 96.7,
  "faster": "Alpha-Beta"
}
```

Both algorithms always pick a move with the same optimal score, so the AI is
unbeatable either way — Alpha-Beta just gets there much faster.

---

## 🔌 API Reference

### `POST /api/move`

Request:

```json
{
  "board": [" "," "," "," "," "," "," "," "," "],
  "algorithm": "alphabeta",
  "ai_player": "O"
}
```

Response:

```json
{
  "board": [" "," "," "," ","O"," "," "," "," "],
  "move": 4,
  "winner": null,
  "stats":      { "algorithm": "Alpha-Beta", "nodes": 18297, "time_ms": 14.1, "move": 4, "score": 0 },
  "comparison": { "minimax": { ... }, "alphabeta": { ... }, "speedup": 29.3, ... }
}
```

### `POST /api/reset`

Returns an empty board.

---

## 📊 Typical Results (3×3 Tic-Tac-Toe, first move)

| Algorithm   | Nodes explored | Time          |
|-------------|----------------|---------------|
| Minimax     | ~549,000       | ~400–600 ms   |
| Alpha-Beta  | ~18,000        | ~10–25 ms     |
| **Saved**   | **~96–97%**    | **~25–30× faster** |

Numbers vary slightly by machine, but Alpha-Beta is consistently dramatically
faster on the same position because it never expands branches that can't
affect the result.

---

## 📜 License

MIT — do whatever you want with it.
