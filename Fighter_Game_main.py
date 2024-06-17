import pygame
from Fighter_Game import Fighter
from pygame import mixer

mixer.init()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('BRAWLER - FIGHTING - GAME')

#Set framerate
clock = pygame.time.Clock()
FPS = 60

#Defining Colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

#Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0] #Player Score [P1,P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
#Define Fighter Variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#Loading Music and Sound effects
pygame.mixer.music.load('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\audio\\music.mp3')
pygame.mixer.music.play(-1,0.0,5000)
sword_fx = pygame.mixer.Sound('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\audio\\sword.wav')
magic_fx = pygame.mixer.Sound('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\audio\\magic.wav')
#Background Image
bg_image = pygame.image.load('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\images\\background\\background.jpg').convert_alpha()

#Loading Spritesheets
warrior_sheet = pygame.image.load('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\images\\warrior\\Sprites\\warrior.png').convert_alpha()
wizard_sheet = pygame.image.load('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\images\\wizard\\Sprites\\wizard.png').convert_alpha()

#Load the Victory image
victory_img = pygame.image.load('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\images\\icons\\victory.png').convert_alpha()

#Define Number of Steps in each animation
WARRIOR_ANIMATION_STEPS = [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS = [8,8,1,8,8,3,7]

#define font
count_font = pygame.font.Font('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\fonts\\turok.ttf',80)
score_font = pygame.font.Font('C:\\New E Drive Files\\Web Development Files\\Python Projects\\Brawler fighting Game\\brawler_tut-main\\assets\\fonts\\turok.ttf',30)

#Function for drawing text
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg,(0,0))
    
#To draw health bars of players
def draw_health_bar(health,x,y):
    ratio = health/100
    pygame.draw.rect(screen,WHITE,(x-2,y-2,404,34))
    pygame.draw.rect(screen, RED,(x,y, 400,30))
    pygame.draw.rect(screen,YELLOW,(x,y,400 *ratio,30))    

fighter_1 = Fighter(1,200,310,False,WARRIOR_DATA,warrior_sheet,WARRIOR_ANIMATION_STEPS,sword_fx)
fighter_2 = Fighter(2,700,310,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)



#Game Loop
run = True
while run:
    
    #Framerate of Players
    clock.tick(FPS)
    
    #Background Image
    draw_bg()
    
    #Drawing Health bars
    draw_health_bar(fighter_1.health,20,20)
    draw_health_bar(fighter_2.health,580,20)
    
    #Drawing Scores of Players
    draw_text("P1 : "+ str(score[0]),score_font,RED,20,60)
    draw_text("P2 : "+ str(score[1]),score_font,RED,580,60)
    
    #Update Countdown
    if intro_count<=0:
        #Moving Players
        fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_2,round_over)
        fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_1,round_over)
    else:
        #Display Count Timer
        draw_text(str(intro_count),count_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/3)
        #Update Count Timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -=1
            last_count_update = pygame.time.get_ticks()
                    
        
    #Update 
    fighter_1.update()
    fighter_2.update()
    
    #Drawing fighting players
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    #Check for Player Defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #Display The Victroy Image
        screen.blit(victory_img,(360,150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1,200,310,False,WARRIOR_DATA,warrior_sheet,WARRIOR_ANIMATION_STEPS,sword_fx)
            fighter_2 = Fighter(2,700,310,True,WIZARD_DATA,wizard_sheet,WIZARD_ANIMATION_STEPS,magic_fx)
    
    #Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
     
     
    pygame.display.update()        

#Quit Game 
pygame.quit()            
