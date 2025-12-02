import pygame
import random


# ----------------------------------------------------------------------------------------------------------------------#
#                                                   VARIABLES                                                           #
# ----------------------------------------------------------------------------------------------------------------------#

# --- Initialisation ---
pygame.init()

# --- Clock ---
clock = pygame.time.Clock()

# --- fenêtre ---
screen = pygame.display.set_mode((600, 600))


# --- Paramètres & Couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 101, 181, 255)
line_width = 10

# --- Police ---
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
# --- IA D'ORIGINE ---
difficulty = "easy"

# --- Style texte --- (IA)
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



# ----------------------------------------------------------------------------------------------------------------------#
#                                                  FONCTION MECANIQUE                                                   #
# ----------------------------------------------------------------------------------------------------------------------#


# --- Menu ---
def main_menu():

    # --- Font ---
    font_title = pygame.font.SysFont(None, 50)
    font_button = pygame.font.SysFont(None, 36)

    # --- Texte Boutons ---
    buttons = [ 
        ("Joueur VS Joueur", "pvp"),
        ("Joueur VS IA", "pvai"),
        ("Difficulté IA", "choose_difficulty"),
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

# --- IA ---
def ordinateur(board, signe, difficulty):

    if difficulty == "easy":
        return ia_easy(board, signe)
    elif difficulty == "medium":
        return ia_medium(board, signe)
    elif difficulty == "hard":
        return ia_hard(board, signe)

def ia_easy(board, signe):
    free_list=[]
    for i in range(3):
        for n in range(3):
            if board[i][n] == "":
                free_list.append((i, n))
    return random.choice(free_list)

def check_win(board, signe, i, n):
    board[i][n] = signe
    result = win(board)
    board[i][n] = ""
    return result

def ia_medium(board, ia_signe, player_s):
    for i in range(3):
        for n in range(3):
            if board[i][n] == "":
                if check_win(board, ia_signe, i, n):
                    return(i, n)
                
    for i in range(3):
        for n in range(3):
            if board[i][n] == "":
                if check_win(board, player_s, i, n):
                    return(i, n)
            
    free = [(i, n)
            for i in range(3)
            for n in range(3)
            if board[i][n] == ""]
    return random.choice(free)


def minimax(board, depth, maximizing, ia_signe, player_s):
    result = win(board)

    # Si la partie est finie -> renvoi du score
    if result == ia_signe:
        return 1
    if result == player_s:
        return -1

    # Si plus de cases -> match nul
    if all(board[i][n] != "" for i in range(3) for n in range(3)):
        return 0

    if maximizing:
        best_score = -999
        for i in range(3):
            for n in range(3):
                if board[i][n] == "":
                    board[i][n] = ia_signe
                    score = minimax(board, depth + 1, False, ia_signe, player_s)
                    board[i][n] = ""
                    best_score = max(best_score, score)
        return best_score

    else:  # minimizing
        best_score = 999
        for i in range(3):
            for n in range(3):
                if board[i][n] == "":
                    board[i][n] = player_s
                    score = minimax(board, depth + 1, True, ia_signe, player_s)
                    board[i][n] = ""
                    best_score = min(best_score, score)
        return best_score


def ia_hard(board, ia_signe, player_s):
    best_score = -999
    best_move = None

    for i in range(3):
        for n in range(3):
            if board[i][n] == "":
                board[i][n] = ia_signe
                score = minimax(board, 0, False, ia_signe, player_s)
                board[i][n] = ""

                if score > best_score:
                    best_score = score
                    best_move = (i, n)

    return best_move

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


# --- Jeu ---          
def reset_board():
    global board, player
    board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]]
    player = "X"

def draw(i, j , player):
    x = board_x + j * cells
    y = board_y + i * cells

    if player == "X":
        screen.blit(angel, (x, y))

    elif player == "O":
        screen.blit(demon, (x, y))

def grid():
    # --- Lignes Vertivales ---
    pygame.draw.line(screen, BLACK, (board_x + cells, board_y),(board_x + cells, board_y + board_game), line_width)
    pygame.draw.line(screen, BLACK, (board_x + cells*2, board_y),(board_x + cells*2, board_y + board_game), line_width)
    # --- Lignes Horizontales ---
    pygame.draw.line(screen, BLACK,(board_x, board_y + cells), (board_x + board_game, board_y + cells), line_width)
    pygame.draw.line(screen, BLACK,(board_x, board_y + cells*2), (board_x + board_game, board_y + cells*2), line_width)

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

def tie():
    for i in board:
        if "" in i:
            return False
    return True

def already_played():
    for i in range(3):
        for j in range(3):
            if board[i][j] != "":
                draw(i, j, board[i][j])

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

def clic_mouse(event):
    global player

    # --- Position souris ---
    x, y = event.pos
    i = (y - board_y) // cells
    j = (x - board_x) // cells   
    print("A cliqué sur ", i ,j)

   

    # -- Verification si clic plateau ---
    if 0 <= i < 3 and 0 <= j < 3:
        
        # --- déjà joué ---
        if board[i][j] != "":
            print("Coup déjà joué")
            return  
        


         # --- Change de joueur ---
        player = "X" if player == "O" else "O"

        
    if mode == "pvai":
        i2, j2 = ordinateur(board, player, difficulty)
        board[i2][j2] = player
        draw(i2, j2, player)

    

        # --- Victoire ---
        if win():
            end_game(f"{player} a gagné !")
            reset_board()
            main_menu()
            return
        
        # --- Match Nul ---
        if tie():
            end_game("Match nul !")
            reset_board()
            main_menu()
            return
     # --- Change de joueur ---
        player = "X" if player == "O" else "O"
        
# --- Mode Jeu ---
def pvp():
    global player, board

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                i = (y - board_y) // cells
                j = (x - board_x) // cells   

                # case hors plateau
                if i < 0 or i > 2 or j < 0 or j > 2:
                    continue

                # --- case déjà prise ---
                if board[i][j] != "":
                    print("Coup déjà joué")
                    continue
              
                # --- jouer le coup ---
                board[i][j] = player
                draw(i, j, player)

                # changer de joueur
                player = "X" if player == "O" else "O"

        # --- Verification ---
        if win():
            end_game(f"{player} a gagné !")
            reset_board()
            return       

        if tie():
            end_game("Match nul !")
            reset_board()
            return 
        pygame.display.flip()

def pvai():
    return

# ----------------------------------------------------------------------------------------------------------------------#
#                                                   BOUCLE MENU                                                         #
# ----------------------------------------------------------------------------------------------------------------------#

# --- Choix Menu ---
mode = None
while True:

    mode = main_menu()

    if mode == "pvp":
        pvp()
        continue

    if mode == "pvai":
        pvai()
        continue
    if mode == "quit":
        pygame.quit()
        exit()
        break


# ----------------------------------------------------------------------------------------------------------------------#
#                                                   BOUCLE JEU                                                          #
# ----------------------------------------------------------------------------------------------------------------------#

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
    already_played()

    # --- Mise à jour écran + 60 fps ---
    pygame.display.flip()
    clock.tick(10)

pygame.quit()