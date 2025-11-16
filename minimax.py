# minimax.py
from evaluation import evaluate_board
import chessboard

def minimax_alpha_beta(b, depth, alpha, beta, player_is_maximizing):
    if depth == 0:
        return evaluate_board(b), None

    player_str = "white" if player_is_maximizing else "black"

    # 🔹 Stopper si le jeu est fini
    if chessboard.is_game_over(b, player_str):
        # On retourne une valeur extrême selon qui a gagné
        if player_is_maximizing:
            return -9999, None  # blanc perd (pas de coups)
        else:
            return 9999, None   # noir perd (pas de coups)

    best_move = None

    if player_is_maximizing:
        value = float('-inf')
        for move in chessboard.get_all_moves(b, player_str):
            new_b = chessboard.make_move(b, move)
            eval_val, _ = minimax_alpha_beta(new_b, depth-1, alpha, beta, False)
            if eval_val > value:
                value, best_move = eval_val, move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move

    else:
        value = float('inf')
        for move in chessboard.get_all_moves(b, player_str):
            new_b = chessboard.make_move(b, move)
            eval_val, _ = minimax_alpha_beta(new_b, depth-1, alpha, beta, True)
            if eval_val < value:
                value, best_move = eval_val, move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move
def find_best_move_for(b, player, depth=3):
    """
    Wrapper : player is 'white' or 'black'
    depth default 3 (augmenter rend beaucoup plus lent)
    """
    is_max = True if player == "white" else False
    val, move = minimax_alpha_beta(b, depth, float('-inf'), float('inf'), is_max)
    return val, move
