# Visualisation de l’arbre de décision
import networkx as nx
import matplotlib.pyplot as plt
import chessboard  # requis pour les fonctions de jeu
import evaluation  # requis pour évaluer les feuilles

def show_tree(tree):
    """Dessine le graphe G fourni."""
    G = nx.DiGraph()
    
    # Ajoute les nœuds et les arêtes au graphe
    # 'tree' est un dictionnaire { 'parent_id': [ (child_id, label), ... ] }
    all_nodes = set(tree.keys())
    for parent, children in tree.items():
        for child_id, label in children:
            all_nodes.add(child_id)
            G.add_edge(parent, child_id, label=label)

    # Prépare les étiquettes pour les nœuds (on veut le score)
    labels = {node_id: f"{node_id}\n(Score: {data['score']:.1f})" for node_id, data in tree.items()}

    # Positionnement pour une meilleure lecture en arbre
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    
    # Dessine le graphe
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, 
            with_labels=True, 
            labels=labels, 
            node_color="lightblue", 
            node_size=3000, 
            font_size=8,
            arrows=True)
    
    # Ajoute les étiquettes sur les arêtes (les coups)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    plt.title("Arbre de décision (Minimax)")
    plt.show(block=False) # 'block=False' évite de bloquer le main.py


def build_and_show_tree(board, player, depth=2):
    """
    Construit un arbre de décision (jusqu'à 'depth') 
    et l'affiche en utilisant networkx.
    """
    print(f"Construction de l'arbre (profondeur {depth}) pour {player}...")
    
    tree_nodes = {} # Dictionnaire pour stocker les nœuds et leurs enfants
    node_counter = 0

    def get_move_str(move):
        """Convertit (x1,y1,x2,y2) en 'e2->e4' (notation plus simple)"""
        # Note: y est la colonne (lettre), x est la ligne (chiffre)
        # Mais ici on garde (ligne, col) pour rester simple
        return f"({move[0]},{move[1]}) -> ({move[2]},{move[3]})"

    def build_recursive(current_board, current_player, current_depth, parent_node_id):
        nonlocal node_counter
        
        # Condition d'arrêt : profondeur max atteinte ou partie finie
        if current_depth == 0 or chessboard.is_game_over(current_board, current_player):
            # C'est une feuille, on l'évalue
            score = evaluation.evaluate_board(current_board)
            tree_nodes[parent_node_id]['score'] = score
            return

        # Joueur suivant
        next_player = "black" if current_player == "white" else "white"
        
        # Explore les coups
        moves = chessboard.get_all_moves(current_board, current_player)
        
        # Si pas de coups, c'est aussi une feuille
        if not moves:
            score = evaluation.evaluate_board(current_board)
            tree_nodes[parent_node_id]['score'] = score
            return

        # Scores des enfants pour le minimax (remontée)
        children_scores = [] 

        # Limite le nombre d'enfants pour la visibilité
        # (sinon l'arbre est trop grand)
        max_children_to_show = 5 
        
        for move in moves[:max_children_to_show]:
            # 1. Crée le nouvel état du jeu
            new_board = chessboard.make_move(current_board, move)
            
            # 2. Crée un nouveau nœud pour l'arbre
            node_counter += 1
            child_node_id = f"Nœud {node_counter}"
            tree_nodes[child_node_id] = {'score': 0, 'children': []} # score initial

            # 3. Ajoute l'enfant au parent (avec le coup comme étiquette)
            move_label = get_move_str(move)
            tree_nodes[parent_node_id]['children'].append( (child_node_id, move_label) )

            # 4. Appel récursif
            build_recursive(new_board, next_player, current_depth - 1, child_node_id)
            
            # 5. Récupère le score calculé de l'enfant
            children_scores.append(tree_nodes[child_node_id]['score'])

        # Logique Minimax simple pour le score du parent
        if not children_scores:
             tree_nodes[parent_node_id]['score'] = evaluation.evaluate_board(current_board)
        elif current_player == "white": # Maximizoo
            tree_nodes[parent_node_id]['score'] = max(children_scores)
        else: # Minimizing
            tree_nodes[parent_node_id]['score'] = min(children_scores)


    # --- Point de départ de la construction ---
    root_id = "Racine (Actuel)"
    tree_nodes[root_id] = {'score': 0, 'children': []}
    
    # Lance la construction récursive
    build_recursive(board, player, depth, root_id)

    # Crée le graphe NetworkX à partir de notre structure
    G_viz = nx.DiGraph()
    labels_nodes = {}
    labels_edges = {}

    for parent_id, data in tree_nodes.items():
        labels_nodes[parent_id] = f"{parent_id}\n(Score: {data['score']:.1f})"
        G_viz.add_node(parent_id)
        for child_id, move_label in data['children']:
            G_viz.add_edge(parent_id, child_id)
            labels_edges[(parent_id, child_id)] = move_label

    # Dessine le graphe
    plt.figure(figsize=(15, 10))
    pos = nx.nx_agraph.graphviz_layout(G_viz, prog="dot") # layout en arbre
    
    nx.draw(G_viz, pos, 
            labels=labels_nodes, 
            with_labels=True, 
            node_color="skyblue", 
            node_size=3500, 
            font_size=9,
            font_weight="bold",
            arrows=True,
            arrowsize=20)
            
    nx.draw_networkx_edge_labels(G_viz, pos, 
                                 edge_labels=labels_edges, 
                                 font_color='red',
                                 font_size=8)
    
    plt.title(f"Arbre d'analyse pour {player} (profondeur {depth})")
    plt.show(block=False) # Affiche sans bloquer le jeu