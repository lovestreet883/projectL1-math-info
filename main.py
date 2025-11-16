import tkinter as tk
import chessboard
import gui
import minimax
import tree_visualizer # ◀️ --- AJOUT
from PIL import Image, ImageTk, ImageFilter, ImageGrab

CELL_SIZE = 60
selected = None
legal_moves_for_selected = []
current_player = "white"
game_over = False

root = tk.Tk()
root.title("Chess.AI (Projet Arbres - L1 Miashs)")
canvas = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE)
canvas.pack()

gui.load_images()

def refresh():
    gui.draw_board(canvas, chessboard.board, selected=selected, legal_moves=legal_moves_for_selected)

def on_click(event):
    global selected, legal_moves_for_selected, current_player

    if game_over:
        return

    # Ne pas laisser le joueur cliquer pendant que l'IA réfléchit
    if current_player == "black":
        print("L'IA est en train de jouer...")
        return

    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if not (0 <= row < 8 and 0 <= col < 8):
        return

    piece = chessboard.board[row][col]

    if selected is None:
        if piece == ".":
            return
        if (current_player == "white" and piece.isupper()) or (current_player == "black" and piece.islower()):
            selected = (row, col)
            legal_moves_for_selected = chessboard.get_moves_for_piece(chessboard.board, row, col)
        else:
            return
    else:
        from_row, from_col = selected
        move = (from_row, from_col, row, col)
        
        # Vérifie si le coup est dans la liste des coups légaux
        if move in legal_moves_for_selected:
            chessboard.board = chessboard.make_move(chessboard.board, move)
            selected = None
            legal_moves_for_selected = []
            current_player = "black" # C'est au tour de l'IA
            refresh()

            if check_game_end():
                return

            # Demande à l'IA de jouer après un court délai
            root.after(100, ai_move)
            return
        else:
            # Si le clic n'est pas un coup légal, on désélectionne
            print(f"Coup illégal : {move}")
            selected = None
            legal_moves_for_selected = []
    refresh()

def ai_move():
    global current_player
    if chessboard.is_game_over(chessboard.board, "black"):
        print(" Partie terminée : les noirs ne peuvent plus jouer !")
        check_game_end() # Vérifie la condition de victoire
        return

    # -----------------------------------------------------------
    # ◀️ --- AJOUT PRINCIPAL : VISUALISATION DE L'ARBRE ---
    # -----------------------------------------------------------
    # On affiche l'arbre des possibilités (prof. 2) AVANT que l'IA ne choisisse
    # On utilise deepcopy pour ne pas modifier le vrai plateau en simulant
    print("L'IA réfléchit... Affichage de l'arbre (profondeur 2)")
    tree_visualizer.build_and_show_tree(
        chessboard.deepcopy(chessboard.board), 
        "black", 
        depth=2  # Profondeur 2 = Coup IA + Réponse Joueur
    )
    # -----------------------------------------------------------

    # L'IA utilise Minimax (profondeur 3) pour trouver le MEILLEUR coup
    print("Calcul Minimax (profondeur 3) en cours...")
    val, move = minimax.find_best_move_for(chessboard.board, "black", depth=3)
    print(f"IA a choisi {move} (score: {val})")

    if move:
        chessboard.board = chessboard.make_move(chessboard.board, move)
        refresh()

        if check_game_end():
            return
    else:
        print("♟️ Aucune action possible pour l’IA.")
    
    current_player = "white"
    refresh()

def check_game_end():
    global game_over
    if game_over: return True # Déjà fini

    for player in ["white", "black"]:
        if chessboard.is_game_over(chessboard.board, player):
            winner = "NOIRS" if player == "white" else "BLANCS"
            print(f" Fin de partie — Les {winner} gagnent !")
            show_game_over_animation(f"Les {winner} gagnent !")
            return True
    return False

def start_new_game():
    global selected, legal_moves_for_selected, current_player, game_over
    print("--- NOUVELLE PARTIE ---")
    selected = None
    legal_moves_for_selected = []
    current_player = "white"
    game_over = False
    
    # Réinitialise le plateau à son état initial
    chessboard.board = [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"]
    ]
    
    refresh()

def show_game_over_animation(winner_text) :
    """Affiche une pastille floue avec un bouton rond à l’intérieur pour rejouer."""
    global game_over
    game_over = True

    # Capture l'échiquier et applique un flou
    try:
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        w = x + 8 * CELL_SIZE
        h = y + 8 * CELL_SIZE
        img = ImageGrab.grab(bbox=(x, y, w, h)).filter(ImageFilter.GaussianBlur(radius=6))
        bg_img = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erreur lors de la capture d'écran pour le flou: {e}")
        bg_img = None # Continue sans flou

    # Overlay
    overlay = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE, highlightthickness=0, bd=0)
    overlay.place(x=0, y=0)
    
    if bg_img:
        overlay.bg_img = bg_img # Garde une référence
        overlay.create_image(0, 0, anchor="nw", image=bg_img)
    else:
        overlay.create_rectangle(0, 0, 8*CELL_SIZE, 8*CELL_SIZE, fill="#000000", stipple="gray50")


    # Couleurs
    bg_color = "#2E2E2E"  
    text_color = "#FFFFFF"
    subtext_color = "#E0E0E0"

    # Coordonnées de la pastille
    cx, cy = 8 * CELL_SIZE / 2, 8 * CELL_SIZE / 2
    width, height = 360, 120
    radius = height / 2
    x1, y1 = cx - width / 2, cy - height / 2
    x2, y2 = cx + width / 2, cy + height / 2

    # Forme pastille (en 3 parties)
    overlay.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=bg_color, outline="")
    overlay.create_oval(x1, y1, x1 + height, y2, fill=bg_color, outline="")
    overlay.create_oval(x2 - height, y1, x2, y2, fill=bg_color, outline="")

    # Textes
    overlay.create_text(cx, cy - 20, text="PARTIE TERMINÉE", fill=text_color,
                        font=("Helvetica", 28, "bold"))
    overlay.create_text(cx, cy + 25, text=winner_text, fill=subtext_color,
                        font=("Helvetica", 18, "italic"))

    # Bouton rond pour rejouer
    def restart_game(event=None):
        overlay.destroy()
        restart_btn.destroy()
        start_new_game()

    circle_r = 22
    circle_x = x2 - radius # Le centre du cercle droit
    circle_y = cy
    restart_btn = tk.Canvas(overlay, width=circle_r * 2, height=circle_r * 2, highlightthickness=0, bd=0, bg=bg_color)
    restart_btn.place(x=circle_x - circle_r, y=circle_y - circle_r)

    restart_btn.create_oval(2, 2, circle_r * 2 - 2, circle_r * 2 - 2, fill="#4B8B3B", outline="white", width=2)
    restart_btn.create_text(circle_r, circle_r, text="↻", fill="white", font=("Helvetica", 18, "bold"))
    restart_btn.bind("<Button-1>", restart_game)



canvas.bind("<Button-1>", on_click)
refresh()
root.mainloop()