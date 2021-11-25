import pygame, random
pygame.init()

WIDTH = 945
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Clown")



# Images
CLOWN_IMAGE = pygame.image.load('assets/clown.png')
BG = pygame.image.load('assets/background.png')


# Sound 
hit_sound = pygame.mixer.Sound('assets/click_sound.wav')
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(0.07)
hit_sound.set_volume(0.07)
pygame.mixer.music.load('assets/ctc_background_music.wav')
pygame.mixer.music.set_volume(0.1)


# Font
font = pygame.font.Font('assets/Franxurter.ttf', 40)

# Game constants
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VEL = 3
CLOWN_ACCELERATION = 0.5

# Colors
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)
PINK = (159, 43, 104)
GREEN = (34, 139, 34)

# Text
title_label = font.render('Catch the Clown', True, PINK)
game_over_text = font.render("GAME OVER", True, GREEN)
continue_text = font.render("Click anywhere to play again", True, GREEN)


# Action Handlers

class Clown:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
    
    def collusion(self, x, y):
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        return rect.collidepoint(x, y)
        

# Game variables
lives = PLAYER_STARTING_LIVES
score = 0

clown_vel = CLOWN_STARTING_VEL
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])
clown = Clown(WIDTH//2 - CLOWN_IMAGE.get_width()//2, HEIGHT//2 - CLOWN_IMAGE.get_height()//2, CLOWN_IMAGE)




run = True
FPS = 60
clock = pygame.time.Clock()


def redraw_screen():
    WIN.blit(BG, (0, 0))
    
    score_label = font.render(f'Score: {score}', True, BLUE)
    lives_label = font.render(f'Lives: {lives}', True, YELLOW)
    
    WIN.blit(score_label, (10, 10))
    WIN.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 10))
    WIN.blit(lives_label, (WIDTH - 10 - lives_label.get_width(), 10))
    
    clown.draw(WIN)
    
    
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    lives = PLAYER_STARTING_LIVES
                    clown_vel = CLOWN_STARTING_VEL
                    clown.x = WIDTH//2 - clown.img.get_width()//2
                    clown.y = HEIGHT//2 - clown.img.get_height()//2
                    prev_dx = clown_dx
                    prev_dy = clown_dy
                    while(prev_dx == clown_dx and prev_dy == clown_dy):
                        clown_dx = random.choice([-1, 1])
                        clown_dy = random.choice([-1, 1])
                    pygame.mixer.music.play(-1)
                    is_paused = False
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            
            if clown.collusion(mouse_x, mouse_y):
                hit_sound.play()
                score += 1
                clown_vel += CLOWN_ACCELERATION
                
                prev_dx = clown_dx
                prev_dy = clown_dy
                
                while(prev_dx == clown_dx and prev_dy == clown_dy):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
            else:
                miss_sound.play()
                lives -= 1
            
    # Clown moving
    clown.x += clown_dx * clown_vel
    clown.y += clown_dy * clown_vel
    
    if clown.x <= 0 or clown.x >= WIDTH - clown.img.get_width():
        clown_dx *= -1
    if clown.y <= 0 or clown.y >= HEIGHT - clown.img.get_height():
        clown_dy *= -1
            
            
pygame.quit()