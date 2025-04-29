import pygame
import sys
import game  # make sure main.py has a function run_game(p1, p2)

pygame.init()

# Screen setup
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

# Load assets
background_m = pygame.image.load("Images/main_page.png")
background_lod = pygame.image.load("Images/95690360.jpg")
background_lod = pygame.transform.scale(background_lod, (1200, 600))
name = pygame.image.load("Images/name.png")
name = pygame.transform.scale(name, (500, 120))
start_button = pygame.image.load("Images/start_button.png")
start_button_t = pygame.image.load("Images/start_button.png")
start_rect = start_button.get_rect(topleft=(180, 450))
start_rect_t = start_button_t.get_rect(topleft=(180, 300))

# Font & input box setup
font = pygame.font.Font(None, 50)
input_box1 = pygame.Rect(200, 250, 300, 50)
input_box2 = pygame.Rect(200, 330, 300, 50)
color_inactive = pygame.Color('black')
color_active = pygame.Color('dodgerblue2')
color1 = color_inactive
color2 = color_inactive
active1 = False
active2 = False
text1 = ''
text2 = ''
step = "menu" 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ## Handle events for each step
        if step == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and start_rect_t.collidepoint(event.pos):
                step = "names"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    step = "names"
        elif step == "names":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = True
                    active2 = False
                elif input_box2.collidepoint(event.pos):
                    active2 = True
                    active1 = False
                else:
                    active1 = active2 = False

                if start_rect.collidepoint(event.pos) and text1 and text2:
                    step = "loading"
            # Handle text input
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    elif event.key != pygame.K_RETURN:
                        text1 += event.unicode
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN:
                        active1 = False
                        active2 = True
                elif active2:
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    elif event.key != pygame.K_RETURN:
                        text2 += event.unicode
                    if event.key == pygame.K_UP:
                        active1 = True
                        active2 = False
                    if event.key == pygame.K_RETURN:
                        active1 = False
                        active2 = False
                if not active1 and not active2 and text1 and text2 and event.key == pygame.K_RETURN:
                    step = "loading"
                if not active1 and not active2 and not text1 and not text2 and event.key == pygame.K_RETURN:
                    active1 = True
                    active2 = False
    # ---- Drawing per step ----
    if step == "menu":
        screen.blit(background_m, (0, 0))
        screen.blit(name, (30, 100))
        screen.blit(start_button_t, start_rect_t)

    elif step == "names":
        screen.blit(background_m, (0, 0))
        screen.blit(name, (30, 100))
        screen.blit(start_button, start_rect)

        # Draw input boxes and labels
        color1 = color_active if active1 else color_inactive
        color2 = color_active if active2 else color_inactive
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)

        txt_surface1 = font.render(text1, True, (0, 0, 0))
        txt_surface2 = font.render(text2, True, (0, 0, 0))
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 10))
        screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 10))

        label1 = font.render("Player 1 :", True, (0, 0, 0))
        label2 = font.render("Player 2 :", True, (0, 0, 0))
        screen.blit(label1, (30, 255))
        screen.blit(label2, (30, 335))

    elif step == "loading":
                
        screen.blit(background_lod, (0, 0))
        pygame.display.flip()
        pygame.time.wait(500)
        game.main(text1,text2,screen,screen_width,screen_height)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
