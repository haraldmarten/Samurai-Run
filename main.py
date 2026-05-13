import pygame
import random
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Samurai Run")

clock = pygame.time.Clock()

jump_sound = pygame.mixer.Sound('assets/jump_sound_2.wav')
jump_sound.set_volume(0.6)
jump_sound_check = True

slide_sound = pygame.mixer.Sound('assets/slide_sound.mp3')
slide_sound.set_volume(0.1)
slide_sound_check = True

pygame.mixer.music.load('assets/backgroundmusic.wav')
pygame.mixer.music.set_volume(0.5)

run_image = pygame.transform.scale(pygame.image.load("assets/samurai_run.png"), (100, 100))
jump_image = pygame.transform.scale(pygame.image.load("assets/samurai_jump.png"), (100, 100))
slide_image = pygame.transform.scale(pygame.image.load("assets/samurai_slide.png"), (100, 100))
background_image = pygame.image.load("assets/best_background.png")

font = pygame.font.Font(None, 200)
font2 = pygame.font.Font(None, 78)

obstacle_1 = pygame.Rect(1280, 0, 300, 450)
obstacle_2 = pygame.Rect(1280, 410, 160, 110)
obstacle_3 = pygame.Rect(1280, 300, 180, 220)
obstacle_4 = pygame.Rect(1280, 470, 60, 50)
obstacle_5 = pygame.Rect(1280, 450, 300, 70)
obstacle_6 = pygame.Rect(1280, 250, 100, 100)

obstacles = [obstacle_1, obstacle_2, obstacle_3, obstacle_4, obstacle_5, obstacle_6]
game_obstacles = []

player_rect = run_image.get_rect(bottom=725, right=500)
player_rect.y = 430
platform_rect = pygame.Rect(0, 520, 1280, 200)
player_hitbox = player_rect.copy()

chr_run = True
chr_jump = False
chr_slide = False

run = True

gravity = 1
jump_height = 25
velocity = jump_height
speed = 10

state_run = True
state_over = False
last_spawned = 0

score = 0

background_image_x = 0
score_rect = pygame.Rect(870, 25, 400, 100)

time_check_2 = 0

death_sound = pygame.mixer.Sound('assets/death_sound.wav')
music_stop_check = True

screen_state = True # Main menu --- False = Game

start_menu = pygame.image.load('assets/start_menu.png')

can_jump = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if screen_state:
        screen.blit(start_menu, (0,0))
        plyr_input_67 = pygame.key.get_pressed()
        if plyr_input_67[pygame.K_SPACE]:
            screen_state = False
            can_jump = True
    elif not screen_state:
        if not pygame.mixer.music.get_busy() and music_stop_check:
            pygame.mixer.music.play()
        score_text = font2.render(f"Score: {score}", True, (30, 30, 30))
        screen.blit(background_image, (background_image_x,0))
        screen.blit(background_image, (background_image_x + 1280,0))
        background_image_x -= .5
        if background_image_x <= -1280:
            background_image_x = 0
        pygame.draw.rect(screen, (122, 122, 122), platform_rect)
        current_time = pygame.time.get_ticks()
        if state_run and not state_over:
            time_rn = pygame.time.get_ticks()
            if time_rn - time_check_2 >= 10000:
                speed += 1
                time_check_2 = time_rn
            score += 1
            keys_pressed = pygame.key.get_pressed()
            # JUMP -----
            if keys_pressed[pygame.K_SPACE]:
                chr_jump = True
                chr_run = False
                chr_slide = False
                player_hitbox = pygame.Rect(player_rect.x + 30, player_rect.y + 30, player_rect.width - 40, player_rect.height - 40)
                if jump_sound_check:
                    jump_sound.play()
                    jump_sound_check = False
                    slide_sound_check = True

            # SLIDE -----
            if keys_pressed[pygame.K_LCTRL] and not chr_jump:
                chr_slide = True
                chr_jump = False
                chr_run = False
                player_hitbox = pygame.Rect(player_rect.x, player_rect.y + 50, player_rect.width, player_rect.height - 50)
                if slide_sound_check:
                    slide_sound.play()
                    slide_sound_check = False
            elif not chr_jump:
                chr_slide = False
                chr_run = True
                player_hitbox = player_rect.copy()
                slide_sound_check = True
            # OBSTACLES -----
            if current_time - last_spawned > 1000:
                rnd_obs = random.choice(obstacles)
                new_obs = rnd_obs.copy()
                game_obstacles.append(new_obs)
                last_spawned = current_time

            for obstacle in game_obstacles[:]:
                obstacle.x -= speed
                if obstacle.right <= 0:
                    game_obstacles.remove(obstacle)
            # HIT DETECTION ------
            if game_obstacles:
                if game_obstacles[0].colliderect(player_hitbox):
                    death_sound.play()
                    pygame.mixer.music.stop()
                    state_run = False
                    state_over = True
                    music_stop_check = False

            # DRAW ANIMATION -------
            if chr_run:
                screen.blit(run_image, player_rect)
            elif chr_jump:
                player_rect.y -= velocity
                velocity -= gravity
                if velocity < -jump_height:
                    velocity = jump_height
                    chr_jump = False
                    player_hitbox = player_rect.copy()
                    chr_run = True
                    jump_sound_check = True
                screen.blit(jump_image, player_rect)
            elif chr_slide:
                screen.blit(slide_image, player_rect)
            # DRAW OBSTACLE ------
            if game_obstacles:
                for obstacle in game_obstacles:
                    pygame.draw.rect(screen, (0,0,0), obstacle)
            pygame.draw.rect(screen, (122, 122, 122), score_rect)
            screen.blit(score_text, (900, 50))
        elif state_over:
            game_over_text = font.render("GAME OVER", True, (30, 30, 30))
            screen.blit(game_over_text, (200, 200))
            inputs = pygame.key.get_pressed()
            pygame.draw.rect(screen, (122, 122, 122), score_rect)
            screen.blit(score_text, (900, 50))
            r_text = font2.render("Press 'r' to restart", True, (30, 30, 30))
            screen.blit(r_text, (400 , 350))
            if inputs[pygame.K_r]:
                game_obstacles.clear()
                speed = 10
                velocity = jump_height
                chr_run = True
                chr_jump = False
                chr_slide = False
                player_rect.y = 430
                player_hitbox = player_rect.copy()
                last_spawned = pygame.time.get_ticks()
                state_run = True
                state_over = False
                score = 0
                jump_sound_check = True
                music_stop_check = True
    pygame.display.flip()
    clock.tick(60)

pygame.quit()