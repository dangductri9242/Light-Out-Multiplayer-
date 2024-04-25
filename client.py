# This is a TCP Client for the game

import pygame
from network import Network
import pickle
pygame.font.init()
import sys

# initialize the screen
width = 1200
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

yellow = "#002060"
white  = (220,220,220)

# Get the IP address
IP = sys.argv[1]

def redrawWindow(win, game, p):
    #fill color
    win.fill((white))

    # if the game is not connected for both players
    if not(game.connected()):

        #Announcing waiting for the other player
        font = pygame.font.SysFont("erasdemiitc", 60)
        text = font.render("Waiting for the second player...", 1,white,yellow)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    # if the game is run with both players
    else:

        #if have not win yet
        if not game.winner():

            #Displaying rules --------------------------------------------------------------------------------
            font = pygame.font.SysFont("erasdemiitc", 20)
            text = font.render("Rules:", 1, (0,0,0))
            win.blit(text, (width/2 - text.get_width()/2, 40))

            font = pygame.font.SysFont("erasdemiitc", 20)
            text = font.render("Each player need to turn OFF all the lights (OFF - Blue, ON - YELLOW) in their sections.", 1, (0,0,0))
            win.blit(text, (width/2 - text.get_width()/2, 65))

            font = pygame.font.SysFont("erasdemiitc", 20)
            text = font.render("Whenever a light is touched, it will switch all the on/off status of itself and its neighbors", 1, (0,0,0))
            win.blit(text, (width/2 - text.get_width()/2, 90))
            
            #Displaying player ---------------------------------------------------------------------------------
            font = pygame.font.SysFont("erasdemiitc", 50)
            if p == 0:
                text = font.render("You", 1, white,yellow)
                win.blit(text, (50, 50))

                text = font.render("Ally", 1, yellow)
                win.blit(text, (1150-text.get_width(), 50))
            else:
                text = font.render("Ally", 1, yellow)
                win.blit(text, (50, 50))

                text = font.render("You", 1, white,yellow)
                win.blit(text, (1150-text.get_width(), 50))

            #Display board -----------------------------------------------------------------------------------
            board = game.getBoard()

            #Left board
            for i in range(0,10):
                for j in range(0,10):
                    if board[i][j] == 1:
                        pygame.draw.rect(win, "#FFFF66", (j*50+50,i*50+150,45,45))
                    else:
                        pygame.draw.rect(win, yellow, (j*50+50,i*50+150,45,45))

            #Right board
            for i in range(0,10):
                for j in range(10,20):
                    if board[i][j] == 1:
                        pygame.draw.rect(win, "#FFFF66", (j*50+150,i*50+150,45,45))
                    else:
                        pygame.draw.rect(win, yellow, (j*50+150,i*50+150,45,45))
        else:
            #Announcing players have won
            if (game.winner() == True and game.connected() == True):

                font = pygame.font.SysFont("rockwellextra", 90)
                text = font.render("You Won!", 1, yellow)
                win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

                font = pygame.font.SysFont("segoeui", 50)
                pygame.draw.rect(win, (140,140,140), (0,415,1200,80))
                text = font.render("Click anywhere to Quit!", 1, (0,0,0))
                win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2+100))

    #Update the graphics
    pygame.display.update()


def main():
    #Initializing state
    run = True
    clock = pygame.time.Clock()
    n = Network(IP)
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            #start the game
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break            

        #Get user input
        for event in pygame.event.get():
            #If player hits quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #If player click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Get position and corresponding position on the grid -------------------------------------------------------------
                pos = pygame.mouse.get_pos()

                x = pos[0]
                y = pos[1]

                if (50<=x) and (x<=550) and (150<=y) and (y<=650):
                    row = (x-50) //50
                    col = (y-150) //50

                elif (650<=x) and (x<=1150) and (150<=y) and (y<=650):
                    row = ((x-650) //50)+10
                    col = (y-150) //50

                # If the game is played normally, get user input-----------------------------------------------------------------------
                if game.connected() and not game.winner():
                    #Limit and allow player just get access to thier portion and take their inputs.
                    if player ==0:
                        if (50<=x) and (x<=550) and (150<=y) and (y<=650) and (player == 0):
                            n.send(str(row)+" "+str(col))
                    else:
                        if (650<=x) and (x<=1150) and (150<=y) and (y<=650) and (player == 1):
                            n.send(str(row)+" "+str(col))
                else:
                    #If win, stop the game
                    if game.winner():
                        run = False

        #Update graphics
        redrawWindow(win, game, player)

#Displaying menu
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        
        clock.tick(60)
        #Displaying menu screen --------------------------------------------------------------
        win.fill((white))

        font = pygame.font.SysFont("erasdemiitc", 100)
        text = font.render("Light Out", 1, white,yellow)
        win.blit(text, (width/2 - text.get_width()/2,170))

        font = pygame.font.SysFont("rockwellextra", 130)
        text = font.render("CHALLENGE", 1, (0,0,0))
        win.blit(text, (width/2 - text.get_width()/2,260))

        font = pygame.font.SysFont("segoeui", 60)
        pygame.draw.rect(win, (140,140,140), (0,495,1200,100))
        text = font.render("Click anywhere to play", 1, (0,0,0))
        win.blit(text, (width/2 - text.get_width()/2,500))
        pygame.display.update()

        #Take user input -----------------------------------------------------------------------------
        for event in pygame.event.get():
            #if they click quit, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            #if player click anywhere, go out of this loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    #start the game
    main()

#start the menu
while True:
    menu_screen()
