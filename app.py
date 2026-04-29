"""
Flask web server for the Tic-Tac-Toe AI game.

Endpoints:
    GET  /             -> serves the game UI
    POST /api/move     -> takes the current board + which algorithm to use,
                          returns the AI's chosen move and stats for both
                          algorithms so the UI can compare them.
    POST /api/reset    -> returns a fresh board (handy from the front-end).

Run locally:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

from __future__ import annotations

import os
from typing import List

from flask import Flask, jsonify, render_template, request

from ai import (
    best_move_alphabeta,
    best_move_minimax,
    check_winner,
    compare_algorithms,
)

app = Flask(__name__)


def _empty_board() -> List[str]:
    return [" "] * 9


def _validate_board(board) -> List[str]:
    if not isinstance(board, list) or len(board) != 9:
        raise ValueError("Board must be a list of 9 cells.")
    cleaned = []
    for cell in board:
        if cell not in ("X", "O", " ", ""):
            raise ValueError(f"Invalid cell value: {cell!r}")
        cleaned.append(cell if cell in ("X", "O") else " ")
    return cleaned


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/reset", methods=["POST"])
def api_reset():
    return jsonify({"board": _empty_board(), "winner": None})


@app.route("/api/move", methods=["POST"])
def api_move():
    data = request.get_json(silent=True) or {}

    try:
        board = _validate_board(data.get("board", _empty_board()))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    algorithm = (data.get("algorithm") or "alphabeta").lower()
    ai_player = data.get("ai_player", "O")
    human_player = "O" if ai_player == "X" else "X"

    # If the game is already over, just report it.
    winner = check_winner(board)
    if winner is not None:
        return jsonify({
            "board": board,
            "move": None,
            "winner": winner,
            "stats": None,
            "comparison": None,
        })

    # Run the requested algorithm to choose the move.
    if algorithm == "minimax":
        chosen = best_move_minimax(list(board), ai_player)
    else:
        chosen = best_move_alphabeta(list(board), ai_player)

    # Always run the comparison too (cheap for 3x3) so the UI can show
    # side-by-side stats for Minimax vs. Alpha-Beta on the same position.
    comparison = compare_algorithms(list(board), ai_player)

    move_index = chosen["move"]
    if move_index is not None:
        board[move_index] = ai_player

    winner = check_winner(board)

    return jsonify({
        "board": board,
        "move": move_index,
        "winner": winner,
        "ai_player": ai_player,
        "human_player": human_player,
        "stats": chosen,
        "comparison": comparison,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    # Toggle debug via FLASK_DEBUG=1; off by default so the dev server
    # doesn't fork an auto-reloader child process.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    # host=0.0.0.0 so it works both locally and inside containers.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)