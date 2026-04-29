def best_move_minimax(board: List[str], player: str) -> dict:
    opponent = "O" if player == "X" else "X"
    best_score = float('-inf')
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = player
            score = minimax(board, False, player, opponent)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    return {"move": best_move, "score": best_score}


def minimax(board: List[str], is_maximizing: bool, player: str, opponent: str) -> int:
    winner = check_winner(board)
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif " " not in board:
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = minimax(board, False, player, opponent)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = opponent
                score = minimax(board, True, player, opponent)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score


def best_move_alphabeta(board: List[str], player: str) -> dict:
    opponent = "O" if player == "X" else "X"
    best_score = float('-inf')
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = player
            score = alphabeta(board, float('-inf'), float('inf'), False, player, opponent)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    return {"move": best_move, "score": best_score}


def alphabeta(board: List[str], alpha: float, beta: float, is_maximizing: bool, player: str, opponent: str) -> int:
    winner = check_winner(board)
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif " " not in board:
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = alphabeta(board, alpha, beta, False, player, opponent)
                board[i] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = opponent
                score = alphabeta(board, alpha, beta, True, player, opponent)
                board[i] = " "
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score


def check_winner(board: List[str]) -> str:
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None


def compare_algorithms(board: List[str], player: str) -> dict:
    minimax_result = best_move_minimax(board, player)
    alphabeta_result = best_move_alphabeta(board, player)

    return {
        "minimax": minimax_result,
        "alphabeta": alphabeta_result
    }