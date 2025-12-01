import pygame



# --- Initialisation ---
pygame.init()


# --- fenêtre ---
screen = pygame.display.set_mode((600, 600))


# --- Paramètres & Couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 101, 181, 255)

# --- Paramètres ---
line_width = 10

# --- Taille des Font X / O ---
font = pygame.font.SysFont(None, 120) 


# --- Plateau ---
window_size = 600
board_game = 450
board_x = (window_size - board_game) // 2
board_y = (window_size - board_game) // 2
cells = board_game // 3

# --- Background ---
background = pygame.image.load(r"assets/background.png").convert()
background = pygame.transform.scale(background, (600, 600))
board_game_background = pygame.image.load(r"assets/background_board.png").convert()
board_game_background = pygame.transform.scale(board_game_background,(450,450))

# --- Smiley Ange / Démon ---
angel = pygame.image.load(r"assets/angel.png").convert_alpha()
angel = pygame.transform.smoothscale(angel, (cells, cells))
demon = pygame.image.load(r"assets/evil.png").convert_alpha()
demon = pygame.transform.smoothscale(demon, (cells, cells))

# --- Liste Plateau ---
board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
player = "X"

#       ~~~~~~~~ FONCTION DE STYLE  - avec IA ~~~~~~~

def draw_text_outline(text, font, color, outline_color, x, y, outline_size=2):
    # --- Calques du contour ---
    for ox in (-outline_size, 0, outline_size):
        for oy in (-outline_size, 0, outline_size):
            if ox != 0 or oy != 0:
                outline = font.render(text, True, outline_color)
                screen.blit(outline, (x + ox, y + oy))

    # --- Texte principal ---
    main = font.render(text, True, color)
    screen.blit(main, (x, y))




#       ~~~~~~~~ FONCTION MECANIQUE ~~~~~~~~



# --- Menu ---

def main_menu():
    

    # --- Font ---
    font_title = pygame.font.SysFont(None, 50)
    font_button = pygame.font.SysFont(None, 36)
    # --- Texte Boutons ---
    buttons = [ 
        ("Joueur VS Joueur", "pvp"),
        ("Joueur VS IA", "pvai"),
        ("Difficulté IA", "difficulty"),
        ("Quitter", "quit")
    ]
    buttons_width = 260
    buttons_height = 55
    spacing = 20
    # --- Centrage bouttons --- ( IA )
    total_height = len(buttons) * buttons_height + (len(buttons) - 1) * spacing
    start_y = (600 - total_height) // 2

    # --- Boutons --- ( IA )
    buttons_rects = []
    for i, (text, action) in enumerate (buttons):
        x = (600 - buttons_width) // 2
        y = start_y + i * (buttons_height + spacing)
        rect = pygame.Rect(x, y, buttons_width, buttons_height)
        buttons_rects.append((rect, action, text))

    # --- couleur boutons --- ( IA )
    for rect, action, text in buttons_rects:
        pygame.draw.rect(screen, (50, 50, 50), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        text_surf = font_button.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)



     # --- Boucle Menu & Clic Souris  ----   ( IA )
    while True:
        mouse_pos = pygame.mouse.get_pos()
        clic = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic = True
        screen.blit(background, (0, 0))

        for rect, action, text in buttons_rects:
            pygame.draw.rect(screen, (50, 50, 50), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            text_surf = font_button.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            if clic and rect.collidepoint(mouse_pos):
                return action
        pygame.display.flip()


# --- Menu difficulté ---

def difficulty_menu():

    # --- Font ---
    font_title = pygame.font.SysFont(None, 50)
    font_button = pygame.font.SysFont(None, 36)
    # --- Texte Boutons ---
    buttons = [ 
        ("Facile", "easy"),
        ("Moyen", "medium"),
        ("Difficile", "hard"),
        ("Retour", "back")
    ]
    buttons_width = 240
    buttons_height = 55
    spacing = 20
    # --- Centrage bouttons --- ( IA )
    total_height = len(buttons) * buttons_height + (len(buttons) - 1) * spacing
    start_y = (600 - total_height) // 2

    # --- Boutons --- ( IA )
    buttons_rects = []
    for i, (text, action) in enumerate (buttons):
        x = (600 - buttons_width) // 2
        y = start_y + i * (buttons_height + spacing)
        rect = pygame.Rect(x, y, buttons_width, buttons_height)
        buttons_rects.append((rect, action, text))


     # --- Boucle Menu & Clic Souris  ----   ( IA )
    while True:
        mouse_pos = pygame.mouse.get_pos()
        clic = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clic = True

        screen.blit(background, (0, 0))

        # --- Titre ---
        title = font_title.render("Difficulté IA", True, WHITE)
        title_rect = title.get_rect(center=(300, 120))
        screen.blit(title, title_rect)
        for rect, action, text in buttons_rects:
            pygame.draw.rect(screen, (50, 50, 50), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            text_surf = font_button.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            if clic and rect.collidepoint(mouse_pos):
                return action
            
        pygame.display.flip()
            

# --- Reset du plateau ---             
def reset_board():
    global board, player
    board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]]
    player = "X"




# --- Dessin joueurs plateau ---
def draw(i, j , player):
    x = board_x + j * cells
    y = board_y + i * cells

    if player == "X":
        screen.blit(angel, (x, y))

    elif player == "O":
        screen.blit(demon, (x, y))




# --- GRILLE  Visuelle 3x3 ----
def grid():
    # --- Lignes Vertivales ---
    pygame.draw.line(screen, BLACK, (board_x + cells, board_y),(board_x + cells, board_y + board_game), line_width)
    pygame.draw.line(screen, BLACK, (board_x + cells*2, board_y),(board_x + cells*2, board_y + board_game), line_width)
    # --- Lignes Horizontales ---
    pygame.draw.line(screen, BLACK,(board_x, board_y + cells), (board_x + board_game, board_y + cells), line_width)
    pygame.draw.line(screen, BLACK,(board_x, board_y + cells*2), (board_x + board_game, board_y + cells*2), line_width)




# --- Verification Victoire ---
def win():
    # --- Verif. lignes ---
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
    # --- Verif. colonnes ---
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    # --- Verfi. Diagonale gauche droite ---
    if board[0][0] == board[1][1] == board[2][2] == player:
          return True
    # --- Verif. Diagonale droite gauche ---
    if board[0][2] == board[1][1] == board[2][0] == player:
          return True
    return False



# --- Fin de partie ---
def end_game(message):
    # --- Format Texte ---
    x = window_size // 3
    y = 20
    font_end = pygame.font.SysFont(None, 60)
    text = font_end.render(message, True, BLACK)
    draw_text_outline(message, font_end, BLACK, WHITE, x, y)

    # --- Texte au dessus du board ---

    pygame.display.flip()

    # --- Blocage fin Relance partie et fermeture ---
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                wait = False




 # --- Clic souris ---
def clic_mouse(event):
    global player
    
    x, y = event.pos
    i = (y - board_y) // cells
    j = (x - board_x) // cells   

    
    print("Clique sur case : ", i ,j)

    # -- Verification si clic plateau ---
    if 0 <= i < 3 and 0 <= j < 3:

        board[i][j] = player
        draw(i, j, player)
            
        if win():
            end_game(f"{player} a gagné !")
            reset_board()
            main_menu()
            return

        # --- Change de joueur ---
        player = "X" if player == "O" else "O"



# --- Clock ---
clock = pygame.time.Clock()

# ••••••••••••••••••••••••••••••••••••••••••••••••••
# ------------_____ Boucle jeu _____--------------
# ••••••••••••••••••••••••••••••••••••••••••••••••••
mode = None
# -Correction Erreur menu boucle OK-
while mode not in("pvp", "pvai"):
    mode = main_menu()

    if mode == "difficulty":
        difficulty = difficulty_menu()
        print("Difficulté Choisie : ", difficulty)

    if difficulty == "back":
        mode = None
    else:
        print("Difficulté choisie :", difficulty)
        mode = None

# --- Choix Menu ---
if mode == "quit":
    pygame.quit()
    exit()
if mode == "pvp":
    print("Lancement du mode Joueur VS Joueur")
if mode == "pvai":
    print("Lancement du mode Joueur VS IA")
    # A activer plus tard




# --- Boucle ---
running = True
while running:
    # --- Gestion des évenements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     # Appel --- Clic souris ---
        if event.type == pygame.MOUSEBUTTONDOWN:
         clic_mouse(event)

    # Appel --- Affichage ---
    screen.blit(background, (0, 0))
    screen.blit(board_game_background, (board_x, board_y))

    # Appel --- Plateau ----
    pygame.draw.rect(screen, BLACK, (board_x - 5, board_y - 5, board_game + 10, board_game + 10), width=10)

    # Appel --- Affichage grille ---
    grid()

    # Affichage des X / O déjà joués
    for i in range(3):
        for j in range(3):
            if board[i][j] != "":
                draw(i, j, board[i][j])

    # --- Mise à jour écran + 60 fps ---
    pygame.display.flip()
    clock.tick(60)



pygame.quit()