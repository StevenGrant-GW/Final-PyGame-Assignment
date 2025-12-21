'''
-----------------------------------------------------------------------------
Program Name: Square Collecter
Program Description: Move a red square to collect green targets while avoiding
an orange bouncing obstacle. Features a start menu and score system an end screen.
-----------------------------------------------------------------------------
References:
https://github.com/tczkqq/dvd-corner/blob/master/dvd-corner.py (used to help me make the obstacle)
https://www.pygame.org/docs/ref/rect.html (used in how i made collisions)
https://realpython.com/python-f-strings/ (taught me how to use f-strings to make the score system)
(put a link to your reference here but also add a comment in the code below where you used the reference)


-----------------------------------------------------------------------------


Additional Libraries/Extensions:
None required (standard Pygame)

Additional files to install in folder:
background.jpg
Blip9.WAV
Hit4.WAV
Pickup9.WAV
PressStart2P-Regular.ttf

-----------------------------------------------------------------------------


Known bugs:
1. due to the obstacle starting where the game last ended it can sometimes spawn inside the player


----------------------------------------------------------------------------




Program Reflection:
I think this project deserves a level 3+ because it manages to fulfill nearly every criteria
and uses some more complex mechanics like multiple menus/states and multiple external assets while
making a replayable game program

 Level 3 Requirements Met:
• Window size fits criteria
• Several user events including starting game, movement with WASD, restarting and ending game
• Using pygame.key.get_pressed() prevents issues from invalid keys
• Uses Integers (pos/size) and Strings (game_state)
• uses if/elif extensively throughout the program
• the main game runs of a While running: loop
• reset_game() is a custom function
• game has multiple screens with Menu, Game and Game over
• game has instructions displayed for every menu
• game includes several sounds for different actions
• game loads and scales a background
• game uses .colliderect() and .collidepoint() to make collision
• game loads PressStart2P-Regular.ttf as a font for all menus
'''


import pygame
import random
import os
pygame.init()

#finds the location of the folder where the game is
current_path = os.path.dirname(__file__)
os.chdir(current_path)

# *********SETUP**********

windowWidth = 800
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Square Collector")
clock = pygame.time.Clock()  #will allow us to set framerate

# *********LOAD ASSETTS*********
coin_pickup = pygame.mixer.Sound("Pickup9.WAV")
obstacle_hit = pygame.mixer.Sound("Hit4.WAV")
game_start = pygame.mixer.Sound("Blip9.WAV")
font_file = "PressStart2P-Regular.ttf"
bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (windowWidth, windowHeight))

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
font = pygame.font.Font(font_file, 15)
title_font = pygame.font.Font(font_file, 40)
small_font = pygame.font.Font(font_file, 20)

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

    #set up custom function to handle Game Over
    def reset_game(): 
        global score, game_state, player_x, player_y, obs_x_speed, obs_y_speed
        score, game_state, player_x, player_y = 0, "GAME", 385, 285
        obs_x_speed, obs_y_speed = 4, 4

    # *********EVENTS**********
    ev = pygame.event.poll()    # Look for any event
    if ev.type == pygame.QUIT:  # window close button clicked?
        break                   #   ... leave game loop
   
    # PUT YOUR MOUSE/KEYBOARD EVENTS HERE
    keys = pygame.key.get_pressed()
   
    if game_state == "MENU":
        if keys[pygame.K_SPACE]:
            game_start.play()
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
            reset_game()
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
            coin_pickup.play() # play coin pickup sound
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
            obstacle_hit.play() # play coin pickup sound
            game_state = "GAMEOVER"
   
    # *********DRAW THE FRAME**********
    window.fill((0, 0, 0))


    if game_state == "MENU":
        # Render surfaces
        title_surf = title_font.render("SQUARE COLLECTOR", True, (255, 255, 255))
        instr1_surf = small_font.render("TOUCH THE GREEN SQUARE FOR POINTS", True, (255, 255, 255))
        instr2_surf = small_font.render("AND AVOID THE ORANGE CIRCLE!", True, (255, 255, 255))
        instr3_surf = font.render("Press WASD to move", True, (200, 200, 200))
        start_surf = font.render("Press SPACE to Start", True, (200, 200, 200))
       
        # Draw centered text by calculating (Center - Half Width)
        title_pos = (windowWidth // 2 - title_surf.get_width() // 2, windowHeight // 4)
        instr1_pos = (windowWidth // 2 - instr1_surf.get_width() // 2, windowHeight // 2 - 50)
        instr2_pos = (windowWidth // 2 - instr2_surf.get_width() // 2, windowHeight // 2 - 20)
        instr3_pos = (windowWidth // 2 - instr3_surf.get_width() // 2, windowHeight // 2 + 60)
        start_pos = (windowWidth // 2 - start_surf.get_width() // 2, windowHeight // 2 + 80)
       
       # pairs the different texts and there positions/sizes
        window.blit(title_surf, title_pos)
        window.blit(instr1_surf, instr1_pos)
        window.blit(instr2_surf, instr2_pos)
        window.blit(instr3_surf, instr3_pos)
        window.blit(start_surf, start_pos)


    elif game_state == "GAME":
        #Draw the background image
        window.blit(bg_img, (0, 0))

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
        final_score_surf = title_font.render(f"Final Score: {score}", True, (255, 255, 255))
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
