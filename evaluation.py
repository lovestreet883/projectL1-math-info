 # Fonction d’évaluation des positions
def evaluate_board(board):
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000,
        '.': 0
    }
    total = 0
    for row in board:
        for piece in row:
            total += piece_values[piece]
    return total