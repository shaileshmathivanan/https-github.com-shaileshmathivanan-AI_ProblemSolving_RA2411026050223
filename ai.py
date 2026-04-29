"""
Tic-Tac-Toe AI engine.

Implements two algorithms for the AI opponent:
    1. Minimax (full game-tree search)
    2. Minimax with Alpha-Beta Pruning

Both algorithms always return the optimal move, so the AI is unbeatable.
The functions also report:
    - execution time (seconds)
    - number of nodes (game states) explored
so the two methods can be compared.

Board representation:
    A board is a list of 9 characters, indexed 0..8 like this:
         0 | 1 | 2
        ---+---+---
         3 | 4 | 5
        ---+---+---
         6 | 7 | 8
    Each cell is "X", "O", or " " (a single space) for empty.

By convention in this module:
    - "X" is the human player (the maximizer when AI plays X, minimizer otherwise)
    - "O" is the AI by default
The functions take an `ai_player` argument so either side can be controlled.
"""

from __future__ import annotations

import time
from typing import List, Optional, Tuple

WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
)


def check_winner(board: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if someone has won, 'Draw' if board full, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "Draw"
    return None


def available_moves(board: List[str]) -> List[int]:
    return [i for i, cell in enumerate(board) if cell == " "]


def _other(player: str) -> str:
    return "O" if player == "X" else "X"


# ---------------------------------------------------------------------------
# Minimax (no pruning)
# ---------------------------------------------------------------------------

def _minimax(board: List[str], current: str, ai_player: str, counter: List[int]) -> int:
    """Return score for `ai_player` from this position.

    +10 - depth  -> AI wins (prefer faster wins)
    -10 + depth  -> AI loses (prefer slower losses)
     0           -> draw
    `counter` is a single-element list used as a mutable counter for the
    number of nodes explored.
    """
    counter[0] += 1
    result = check_winner(board)
    if result is not None:
        if result == ai_player:
            return 10
        if result == "Draw":
            return 0
        return -10

    if current == ai_player:
        best = -float("inf")
        for move in available_moves(board):
            board[move] = current
            score = _minimax(board, _other(current), ai_player, counter)
            board[move] = " "
            if score > best:
                best = score
        return int(best)
    else:
        best = float("inf")
        for move in available_moves(board):
            board[move] = current
            score = _minimax(board, _other(current), ai_player, counter)
            board[move] = " "
            if score < best:
                best = score
        return int(best)


def best_move_minimax(board: List[str], ai_player: str = "O") -> dict:
    """Compute the AI's best move using plain Minimax.

    Returns a dict with: move, score, nodes, time_ms.
    """
    counter = [0]
    start = time.perf_counter()

    best_score = -float("inf")
    best_move: Optional[int] = None

    for move in available_moves(board):
        board[move] = ai_player
        score = _minimax(board, _other(ai_player), ai_player, counter)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return {
        "move": best_move,
        "score": int(best_score) if best_move is not None else 0,
        "nodes": counter[0],
        "time_ms": elapsed_ms,
        "algorithm": "Minimax",
    }


# ---------------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning
# ---------------------------------------------------------------------------

def _alphabeta(
    board: List[str],
    current: str,
    ai_player: str,
    alpha: float,
    beta: float,
    counter: List[int],
) -> int:
    counter[0] += 1
    result = check_winner(board)
    if result is not None:
        if result == ai_player:
            return 10
        if result == "Draw":
            return 0
        return -10

    if current == ai_player:
        value = -float("inf")
        for move in available_moves(board):
            board[move] = current
            value = max(value, _alphabeta(board, _other(current), ai_player, alpha, beta, counter))
            board[move] = " "
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cutoff
        return int(value)
    else:
        value = float("inf")
        for move in available_moves(board):
            board[move] = current
            value = min(value, _alphabeta(board, _other(current), ai_player, alpha, beta, counter))
            board[move] = " "
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cutoff
        return int(value)


def best_move_alphabeta(board: List[str], ai_player: str = "O") -> dict:
    """Compute the AI's best move using Minimax with Alpha-Beta Pruning."""
    counter = [0]
    start = time.perf_counter()

    best_score = -float("inf")
    best_move: Optional[int] = None
    alpha, beta = -float("inf"), float("inf")

    for move in available_moves(board):
        board[move] = ai_player
        score = _alphabeta(board, _other(ai_player), ai_player, alpha, beta, counter)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return {
        "move": best_move,
        "score": int(best_score) if best_move is not None else 0,
        "nodes": counter[0],
        "time_ms": elapsed_ms,
        "algorithm": "Alpha-Beta",
    }


def compare_algorithms(board: List[str], ai_player: str = "O") -> dict:
    """Run both algorithms on the same position and return a comparison."""
    mm = best_move_minimax(list(board), ai_player)
    ab = best_move_alphabeta(list(board), ai_player)

    speedup = (mm["time_ms"] / ab["time_ms"]) if ab["time_ms"] > 0 else None
    nodes_saved = mm["nodes"] - ab["nodes"]
    nodes_saved_pct = (nodes_saved / mm["nodes"] * 100.0) if mm["nodes"] else 0.0

    return {
        "minimax": mm,
        "alphabeta": ab,
        "speedup": speedup,
        "nodes_saved": nodes_saved,
        "nodes_saved_pct": nodes_saved_pct,
        "faster": "Alpha-Beta" if ab["time_ms"] < mm["time_ms"] else "Minimax",
    }
