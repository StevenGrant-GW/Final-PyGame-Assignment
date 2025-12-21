'''
-----------------------------------------------------------------------------
Program Name: Square Collecter
Program Description: Move a red square to collect green targets while avoiding
an orange bouncing obstacle. Features a start menu and score system an end screen.
-----------------------------------------------------------------------------
References:
https://github.com/tczkqq/dvd-corner/blob/master/dvd-corner.py
https://www.pygame.org/docs/ref/rect.html
(put a link to your reference here but also add a comment in the code below where you used the reference)


-----------------------------------------------------------------------------


Additional Libraries/Extensions:
None required (standard Pygame)


-----------------------------------------------------------------------------


Known bugs:
None


----------------------------------------------------------------------------




Program Reflection:
I think this project deserves a level XXXXXX because ...


 Level 3 Requirements Met:
•
•  
•  
•  
•  
•


Features Added Beyond Level 3 Requirements:
•
•  
•  
•  
•  
•
-----------------------------------------------------------------------------
'''


import pygame
import random
pygame.init()


# *********SETUP**********


windowWidth = 800
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Square Collector")
clock = pygame.time.Clock()  #will allow us to set framerate


# Variables for the player character
player_x = 385 # Centered for 800 width
player_y = 285 # Centered for 600 height
player_size = 30
player_speed = 5


# Variables for target square
target_x = random.randint(0, windowWidth - 20)
target_y = random.randint(0, windowHeight - 20)
target_size = 20


# Variables to set up a score system
score = 0
# Using default fonts to ensure consistency across different computers
font = pygame.font.SysFont("Arial", 32)
title_font = pygame.font.SysFont("Arial", 72, bold=True)


# Variables for Obstacle
obs_radius = 25
obs_x = random.randint(obs_radius, windowWidth - obs_radius)
obs_y = random.randint(obs_radius, windowHeight - obs_radius)
obs_x_speed = 4
obs_y_speed = 4


# State variable to handle Menu vs Game
game_state = "MENU"
# ---------------------------


# *********GAME LOOP**********
running = True
while running:
    # *********EVENTS**********
    ev = pygame.event.poll()    # Look for any event
    if ev.type == pygame.QUIT:  # window close button clicked?
        break                   #   ... leave game loop
   
    # PUT YOUR MOUSE/KEYBOARD EVENTS HERE
    keys = pygame.key.get_pressed()
   
    if game_state == "MENU":
        if keys[pygame.K_SPACE]:
            game_state = "GAME"


    elif game_state == "GAME":
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed

    elif game_state == "GAMEOVER":
        if keys[pygame.K_r]:
            score, game_state, player_x, player_y = 0, "GAME", 385, 285
        if keys[pygame.K_ESCAPE]:
            running = False


    # *********GAME LOGIC**********
    if game_state == "GAME":
        # detect collision with walls so the player can not leave the window
        if player_x < 0:
            player_x = 0
        if player_x > windowWidth - player_size:
            player_x = windowWidth - player_size
        if player_y < 0:
            player_y = 0
        if player_y > windowHeight - player_size:
            player_y = windowHeight - player_size


        # Make the obstacle move around the screen (using DVD logic reference)
        if (obs_x + obs_radius >= windowWidth) or (obs_x - obs_radius <= 0):
            obs_x_speed = -obs_x_speed
        if (obs_y + obs_radius >= windowHeight) or (obs_y - obs_radius <= 0):
            obs_y_speed = -obs_y_speed
       
        obs_x += obs_x_speed
        obs_y += obs_y_speed
        # ---------------------------


        # Make the green square collide with the player (using PyGame .rect reference)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        target_rect = pygame.Rect(target_x, target_y, target_size, target_size)

        # Checks if the player touches the target to increase score and move the target
        if player_rect.colliderect(target_rect):
            score += 1
            target_x = random.randint(0, windowWidth - target_size)
            target_y = random.randint(0, windowHeight - target_size)

        # Every 3 points, increase the absolute speed of the obstacle by 1
            if score > 0 and score % 3 == 0:
                if obs_x_speed > 0: obs_x_speed += 1
                else: obs_x_speed -= 1
                
                if obs_y_speed > 0: obs_y_speed += 1
                else: obs_y_speed -= 1

        # Checks if the player touches the obstacle to trigger a game over
        if player_rect.collidepoint(obs_x, obs_y):
            game_state = "GAMEOVER"
   
    # *********DRAW THE FRAME**********
    window.fill((0, 0, 0))


    if game_state == "MENU":
        # Render surfaces
        title_surf = title_font.render("SQUARE COLLECTOR", True, (255, 255, 255))
        instr_surf = font.render("Touch the green square for points and avoid the Orange Circle!", True, (255, 255, 255))
        start_surf = font.render("Press SPACE to Start", True, (200, 200, 200))
       
        # Draw centered text by calculating (Center - Half Width)
        title_pos = (windowWidth // 2 - title_surf.get_width() // 2, windowHeight // 4)
        instr_pos = (windowWidth // 2 - instr_surf.get_width() // 2, windowHeight // 2 - 20)
        start_pos = (windowWidth // 2 - start_surf.get_width() // 2, windowHeight // 2 + 60)
       
        window.blit(title_surf, title_pos)
        window.blit(instr_surf, instr_pos)
        window.blit(start_surf, start_pos)


    elif game_state == "GAME":
        # Draw the target green square
        pygame.draw.rect(window, (0, 255, 0), (target_x, target_y, target_size, target_size))
       
        # Draw the red player square
        pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_size, player_size))


        # Draw the orange circle obstacle
        pygame.draw.circle(window, (255, 165, 0), (int(obs_x), int(obs_y)), obs_radius)


        # Draw the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (20, 20))

    elif game_state == "GAMEOVER":
        # Render surfaces
        over_surf = title_font.render("GAME OVER", True, (255, 0, 0))
        final_score_surf = font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_surf = font.render("Press R to Restart", True, (200, 200, 200))
        quit_surf = font.render("Press Escape to Quit", True, (150, 150, 150))

        # Position surfaces
        over_pos = (windowWidth // 2 - over_surf.get_width() // 2, windowHeight // 4)
        score_pos = (windowWidth // 2 - final_score_surf.get_width() // 2, windowHeight // 2 - 40)
        restart_pos = (windowWidth // 2 - restart_surf.get_width() // 2, windowHeight // 2 + 40)
        quit_pos = (windowWidth // 2 - quit_surf.get_width() // 2, windowHeight // 2 + 90)

        # Draw surfaces
        window.blit(over_surf, over_pos)
        window.blit(final_score_surf, score_pos)
        window.blit(restart_surf, restart_pos)
        window.blit(quit_surf, quit_pos)


    # *********SHOW THE FRAME TO THE USER**********
    pygame.display.flip()
    clock.tick(60) #Force frame rate to 60fps or lower

pygame.quit()
