import pygame, random

pygame.init()


WIDTH = 1000
HEIGHT = 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feed the Dragon")



# Images
DRAGON_IMAGE = pygame.image.load('assets/dragon_right.png')
COIN_IMAGE = pygame.image.load('assets/coin.png')


# Colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Fonts
font = pygame.font.Font('assets/AttackGraffiti.ttf', 32)


# Sounds 
coin_sound = pygame.mixer.Sound('assets/coin_sound.wav')
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(0.03)
coin_sound.set_volume(0.1)
pygame.mixer.music.load('assets/ftd_background_music.wav')
pygame.mixer.music.set_volume(0.08)





def collide(obj1, obj2):
      offset_x = obj2.x - obj1.x
      offset_y = obj2.y - obj1.y
      return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class Coin():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
    def off_screen(self):
        return self.x < 0
    
    def collusion(self, player):
        if collide(self, player):
            return True
        

class Player():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


def generate_new_coin():
    return Coin(WIDTH + BUFFER_DISTANCE, random.randint(64, HEIGHT - 64), COIN_IMAGE)



# Game Value
run = True
FPS = 60
clock = pygame.time.Clock()

STARING_LIVES = 5
PLAYER_STARING_VEL = 5
COIN_STARTING_VEL = 5
COIN_ACCELERATION = 0.35
PLAYER_ACCELERATION = 0.08
BUFFER_DISTANCE = 100

score = 0
lives = STARING_LIVES
coin_vel = COIN_STARTING_VEL
player_vel = PLAYER_STARING_VEL

player = Player(20, HEIGHT//2, DRAGON_IMAGE)
current_coin = generate_new_coin()



# Texts
title_label = font.render("Feed the Dragon", True, GREEN, WHITE)

game_over_text = font.render("GAME OVER", True, GREEN)
continue_text = font.render("Press any key to play again", True, GREEN)



def redraw_screen():
    WIN.fill(BLACK)

    
    score_label = font.render(f"Score: {score}", True, GREEN)
    lives_label = font.render(f"Lives: {lives}", True, GREEN)
    
    
    WIN.blit(score_label, (10, 10))
    WIN.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 10))
    WIN.blit(lives_label, (WIDTH - 10 - lives_label.get_width(), 10))
    pygame.draw.line(WIN, WHITE, (0, 64), (WIDTH, 64), 2)
    
    
    player.draw(WIN)
    current_coin.draw(WIN)
    
    
    pygame.display.update()
    
    

pygame.mixer.music.play(-1)
while run:
    clock.tick(FPS)
    redraw_screen()
    
    if lives == 0:
        WIN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
        WIN.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 32 - continue_text.get_height()//2))
        pygame.display.update()
        

        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    score = 0
                    lives = STARING_LIVES
                    player_vel = PLAYER_STARING_VEL
                    coin_vel = COIN_STARTING_VEL
                    pygame.mixer.music.play(-1)
                    is_paused = False
                

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.y - player_vel > 64:
        player.y -= player_vel
    if keys[pygame.K_DOWN] and player.y + player_vel < HEIGHT - 64:
         player.y += player_vel
         
         
    # Coin Actions
    if current_coin.off_screen():
        lives -= 1
        miss_sound.play()
        current_coin = generate_new_coin()
        coin_vel += COIN_ACCELERATION
        player_vel += PLAYER_ACCELERATION    
    else:
        current_coin.x -= coin_vel
        
    if current_coin.collusion(player):
        score += 1
        coin_sound.play()
        current_coin = generate_new_coin()
        coin_vel += COIN_ACCELERATION
        player_vel += PLAYER_ACCELERATION
                   
            
pygame.quit()