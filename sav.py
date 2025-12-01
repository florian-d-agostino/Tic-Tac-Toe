   
   # --- Boucle Menu ---
while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # --- Clic souris ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if button_rect.collidepoint(mx, my):
                    return "pvp"
                
            # --- Affichage du menu ---
            screen.fill(BLACK)

            # --- Bouton ---
            pygame.draw.rect(screen, BLUE, button_rect, border_bottom_left_radius=10)
            button_text = font_button.render("Joueur VS Joueur", True, WHITE)
            screen.blit(
                button_text,
                (300 - button_text.get_width() // 2,
                 300 - button_text.get_height() // 2 + 10)
            )
            pygame.display.flip()