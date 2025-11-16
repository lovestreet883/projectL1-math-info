# Gestion du plateau et des règles (version de base, sans roque/promotion/en-passant)
from copy import deepcopy

# Vide = "."
# Pièces blanches : "P", "R", "N", "B", "Q", "K"
# Pièces noires :   "p", "r", "n", "b", "q", "k"

board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]
def is_game_over(b, player):
    """Retourne True si le joueur n’a plus de roi ou aucun coup possible."""
    king_symbol = "K" if player == "white" else "k"

    #  vérifier si le roi est encore sur le plateau
    king_found = any(king_symbol in row for row in b)
    if not king_found:
        return True  # roi capturé => partie finie

    #  vérifier s’il reste des coups possibles
    moves = get_all_moves(b, player)
    if len(moves) == 0:
        return True

    return False



def print_board(b):
    for row in b:
        print(" ".join(row))
    print()

def make_move(b, move):

    ##Retourne une NOUVELLE copie du plateau après application du move (x1,y1,x2,y2).

    x1, y1, x2, y2 = move
    new_board = deepcopy(b)
    new_board[x2][y2] = new_board[x1][y1]
    new_board[x1][y1] = "."
    return new_board

# Helper pour mouvements glissants (tour, fou, reine)
def generate_sliding_moves(b, x, y, piece, directions):
    moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            target = b[nx][ny]
            if target == ".":
                moves.append((x, y, nx, ny))
            else:
                # si cible adversaire -> capture possible puis stop
                if target.isupper() != piece.isupper():
                    moves.append((x, y, nx, ny))
                break
            nx += dx
            ny += dy
    return moves

def get_moves_for_piece(b, x, y):
    ##NB: Ne vérifie pas si le roi est mis en échec — ajoute la logique plus tard.

    if not (0 <= x < 8 and 0 <= y < 8):
        return []
    piece = b[x][y]
    if piece == ".":
        return []

    moves = []
    is_white = piece.isupper()

    if piece.lower() == "p":  # pion
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1

        # avance simple
        nx, ny = x + direction, y
        if 0 <= nx < 8 and b[nx][ny] == ".":
            moves.append((x, y, nx, ny))
            # double pas
            nx2 = x + 2*direction
            if x == start_row and 0 <= nx2 < 8 and b[nx2][y] == ".":
                moves.append((x, y, nx2, y))

        # captures
        for dy in (-1, 1):
            cx, cy = x + direction, y + dy
            if 0 <= cx < 8 and 0 <= cy < 8:
                target = b[cx][cy]
                if target != "." and target.isupper() != is_white:
                    moves.append((x, y, cx, cy))

    elif piece.lower() == "n":  # cavalier
        deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for dx, dy in deltas:
            nx, ny = x+dx, y+dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = b[nx][ny]
                if target == "." or target.isupper() != is_white:
                    moves.append((x,y,nx,ny))

    elif piece.lower() == "k":  # roi (simple)
        deltas = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dx, dy in deltas:
            nx, ny = x+dx, y+dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = b[nx][ny]
                if target == "." or target.isupper() != is_white:
                    moves.append((x,y,nx,ny))
        # roque non géré ici (optionnel)

    elif piece.lower() == "r":  # tour
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        moves.extend(generate_sliding_moves(b, x, y, piece, directions))

    elif piece.lower() == "b":  # fou
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        moves.extend(generate_sliding_moves(b, x, y, piece, directions))

    elif piece.lower() == "q":  # reine
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        moves.extend(generate_sliding_moves(b, x, y, piece, directions))

    return moves

def get_all_moves(b, player):

    moves = []
    for x in range(8):
        for y in range(8):
            piece = b[x][y]
            if piece == ".":
                continue
            if player == "white" and piece.isupper():
                moves.extend(get_moves_for_piece(b, x, y))
            elif player == "black" and piece.islower():
                moves.extend(get_moves_for_piece(b, x, y))
    return moves
