# 🎮 Tic Tac Toe (Pygame)

A simple **Tic Tac Toe game** built with **Python** and **Pygame**. It supports:

- **2-Player mode** (local multiplayer)
- **Bot mode** with 3 difficulty levels:
  - **Easy** → random moves
  - **Medium** → blocks winning moves + some strategy
  - **Hard** → unbeatable (Minimax algorithm)

---

## 📌 Requirements
- Python 3.12 or 3.13
- Pygame

Install pygame:
```bash
pip install pygame
```

---

## ▶️ How to Run
Run the game from terminal:
```bash
python tic-tac-toe.py
```

---

## 🎮 Game Modes
You can change the mode at the bottom of `tic-tac-toe.py`:

```python
# Options: main("2p") OR main("bot", "easy" / "medium" / "hard")
main("bot", "hard")
```

### Modes:
- `main("2p")` → 2 players (local)
- `main("bot", "easy")` → Play vs easy bot
- `main("bot", "medium")` → Play vs medium bot
- `main("bot", "hard")` → Play vs unbeatable bot

---

## 🖥️ Controls
- **Mouse click** on a square to place your symbol.
- Player 1 = `O` (circle)
- Player 2 / Bot = `X` (cross)

---

## 📷 Screenshots (optional)
👉 Add screenshots of gameplay here once you run it!

---

## 📜 License
This project is free to use and modify for learning purposes.
