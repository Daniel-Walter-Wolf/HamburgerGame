## Victor Fabio and Dan Wolf
##
## 11/17/13
##
## This program runs a game in which hamburgers fly across the screen and the player has to catch
## them and eat them before they leave the screen.  If they miss too many, the game is over.
##
## For this game we used the python and pygame documentation.

#import modules
import pygame
import random
import math

#this function finds the distance between two points
def distance (x1, y1, x2, y2):
    """Calculates the distance between two points (x1, y1) and
    (x2,y2)."""
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

#set up indices
WIDTH = 0
X = 1
Y = 2
XVEL = 3
YVEL = 4
COLOR = 5
COLLIDE = 6
HEIGHT = 7

#define all helping functions to create and filter the burgers, to read and
#write the high score file, and order the high scores.
def create_burger(width, height,w2):
    x = width-w2
    y = random.randint(w2, height-w2)
    xvel = 2
    yvel = 0
    color = (0,240,0)
    collide = False
    burger = [w2, x, y, xvel, yvel, color, collide]
    return burger

def filter_burgers(burgers):
    burgers2 = []
    for burger in burgers:
        if burger[X] > 0:
            burgers2 += [burger]
    return burgers2

def read_file():
    f = open("hiscores.txt", "r")
    dict = {}
    
    for line in f:
        n = line.strip("\n")
        n = n.split(":")
        
        key = n[0]
        value = int(n[1])
        
        dict[key] = value
        
    return dict        

    f.close()

def order_dict(dict):
    first = 0
    second = 0
    third = 0
    scores = []
    
    for key, value in dict.items():
        if value > first:
            first = value
            name = key
    scores += [name + ": " + str(first)]
    
    for key, value in dict.items():
        if value > second and value < first:
            second = value
            name = key
    scores += [name + ": " + str(second)]
    
    for key, value in dict.items():
        if value > third and value < second:
            third = value
            name = key
    scores += [name + ": " + str(third)]
    
    return scores

def write_file(dict):
    f= open("hiscores.txt","w")
    
    for key,value in dict.items():
        entry = str(key)+":"+str(value)+"\n"
        f.write(entry)
        
    f.close()

#main game function
def run_game():
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()
    
    flames = pygame.image.load("Flames.png")

    # pictures and sound
    width = flames.get_width()
    height = flames.get_height()
    my_win = pygame.display.set_mode((width,height))

    myFont = pygame.font.Font(None,30)
    endFont = pygame.font.Font(None,80)

    hamburger = pygame.image.load("hamburger.png")
    hamburger = hamburger.convert_alpha()

    w2 = hamburger.get_width()
    
    skull = pygame.image.load("Skull.png")
    skull = skull.convert_alpha()
    
    bite_sound = pygame.mixer.Sound("bite_sound.wav")
    
    pygame.mixer.music.load("valkyries.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.5)

    # starting position, size, and velocity for the player character
    w = skull.get_width()
    h = skull.get_height()
    x = 0
    y = random.randint(0, height-w)
    yvel = 0

    #variables for key presses
    up = False
    down = False
    replay = False

    #variables for high scores
    score = 0
    dict = read_file()

    # create a list of burgers
    burgers = []
    missed_burgers = 0
    
    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0
    time = 0
    n = 1

    # initialize the player name
    name = ""

    ## INTRO SCREEN LOOP: This program uses a sequence of loops to go
    ## through an intro screen, the main game, and a game over screen.
    keepGoingIntro = True
    keepGoing = True
    keepGoingGameOver = True
    while (keepGoingIntro):

        dt = clock.tick()

        # Handle events     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoingIntro = False

            # During the intro screen, record the characters the
            # player types (he is inputting his player name). End the
            # intro phase when the player hits 'Enter'.
            elif event.type==pygame.KEYDOWN:
                if event.key >= 65 and event.key <= 122:
                    name += chr(event.key)
                elif event.key == 13:
                    keepGoingIntro = False

        # Draw picture and update display.
        my_win.fill(pygame.color.Color("darkgreen"))
        
        # draw the intro message
        label = myFont.render("Move the skull up and down with w and s to catch the burgers.", True, pygame.color.Color("black"))
        x3, y3 = 50, 50
        my_win.blit(label, (x3,y3))

        label = myFont.render("If you miss ten, you lose.", True, pygame.color.Color("black"))
        y3 += 45
        my_win.blit(label, (x3,y3))


        label = myFont.render("Please enter your name: "+name, True, pygame.color.Color("black"))
        y3 += 45
        my_win.blit(label, (x3,y3))

        label = myFont.render("Then hit 'Enter' to start.", True, pygame.color.Color("black"))
        y3 += 45
        my_win.blit(label, (x3,y3))

        pygame.display.update()
        
    ## The game loop starts here.
    while (keepGoing):
        dt = clock.tick(60)
        draw = random.randint(1,75)

        ## Handle events.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                keepGoing = False
                keepGoingGameOver = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "w":
                    up = True
                elif pygame.key.name(event.key) == "s":
                    down = True

            elif event.type == pygame.KEYUP:
                if pygame.key.name(event.key) == "w":
                    up = False
                elif pygame.key.name(event.key) == "s":
                    down = False

        #spawn burgers
        if keepGoing == True:
            burger = create_burger(width, height,w2)
            if len(burgers) < 5:
                if draw == 50:
                    burgers += [burger]
                
        ## Simulate game world
        # update velocity according to player input
        if up and not down:
            yvel = -7
        elif down and not up:
            yvel = 7
        else:
            yvel = 0

        if y <= 0:
            up = False
            y = 0
        if y >= height-h:
            down = False
            y = height-h

        # move burger/update burger position
        for burger in burgers:
            burger[X] = burger[X] + burger[XVEL]
            burger[Y] = burger[Y] + burger[YVEL]
 
        # make sure burger stays inside pygame window and update burger
        # velocity
        for burger in burgers:
            if (burger[X] > width - burger[WIDTH]):
                burger[X] = width - burger[WIDTH]
                burger[XVEL] = -1 * burger[XVEL]
            if (burger[Y] < burger[WIDTH]):
                burger[Y] = burger[WIDTH]
                burger[YVEL] = -1 * burger[YVEL]
            if (burger[Y] > height - burger[WIDTH]):
                burger[Y] = height - burger[WIDTH]
                burger[YVEL] = -1 * burger[YVEL]
        
        # move player character
        y += yvel

        # collision detection
        for burger in burgers:
            if burger[COLLIDE] == False:
                if (burger[Y]+burger[WIDTH]) < y:
                    burger[COLLIDE] = False
                elif burger[Y] > (y + (h-10)):
                    burger[COLLIDE] = False
                elif burger[X] > (x + w-5):
                    burger[COLLIDE] = False                    
                else:
                    burger[COLLIDE] = True
                    score += 1
                    bite_sound.play()
                    if burger[COLLIDE] == True:
                        burger[X] = width - w
                        burger[Y] = random.randint(w, height-w)
                        burger[COLLIDE] = False
            if burger[X] <= 0:
                missed_burgers += 1

        # variable speed
        if score >= 5*n:
            n+=1
            for burger in burgers:
                burger[XVEL]-=1
            burger[XVEL]-=1

        ## Draw picture and update display
        my_win.blit(flames,(0,0))
        
        msg = myFont.render(str(name)+": "+str(score), True, pygame.color.Color("darkgreen"))
        my_win.blit(msg, (20,height-40)) 

        msg = myFont.render("Missed: "+str(missed_burgers), True, pygame.color.Color("darkgreen"))
        my_win.blit(msg, (20,0))
        
        for burger in burgers:
            my_win.blit(hamburger, (burger[X],burger[Y]))
       
        my_win.blit(skull, (x,y))
                    
        burgers = filter_burgers(burgers)

        if missed_burgers >= 10:
            keepGoing = False

        pygame.display.update()

    #game over screen
    while (keepGoingGameOver):
        ## Handle events.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                keepGoingGameOver = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "r":
                    replay = True
            elif event.type == pygame.KEYUP:
                if pygame.key.name(event.key) == "r":
                    replay = False

        #deal with high scores                
        for key, value in dict.items():
            if name == key:
                if score > value:
                    dict[name] = score
            elif name not in dict.keys():
                dict[name] = score
      
        write_file(dict)
        scores = order_dict(dict)

        #draw game over screen with high scores and replay option
        my_win.fill(pygame.color.Color("black"))

        top_scores = myFont.render("Top Scores:", True, pygame.color.Color("darkgreen"))
        my_win.blit(top_scores, (width/2-50,height/2+20))        
        scores_first = myFont.render(str(scores[0]), True, pygame.color.Color("darkgreen"))
        my_win.blit(scores_first, (width/2-50,height/2+50))
        scores_second = myFont.render(str(scores[1]), True, pygame.color.Color("darkgreen"))
        my_win.blit(scores_second, (width/2-50,height/2+70))
        scores_third = myFont.render(str(scores[2]), True, pygame.color.Color("darkgreen"))
        my_win.blit(scores_third, (width/2-50,height/2+90))
        
        pygame.mixer.music.stop()
        end_msg = endFont.render("Game Over", True, pygame.color.Color("darkred"))
        my_win.blit(end_msg, (width/2-160,height/2-100))

        msg = myFont.render(str(name)+": "+str(score), True, pygame.color.Color("darkred"))
        my_win.blit(msg, (width/2-50,height/2-20))

        replay_msg = myFont.render("Press r to replay", True, pygame.color.Color("darkred"))
        my_win.blit(replay_msg, (width-250,height-40))

        #replay option
        if replay:
            run_game()

        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Call the function run_game.

run_game()
