// This file contains the JavaScript code for the Tic-Tac-Toe game, handling user interactions, making API calls to the Flask server, and updating the UI based on the game state.

const apiUrl = '/api/move';
const resetUrl = '/api/reset';

let board = [];
let aiPlayer = 'O';
let humanPlayer = 'X';
let currentPlayer = humanPlayer;

function initGame() {
    board = Array(9).fill(' ');
    currentPlayer = humanPlayer;
    renderBoard();
    document.getElementById('message').innerText = '';
}

function renderBoard() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.innerText = board[index];
        cell.classList.remove('highlight');
    });
}

function handleCellClick(index) {
    if (board[index] !== ' ' || currentPlayer !== humanPlayer) return;

    board[index] = humanPlayer;
    renderBoard();
    checkGameStatus();

    if (currentPlayer === humanPlayer) {
        currentPlayer = aiPlayer;
        makeAIMove();
    }
}

function makeAIMove() {
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ board, algorithm: 'alphabeta', ai_player: aiPlayer }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.move !== null) {
            board[data.move] = aiPlayer;
            renderBoard();
            checkGameStatus();
        }
    });
}

function checkGameStatus() {
    const winner = checkWinner();
    if (winner) {
        document.getElementById('message').innerText = `${winner} wins!`;
        return;
    }
    if (board.every(cell => cell !== ' ')) {
        document.getElementById('message').innerText = 'It\'s a draw!';
    } else {
        currentPlayer = currentPlayer === humanPlayer ? aiPlayer : humanPlayer;
    }
}

function checkWinner() {
    const winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
        [0, 4, 8], [2, 4, 6]             // diagonals
    ];

    for (const combination of winningCombinations) {
        const [a, b, c] = combination;
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            return board[a];
        }
    }
    return null;
}

document.getElementById('reset').addEventListener('click', initGame);
document.querySelectorAll('.cell').forEach((cell, index) => {
    cell.addEventListener('click', () => handleCellClick(index));
});

initGame();