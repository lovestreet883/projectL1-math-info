import tkinter as tk
from PIL import Image, ImageTk
import os

CELL_SIZE = 60
images_refs = {}  # dictionnaire pour garder les images en mémoire

def load_images():
    """Charge les images des pièces (cherche plusieurs dossiers possibles)."""
    global images_refs
    images_refs.clear()

   
    pieces = {
        "P": "wP.png", "R": "wR.png", "N": "wN.png", "B": "wB.png", "Q": "wQ.png", "K": "wK.png",
        "p": "bP.png", "r": "bR.png", "n": "bN.png", "b": "bB.png", "q": "bQ.png", "k": "bK.png"
    }

    # dossiers candidats (vérifie les plus probables)
    candidates = ["piece", "pieces", "chess_images", "chess_images", "images"]
    base_dir = None
    for c in candidates:
        path = os.path.join(os.path.dirname(__file__), c)
        if os.path.isdir(path):
            base_dir = path
            break

    if base_dir is None:
        # pas trouvé : on essaye le répertoire courant (utile si tu lances depuis un autre cwd)
        for c in candidates:
            if os.path.isdir(c):
                base_dir = c
                break

    if base_dir is None:
        print("[ERREUR] Aucun dossier d'images trouvé. Cherchés :", candidates)
        return
    else:
        print("[INFO] Dossier d'images utilisé :", base_dir)

    for symbol, filename in pieces.items():
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            img = Image.open(path).resize((CELL_SIZE - 8, CELL_SIZE - 8))
            images_refs[symbol] = ImageTk.PhotoImage(img)
        else:
            print(f"[ERREUR] Image introuvable pour {symbol} : {path}")


def draw_board(canvas, b, selected=None, legal_moves=None):
    """Dessine le plateau b sur le canvas."""
    canvas.delete("all")

    legal_targets = set()
    if legal_moves:
        for mv in legal_moves:
            legal_targets.add((mv[2], mv[3]))

    for i in range(8):
        for j in range(8):
            color = "#EEE" if (i + j) % 2 == 0 else "#555"
            canvas.create_rectangle(
                j * CELL_SIZE, i * CELL_SIZE,
                (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                fill=color, outline=""
            )

            if selected == (i, j):
                canvas.create_rectangle(
                    j * CELL_SIZE, i * CELL_SIZE,
                    (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                    outline="yellow", width=3
                )

            if (i, j) in legal_targets:
                canvas.create_oval(
                    j * CELL_SIZE + 25, i * CELL_SIZE + 25,
                    j * CELL_SIZE + 35, i * CELL_SIZE + 35,
                    fill="green", outline=""
                )

            piece = b[i][j]
            if piece != ".":
                if piece in images_refs:
                    canvas.create_image(
                        j * CELL_SIZE + CELL_SIZE // 2,
                        i * CELL_SIZE + CELL_SIZE // 2,
                        image=images_refs[piece]
                    )
                else:
                    canvas.create_text(
                        j * CELL_SIZE + 30, i * CELL_SIZE + 30,
                        text=piece, font=("Arial", 24), fill="black"
                    )
