'''
-----------------------------------------------------------------------------
Program Name: (never put your personal name or information on the Internet)
Program Description:

-----------------------------------------------------------------------------
References:

(put a link to your reference here but also add a comment in the code below where you used the reference)

-----------------------------------------------------------------------------

Additional Libraries/Extensions:

(put a list of required extensions so that the user knows that they need to download extra features)

-----------------------------------------------------------------------------

Known bugs:

(put a list of known bugs here, if you have any)

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
pygame.init()

# *********SETUP**********

windowWidth = 800
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()  #will allow us to set framerate

# Variables for setup
player_x = 250
player_y = 250
player_speed = 5
# ---------------------------

# *********GAME LOOP**********
while True:
    # *********EVENTS**********
    ev = pygame.event.poll()    # Look for any event
    if ev.type == pygame.QUIT:  # windowow close button clicked?
        break                   #   ... leave game loop
    
    #PUT YOUR MOUSE/KEYBOARD EVENTS HERE
    
    # *********GAME LOGIC**********
    
    # Movement Logic here to cause the character to move each cardinal direction with WASD
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    
    #PUT YOUR GAME LOGIN HERE FOR EACH GAMESTATE
    
    # *********DRAW THE FRAME**********
    window.fill((0, 0, 0)) # Clears the screen with black to keep the character from leaving a trail

    # Draws the player character as a red cube
    pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, 20, 20))

    #PUT YOUR DRAWING, IMAGE PLACEMENT, BLIT ETC.. COMMANDS HERE FOR EACH GAMESTATE'''

    # *********SHOW THE FRAME TO THE USER**********
    pygame.display.flip()
    clock.tick(60) #Force frame rate to 60fps or lower


pygame.quit()