(function () {
    "use strict";

    const boardEl = document.getElementById("board");
    const cells = Array.from(document.querySelectorAll(".cell"));
    const statusEl = document.getElementById("status");
    const resetBtn = document.getElementById("reset");
    const algorithmEl = document.getElementById("algorithm");
    const humanSelect = document.getElementById("human-player");

    const mmNodes = document.getElementById("mm-nodes");
    const mmTime = document.getElementById("mm-time");
    const mmMove = document.getElementById("mm-move");
    const abNodes = document.getElementById("ab-nodes");
    const abTime = document.getElementById("ab-time");
    const abMove = document.getElementById("ab-move");

    const fasterEl = document.getElementById("faster");
    const speedupEl = document.getElementById("speedup");
    const nodesSavedEl = document.getElementById("nodes-saved");
    const historyBody = document.getElementById("history-body");

    const scoreHuman = document.getElementById("score-human");
    const scoreAi = document.getElementById("score-ai");
    const scoreDraw = document.getElementById("score-draw");

    const state = {
        board: Array(9).fill(" "),
        humanPlayer: "X",
        aiPlayer: "O",
        gameOver: false,
        busy: false,
        moveNumber: 0,
        score: { human: 0, ai: 0, draw: 0 },
    };

    function render() {
        cells.forEach((cell, i) => {
            const v = state.board[i];
            cell.textContent = v === " " ? "" : v;
            cell.classList.remove("x", "o");
            if (v === "X") cell.classList.add("x");
            if (v === "O") cell.classList.add("o");
            cell.disabled = state.busy || state.gameOver || v !== " ";
        });
    }

    function setStatus(text, mood) {
        statusEl.textContent = text;
        statusEl.classList.remove("win", "lose", "draw");
        if (mood) statusEl.classList.add(mood);
    }

    function highlightWin(winner) {
        if (winner === "Draw" || !winner) return;
        const lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6],
        ];
        for (const [a,b,c] of lines) {
            if (state.board[a] === winner && state.board[b] === winner && state.board[c] === winner) {
                cells[a].classList.add("win");
                cells[b].classList.add("win");
                cells[c].classList.add("win");
                return;
            }
        }
    }

    function fmtMs(ms) {
        if (ms === undefined || ms === null) return "—";
        if (ms < 1) return ms.toFixed(3) + " ms";
        if (ms < 10) return ms.toFixed(2) + " ms";
        return ms.toFixed(1) + " ms";
    }

    function updateStats(comparison) {
        if (!comparison) {
            mmNodes.textContent = mmTime.textContent = mmMove.textContent = "—";
            abNodes.textContent = abTime.textContent = abMove.textContent = "—";
            fasterEl.textContent = speedupEl.textContent = nodesSavedEl.textContent = "—";
            return;
        }
        const mm = comparison.minimax, ab = comparison.alphabeta;
        mmNodes.textContent = mm.nodes.toLocaleString();
        mmTime.textContent = fmtMs(mm.time_ms);
        mmMove.textContent = mm.move !== null ? `#${mm.move + 1}` : "—";

        abNodes.textContent = ab.nodes.toLocaleString();
        abTime.textContent = fmtMs(ab.time_ms);
        abMove.textContent = ab.move !== null ? `#${ab.move + 1}` : "—";

        fasterEl.textContent = comparison.faster;
        speedupEl.textContent = comparison.speedup
            ? comparison.speedup.toFixed(2) + "×"
            : "—";
        nodesSavedEl.textContent =
            `${comparison.nodes_saved.toLocaleString()} (${comparison.nodes_saved_pct.toFixed(1)}%)`;
    }

    function pushHistory(comparison) {
        if (!comparison) return;
        const empty = historyBody.querySelector("tr.empty");
        if (empty) empty.remove();

        state.moveNumber += 1;
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${state.moveNumber}</td>
            <td>${comparison.minimax.nodes.toLocaleString()} / ${fmtMs(comparison.minimax.time_ms)}</td>
            <td>${comparison.alphabeta.nodes.toLocaleString()} / ${fmtMs(comparison.alphabeta.time_ms)}</td>
            <td>${comparison.nodes_saved.toLocaleString()} (${comparison.nodes_saved_pct.toFixed(0)}%)</td>
        `;
        historyBody.prepend(tr);
    }

    function checkWinnerLocal(board) {
        const lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6],
        ];
        for (const [a,b,c] of lines) {
            if (board[a] !== " " && board[a] === board[b] && board[a] === board[c]) {
                return board[a];
            }
        }
        if (!board.includes(" ")) return "Draw";
        return null;
    }

    function endGame(winner) {
        state.gameOver = true;
        if (winner === state.humanPlayer) {
            setStatus("You win! (impossible — but congrats!)", "win");
            state.score.human += 1;
        } else if (winner === state.aiPlayer) {
            setStatus("AI wins. Try again.", "lose");
            state.score.ai += 1;
        } else {
            setStatus("Draw.", "draw");
            state.score.draw += 1;
        }
        scoreHuman.textContent = state.score.human;
        scoreAi.textContent = state.score.ai;
        scoreDraw.textContent = state.score.draw;
        highlightWin(winner);
        render();
    }

    async function aiMove() {
        if (state.gameOver) return;
        state.busy = true;
        setStatus("AI is thinking…");
        render();

        try {
            const res = await fetch("/api/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    board: state.board,
                    algorithm: algorithmEl.value,
                    ai_player: state.aiPlayer,
                }),
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Server error");

            state.board = data.board;
            updateStats(data.comparison);
            pushHistory(data.comparison);

            if (data.move !== null && data.move !== undefined) {
                cells[data.move].classList.add("placed");
                setTimeout(() => cells[data.move].classList.remove("placed"), 200);
            }

            if (data.winner) {
                endGame(data.winner);
            } else {
                setStatus(`Your turn — place an ${state.humanPlayer}.`);
            }
        } catch (err) {
            setStatus("Error: " + err.message, "lose");
        } finally {
            state.busy = false;
            render();
        }
    }

    function handleCellClick(e) {
        if (state.gameOver || state.busy) return;
        // Capture the cell reference now — `e.currentTarget` is nulled out
        // by the browser once the synchronous handler returns, so we can't
        // safely use it inside setTimeout/async callbacks below.
        const cell = e.currentTarget;
        const idx = Number(cell.dataset.index);
        if (state.board[idx] !== " ") return;

        state.board[idx] = state.humanPlayer;
        cell.classList.add("placed");
        setTimeout(() => cell.classList.remove("placed"), 200);
        render();

        const winner = checkWinnerLocal(state.board);
        if (winner) {
            endGame(winner);
            return;
        }
        aiMove();
    }

    async function newGame() {
        state.board = Array(9).fill(" ");
        state.gameOver = false;
        state.busy = false;
        state.humanPlayer = humanSelect.value;
        state.aiPlayer = state.humanPlayer === "X" ? "O" : "X";
        state.moveNumber = 0;
        cells.forEach(c => c.classList.remove("win", "placed"));
        historyBody.innerHTML = '<tr class="empty"><td colspan="4">No AI moves yet.</td></tr>';
        updateStats(null);
        setStatus(`Your turn — place an ${state.humanPlayer}.`);
        render();

        // If AI plays first (human chose O), let it move.
        if (state.aiPlayer === "X") {
            await aiMove();
        }
    }

    cells.forEach(cell => cell.addEventListener("click", handleCellClick));
    resetBtn.addEventListener("click", newGame);
    humanSelect.addEventListener("change", newGame);

    newGame();
})();
