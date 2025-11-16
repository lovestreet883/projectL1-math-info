import tkinter as tk
import chessboard
import gui
from PIL import Image, ImageTk, ImageFilter, ImageGrab

CELL_SIZE = 60
selected = None
legal_moves_for_selected = []
current_player = "white"
game_over = False

root = tk.Tk()
canvas = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE)


def start_new_game():
    global selected, legal_moves_for_selected, current_player, game_over
    selected = None
    legal_moves_for_selected = []
    current_player = "white"
    game_over = False
    canvas.delete("all")
    gui.draw_board(canvas, chessboard.board)


def show_game_over_animation(winner_text):
    """Affiche une pastille floue avec un bouton rond à l’intérieur pour rejouer."""
    global game_over
    game_over = True

    # Capture l'échiquier et applique un flou
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = x + 8 * CELL_SIZE
    h = y + 8 * CELL_SIZE
    img = ImageGrab.grab(bbox=(x, y, w, h)).filter(ImageFilter.GaussianBlur(radius=6))
    bg_img = ImageTk.PhotoImage(img)

    # Overlay flou
    overlay = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE, highlightthickness=0, bd=0)
    overlay.place(x=0, y=0)
    overlay.bg_img = bg_img
    overlay.create_image(0, 0, anchor="nw", image=bg_img)

    # Couleurs sobres
    bg_color = "#2E2E2E"  # gris anthracite
    text_color = "#FFFFFF"
    subtext_color = "#E0E0E0"

    # Coordonnées de la pastille
    cx, cy = 8 * CELL_SIZE / 2, 8 * CELL_SIZE / 2
    width, height = 360, 120
    radius = height / 2
    x1, y1 = cx - width / 2, cy - height / 2
    x2, y2 = cx + width / 2, cy + height / 2

    # Forme pastille
    overlay.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=bg_color, outline="")
    overlay.create_oval(x1, y1, x1 + height, y2, fill=bg_color, outline="")
    overlay.create_oval(x2 - height, y1, x2, y2, fill=bg_color, outline="")

    # Textes centrés dans la pastille
    overlay.create_text(cx, cy - 20, text="GAME OVER", fill=text_color,
                        font=("Helvetica", 28, "bold"))
    overlay.create_text(cx, cy + 25, text=winner_text, fill=subtext_color,
                        font=("Helvetica", 18, "italic"))

    # Bouton rond à l'intérieur, à droite de la pastille
    def restart_game(event=None):
        overlay.destroy()
        restart_btn.destroy()
        start_new_game()
        global game_over
        game_over = False

    circle_r = 22
    # placer le cercle à l'intérieur, légèrement à droite du centre
    circle_x = x2 - radius / 2
    circle_y = cy
    restart_btn = tk.Canvas(root, width=circle_r * 2, height=circle_r * 2, highlightthickness=0, bd=0, bg=root["bg"])
    restart_btn.place(x=circle_x - circle_r, y=circle_y - circle_r)

    restart_btn.create_oval(0, 0, circle_r * 2, circle_r * 2, fill="#4B8B3B", outline="")
    restart_btn.create_text(circle_r, circle_r, text="↻", fill="white", font=("Helvetica", 16, "bold"))

    # clic uniquement sur le cercle
    restart_btn.bind("<Button-1>", restart_game)
