
import pygame
import random
import math

def distance (x1, y1, x2, y2):
    """Calculates the distance between two points (x1, y1) and
    (x2,y2)."""
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

WIDTH = 0
X = 1
Y = 2
XVEL = 3
YVEL = 4
COLOR = 5
COLLIDE = 6
HEIGHT = 7

def create_burger(width, height,w2,):
   
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

def run_game():
    
    ## Initialize the pygame submodules and set up the display window.
    pygame.init()
    
    flames = pygame.image.load("Flames.png")
    
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
   
    up = False
    down = False
    left = False
    right = False

    score = 0

    # pictures and sound
   

    # create a list of balls
    burgers = []
    missed_burgers = 0
    
    ## setting up the clock
    clock = pygame.time.Clock()
    dt = 0
    time = 0
    n = 1
    
    ## The game loop starts here.
    keepGoing = True    
    while (keepGoing):
        dt = clock.tick(60)
        draw = random.randint(1,75)

        ## Handle events.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                keepGoing = False
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
        if y >= height-w:
            down = False

        # move circle/update circle position
        for burger in burgers:
            burger[X] = burger[X] + burger[XVEL]
            burger[Y] = burger[Y] + burger[YVEL]
 
        # make sure circle stays inside pygame window and update circle
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

        if score == 5*n:
            n+=1
            for burger in burgers:
                
                burger[XVEL]-=1 
                

        ## Draw picture and update display
        my_win.blit(flames,(0,0))
        
        msg = myFont.render("Your score: "+str(score), True, pygame.color.Color("green"))
        my_win.blit(msg, (20,height-40)) 

        msg = myFont.render("Missed: "+str(missed_burgers), True, pygame.color.Color("green"))
        my_win.blit(msg, (20,0))
        
        for burger in burgers:
            my_win.blit(hamburger, (burger[X],burger[Y]))

       
        my_win.blit(skull, (x,y))
                    
        burgers = filter_burgers(burgers)

        if missed_burgers > 9:
            my_win.fill(pygame.color.Color("black"))
            end_msg = endFont.render("Game Over", True, pygame.color.Color("darkred"))
            my_win.blit(end_msg, (width/2-160,height/2-30))
            
        pygame.display.update()

    ## The game loop ends here.

    pygame.quit()


## Call the function run_game.

run_game()
