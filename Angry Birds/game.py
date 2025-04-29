import pygame
import math
import sys
import random
import blocks
import angry_birds
import projectiles
# Initialize the pygame module
def main(text1,text2,screen,screen_width,screen_height):

     # Randomize wind for each game
    wind_speed = random.uniform(0, 1.0)  # Random wind speed
    wind_angle = random.uniform(0, 2 * math.pi)  # Random wind direction in radians
    projectiles.set_wind(wind_speed, wind_angle)

    o = 35
    pygame.init()
    # LOAD ASSETS
    # Load background image
    clock = pygame.time.Clock()
    catapult_center_l = pygame.math.Vector2(297.5, 362.5)
    catapult_center_r = pygame.math.Vector2(900, 362.5)
    score_player1 = 0
    score_player2 = 0
    pygame.display.set_caption("Angry Birds")

    background = pygame.image.load("Images/background.jpg")
    sprite = pygame.image.load("Images/catapult.png")
    background = pygame.transform.scale(background, (1200, 600))
    sprite = pygame.transform.scale(sprite, (50, 180))
    ibg = pygame.image.load("Images/ibg.png")
    ibg = pygame.transform.scale(ibg, (560, 300))
    final_image = pygame.image.load("Images/final.png")
    final_image = pygame.transform.scale(final_image, (600, 300))
    # Load exit button image
    exit_button = pygame.image.load("Images/exit_button.png")
    exit_button = pygame.transform.scale(exit_button, (50, 50))
    exit_button_rect = exit_button.get_rect(topright=(screen_width - 10, screen_height - 60))
    font = pygame.font.SysFont(None, 40)

    # Player turn tracking
    current_player = 1
    current_player_name = ""
    # Check if all blocks are destroyed for Player 1 or Player 2
    def check_game_end():
        player1_blocks = any(block is not None for row in blocks.block_rect_l for block in row)
        player2_blocks = any(block is not None for row in blocks.block_rect_r for block in row)
        if not player1_blocks:
            return text2
        elif not player2_blocks:
            return text1
        return None
    def display_winner_screen(winner, score, screen):
        screen.blit(background,(0,0))  # background
        title_font = pygame.font.SysFont("comicsans", 100, bold=True)
        score_font = pygame.font.SysFont("comicsans", 60, bold=False)
    
        # Display winner text
        winner_text = title_font.render(f"{winner} Wins!", True, (244, 4, 96))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, 100))
    
        # Display score
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        screen.blit(final_image, (300, 250))
       # Load and display the "Play" button image
        play_button = pygame.image.load("Images/play_button.png")  # Replace with your button image path
        play_button_rect = play_button.get_rect(center=(screen.get_width() // 2, 300))
        #screen.blit(play_button, play_button_rect)

        pygame.display.flip()
    
        # Wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        return True  # Restart the game
    # Player 1 (left)
    selected_l = False
    drag_l = False
    launched_l = False
    p_l = 0
    launch_l = False
    # Player 2 (right)
    selected_r = False
    drag_r = False
    launched_r = False
    p_r = 0
    launch_r = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    # Determine the winner or draw
                    if score_player1 > score_player2:
                        winner = "Player 1"
                        winner_score = score_player1
                    elif score_player2 > score_player1:
                        winner = "Player 2"
                        winner_score = score_player2
                    else:
                        winner = "Draw"
                        winner_score = None

                    # Display the winner screen
                    if winner == "Draw":
                        if display_winner_screen("It's a Draw! No", "Scores are tied!", screen):
                            main(text1, text2, screen, screen_width, screen_height)  # Restart the game
                    else:
                        if display_winner_screen(winner, winner_score, screen):
                            main(text1, text2, screen, screen_width, screen_height)  # Restart the game

                    running = False
                    break
            # --- PLAYER 1 TURN ---
            if current_player == 1:               
                current_player_name = text1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(3):
                        if angry_birds.rect_l[i].collidepoint(event.pos) and not selected_l:
                            selected_l = True
                            p_l = i
                            angry_birds.rect_l[i] = angry_birds.birds_l[i].get_rect(center=catapult_center_l)
                            break
                    if angry_birds.rect_l[p_l].collidepoint(event.pos) and not launched_l and selected_l and not drag_l:
                        drag_l = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    try:
                        if drag_l and drag_vector_l.length() > 5:                        
                            drag_l = False
                            launched_l = True
                            launch_l = True
                        else:
                            # Reset bird to catapult center if drag is invalid
                            angry_birds.rect_l[p_l].center = catapult_center_l
                            drag_l = False
                            launched_l = False
                    except UnboundLocalError:
                        drag_vector_l = pygame.math.Vector2(0, 0)
                        if drag_l and drag_vector_l.length() > 5:                        
                            drag_l = False
                            launched_l = True
                            launch_l = True
                        else:
                            # Reset bird to catapult center if drag is invalid
                            angry_birds.rect_l[p_l].center = catapult_center_l
                            drag_l = False
                            launched_l = False
                if launched_l:
                    try:
                        proj = projectiles.projectile(
                            angry_birds.birds_l[p_l],
                            angry_birds.rect_l[p_l].center,
                            (drag_vector_l.x / 2, drag_vector_l.y / 2),(0,-2),angry_birds.bird_types_l[p_l]
                        )
                    except UnboundLocalError:
                        drag_vector_l = pygame.math.Vector2(0, 0)
                        proj = projectiles.projectile(
                            angry_birds.birds_l[p_l],
                            angry_birds.rect_l[p_l].center,
                            (drag_vector_l.x / 2, drag_vector_l.y / 2),(0,-2),angry_birds.bird_types_l[p_l]
                        )
            
                    projectiles.projectiles_l.append(proj)
                    launched_l = False
                    selected_l = False
                    current_player = 2
                    angry_birds.birds_l = [angry_birds.bird_l(random.randint(1,4)) for i in range(3)]
                    angry_birds.rect_l = [image.get_rect(topleft=(330+(o+5)*(angry_birds.birds_l.index(image)),480)) for image in angry_birds.birds_l]

                elif event.type == pygame.MOUSEMOTION and not launched_l and drag_l:
                    mouse_pos = pygame.math.Vector2(event.pos)
                    drag_vector_l = mouse_pos - catapult_center_l
                    if drag_vector_l.length() > projectiles.max_drag:
                        drag_vector_l.scale_to_length(projectiles.max_drag)
                    if drag_vector_l.length() <= 5 and mouse_pos == catapult_center_l:
                        drag_vector_l = pygame.math.Vector2(0, 0) 
                        drag_l = False
                    angry_birds.rect_l[p_l].center = catapult_center_l + drag_vector_l

            # --- PLAYER 2 TURN ---
            elif current_player == 2:
                current_player_name = text2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(3):
                        if angry_birds.rect_r[i].collidepoint(event.pos) and not selected_r:
                            selected_r = True
                            p_r = i
                            angry_birds.rect_r[i] = angry_birds.birds_r[i].get_rect(center=catapult_center_r)
                            break
                    if angry_birds.rect_r[p_r].collidepoint(event.pos) and not launched_r and selected_r and not drag_r:
                        drag_r = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    try:
                        if drag_r and drag_vector_r.length() > 5:
                            drag_r = False
                            launched_r = True
                            launch_r = True
                        else:
                            # Reset bird to catapult center if drag is invalid
                            angry_birds.rect_r[p_r].center = catapult_center_r
                            drag_r = False
                            launched_r = False
                    except UnboundLocalError:
                        drag_vector_r = pygame.math.Vector2(0, 0)
                        if drag_r and drag_vector_r.length() > 5:
                            drag_r = False
                            launched_r = True
                            launch_r = True

                        else:                      
                            # Reset bird to catapult center if drag is invalid
                            angry_birds.rect_r[p_r].center = catapult_center_r
                            drag_r = False
                            launched_r = False
                if launched_r:
                    try:
                        proj = projectiles.projectile(
                            angry_birds.birds_r[p_r],
                            angry_birds.rect_r[p_r].center,
                            (drag_vector_r.x / 2, drag_vector_r.y / 2),(0,-2),angry_birds.bird_types_r[p_r]
                        )
                    except UnboundLocalError:
                        drag_vector_r = pygame.math.Vector2(0, 0)
                        proj = projectiles.projectile(
                            angry_birds.birds_r[p_r],
                            angry_birds.rect_r[p_r].center,
                            (drag_vector_r.x / 2, drag_vector_r.y / 2),(0,-2),angry_birds.bird_types_r[p_r]
                        )

                    projectiles.projectiles_r.append(proj)
                    launched_r = False
                    selected_r = False
                    current_player = 1
                    angry_birds.birds_r = [angry_birds.bird_r(random.randint(1,4)) for i in range(3)]
                    angry_birds.rect_r = [image.get_rect(topleft=(775+(o+5)*(angry_birds.birds_r.index(image)),480)) for image in angry_birds.birds_r]

                elif event.type == pygame.MOUSEMOTION and not launched_r and drag_r:
                    mouse_pos = pygame.math.Vector2(event.pos)
                    drag_vector_r = mouse_pos - catapult_center_r
                    if drag_vector_r.length() <= 5 or mouse_pos == catapult_center_r:
                        drag_vector_r = pygame.math.Vector2(0, 0)
                        drag_r = False
                    if drag_vector_r.length() > projectiles.max_drag:
                        drag_vector_r.scale_to_length(projectiles.max_drag)
                    angry_birds.rect_r[p_r].center = catapult_center_r + drag_vector_r

        winner = check_game_end()
        if winner:
            if winner == "Player 1":
                if display_winner_screen(text1, score_player1, screen):
                    main(text1, text2, screen, screen_width, screen_height)  # Restart the game
            elif winner == "Player 2":
                if display_winner_screen(text2, score_player2, screen):
                    main(text1, text2, screen, screen_width, screen_height)  # Restart the game
            running = False
            break
        # Before drawing real projectiles...
        wind_speed = random.uniform(0, 0.5)
        if wind_speed == 0:
            wind_angle = 0   
        else:  # Random wind speed
            wind_angle = random.uniform(0, 2 * math.pi)  # Random wind direction in radians
        projectiles.set_wind(wind_speed, wind_angle)
        # Drawing
        screen.blit(background, (0, 0))
        screen.blit(sprite, (275, 335))  # Left catapult
        screen.blit(sprite, (875, 335))  # Right catapult
        # Left catapult
        # Blocks and energy bars
        blocks.block_draw_left(blocks.block_rect_l,screen)
        blocks.block_draw_right(blocks.block_rect_r,screen)
        blocks.energy_bars(blocks.block_rect_l, screen, pygame.draw, pygame.draw)
        blocks.energy_bars(blocks.block_rect_r, screen, pygame.draw, pygame.draw)
        pygame.draw.rect(screen, "black", (catapult_center_l.x,catapult_center_l.y, 5, 5))
        pygame.draw.rect(screen, "black", (catapult_center_r.x,catapult_center_r.y, 5, 5))

        try:
            if current_player == 1 and drag_l:
                projectiles.draw_trajectory(
                    screen,
                    catapult_center_l,
                    drag_vector_l * (-0.5),
                    pygame.math.Vector2(0, -2)
            )
            elif current_player == 2 and drag_r:
                projectiles.draw_trajectory(
                    screen,
                    catapult_center_r,
                    drag_vector_r * (-0.5),
                    pygame.math.Vector2(0, -2)
            )
        except UnboundLocalError:
            drag_vector_l = pygame.math.Vector2(0, 0)
            drag_vector_r = pygame.math.Vector2(0, 0)
            if current_player == 1 and drag_l:
                projectiles.draw_trajectory(
                    screen,
                    catapult_center_l,
                    drag_vector_l * (-0.5),
                    pygame.math.Vector2(0, -2)
            )
            elif current_player == 2 and drag_r:
                projectiles.draw_trajectory(
                    screen,
                    catapult_center_r,
                    drag_vector_r * (-0.5),
                    pygame.math.Vector2(0, -2)
            )

        # Projectiles
        for proj in projectiles.projectiles_l:
            for i,row in enumerate(blocks.block_rect_r):
                for j,block in enumerate(row):
                    if block is not None and proj.rect.colliderect(block.rect):
                        collision_side = projectiles.get_collision_side(block.rect, proj.rect)
                
                        # Adjust bird's motion based on collision side
                        if collision_side == "top":
                            proj.vel.y = -proj.vel.y  # Reverse vertical velocity
                        elif collision_side == "left":
                            proj.vel.x = -proj.vel.x  # Reverse horizontal velocity
                        elif collision_side == "right":
                            proj.vel.x = -abs(proj.vel.x)


                        if proj.bird_type == 3 and block.type in {1, 4}:  # Chuk
                            damage = 50
                        elif proj.bird_type == 2 and block.type == 2:  # Bomb
                            damage = 50
                        elif proj.bird_type == 1 and block.type == 3:  # Blue Bird
                            damage = 50
                        elif proj.bird_type == 4:  # Red Bird
                            damage = 37
                        else:
                            damage = 25

                        block.health -= damage

                        score_player1 += 2*damage
                        # Check if block is destroyed
                        if block.health <= 0:
                            blocks.block_rect_r[i][j] = None
                            score_player1 += 15

        for proj in projectiles.projectiles_r:
            for i,row in enumerate(blocks.block_rect_l):
                for j,block in enumerate(row):
                    if block is not None and proj.rect.colliderect(block.rect):
                        collision_side = projectiles.get_collision_side(block.rect, proj.rect)
                        # Adjust bird's motion based on collision side
                        if collision_side == "top":             
                            proj.vel.y = -proj.vel.y
                        #elif collision_side == "left":
                            #proj.vel.x = -abs(proj.vel.x)
                        elif collision_side == "right": 
                            proj.vel.x = -proj.vel.x
    
                        if proj.bird_type == 3 and block.type in [1, 4]:  # Chuk
                            damage = 50
                        elif proj.bird_type == 2 and block.type == 2:  # Bomb
                            damage = 50
                        elif proj.bird_type == 1 and block.type == 3:  # Blue Bird
                            damage = 50
                        elif proj.bird_type == 4:  # Red Bird
                            damage = 37
                        else:
                            damage = 25

                        block.health -= damage

                        score_player2 += 2*damage
                        if block.health <= 0:
                            blocks.block_rect_l[i][j] = None
                            score_player2 += 15


        # Draw projectiles               
        for proj in projectiles.projectiles_l:
            proj.update()
            proj.draw(screen)
        for proj in projectiles.projectiles_r:
            proj.update()
            proj.draw(screen)

        # Angry birds
        if current_player == 1 and not launch_l:
            angry_birds.birds_draw_left(screen)
        elif current_player == 2 and not launch_r:
            angry_birds.birds_draw_right(screen)

        # Display turn info
        turn_text = font.render(f"{current_player_name}'s Turn", True, (0, 25, 30))
        screen.blit(turn_text, (screen_width // 2 - 100, 20))

        wind_speed_text = font.render(f"Wind Speed: {wind_speed:.2f}", True, (0, 0, 0))
        wind_direction_text = font.render(f"Wind Direction: {math.degrees(wind_angle):.1f}°", True, (0, 0, 0))
        screen.blit(wind_speed_text, (screen_width // 2 - 100, 50))
        screen.blit(wind_direction_text, (screen_width // 2 - 100, 80))

        score_text_p1 = font.render(f"{text1} Score: {score_player1}", True, (0, 0, 255))
        score_text_p2 = font.render(f"{text2} Score: {score_player2}", True, (255, 0, 0))
        screen.blit(score_text_p1, (100, 20))
        screen.blit(score_text_p2, (screen_width - 300, 20))

        screen.blit(exit_button, exit_button_rect)
        # Flip
        pygame.display.flip()
        clock.tick(30)
        launch_r = False
        launch_l = False
    pygame.quit()
    sys.exit()