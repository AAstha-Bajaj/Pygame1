import pygame
import os   #helps to define the path to these images
pygame.font.init()
pygame.mixer.init()   #pygame librarry for sound effects

WIDTH, HEIGHT = 600, 450
WIN =pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("First Game!")
BORDER =pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Assets_Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VELOCITY = 5
BULLETS_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMG = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'spaceship_yellow.png')), 90)
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))


def drawWindow(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
#      WIN.fill((255, 255, 255))
     WIN.blit(SPACE, (0,0))
     pygame.draw.rect(WIN,BLACK, BORDER)

     red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
     yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
     WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
     WIN.blit(yellow_health_text,  (10, 10))

     WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
     WIN.blit(RED_SPACESHIP,(red.x, red.y))

     for bullet in red_bullets:
           pygame.draw.rect(WIN, RED, bullet)
     for bullet in yellow_bullets:
           pygame.draw.rect(WIN, YELLOW, bullet)

     pygame.display.update()


def yellowMovement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #left
            yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY +yellow.width < BORDER.x: #right
            yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY >0: #up
            yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT: #down
            yellow.y += VELOCITY


def redMovement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #left
            red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: #right
            red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY >0: #up
            red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT - 15: #down
            red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
      for bullet in yellow_bullets:
            bullet.x += BULLETS_VEL
            if red.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(RED_HIT))
                  yellow_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                  yellow_bullets.remove(bullet)
      
      for bullet in red_bullets:
            bullet.x -= BULLETS_VEL
            if yellow.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(YELLOW_HIT))
                  red_bullets.remove(bullet)
            elif bullet.x < 0:
                 red_bullets.remove(bullet) 


def drawWinner(text):
      draw_text = WINNER_FONT.render(text, 1, WHITE)
      WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
      pygame.display.update()
      pygame.time.delay(3000)


def main():
    red = pygame.Rect(500, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5


    clock = pygame.time.Clock()  #controls the speed of while loop
    run = True
    while run:
        clock.tick(FPS)   #sets a limit so it never go over this limit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                  if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                         bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                         red_bullets.append(bullet)
                         BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                  red_health -= 1
                  BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                  yellow_health -= 1
                  BULLET_HIT_SOUND.play() 
        
        winText = ""
        if red_health <= 0:
              winText = "Yellow wins!"
        if yellow_health <= 0:
              winText = "Red wins!"
        if winText != "":
            drawWinner(winText) 
            break                   

        keys_pressed = pygame.key.get_pressed()
        yellowMovement(keys_pressed, yellow)
        redMovement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        drawWindow(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()

if __name__=="__main__":
    main()
