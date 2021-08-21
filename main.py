import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900)) 

def create_pipe():
    random_pipe_pos = random.choice(pipe_hight)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe
    
   
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5 
    return pipes


def draw_pipes(pipes):
     for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False ,True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            can_score = True            
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True        
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movment*3 ,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    score_surface = game_font.render(str(score), True, (255,255,255))
    score_rect = score_surface.get_rect(center = (288,100))
    screen.blit(score_surface, score_rect)

def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score == True:
                score += 1
                can_score = False
            if pipe.centerx > 105 :
                can_score = True
                



pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_active = False
game_font = pygame.font.Font('04b_19.ttf',40)
score = 0
can_score = True


#Game Variables
gravity = 0.25
bird_movment = 0
game_active = True
#bg
bg_surface = pygame.image.load('images/bg1.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
#floor
floor_surface = pygame.image.load('images/floor.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0
#bird
# bird_suface = pygame.image.load('images/red_bird_mid_flap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_suface)
# bird_rect = bird_surface.get_rect(center= (100, 512))
bird_doewflap = pygame.transform.scale2x(pygame.image.load('images/red_bird_down_flap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('images/red_bird_mid_flap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('images/red_bird_up_flap.png').convert_alpha())
bird_frames = [bird_doewflap, bird_midflap, bird_up]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center= (100, 512))  

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
#pipe
pipe_surface = pygame.image.load('images/pipe_green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_hight = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('images/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center= (288, 512))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movment = 0
                bird_movment -= 9

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                score = 0
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movment = 0

        if event.type == SPAWNPIPE: 
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2 :
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,  bird_rect = bird_animation()


    screen.blit(bg_surface, (0,0))
    if game_active == True:
        #bird
        bird_movment += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movment
        screen.blit(rotated_bird, bird_rect)
        floor_x_pos -= 1
        game_active = check_collision(pipe_list)
        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()
        score_display()
    else:
        screen.blit(game_over_surface, game_over_rect)

    #floor
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)