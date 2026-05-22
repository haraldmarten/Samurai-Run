import pygame
import random
pygame.init()

# -------------------- SCREEN --------------------
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Samurai Run")
clock = pygame.time.Clock()

# -------------------- SOUNDS --------------------
jump_sound = pygame.mixer.Sound('assets/jump_sound_2.wav')
jump_sound.set_volume(0.6)
jump_sound_check = True

slide_sound = pygame.mixer.Sound('assets/slide_sound.mp3')
slide_sound.set_volume(0.1)
slide_sound_check = True

death_sound = pygame.mixer.Sound('assets/death_sound.wav')

pygame.mixer.music.load('assets/backgroundmusic.wav')
pygame.mixer.music.set_volume(0.5)

music_stop_check = True
mute_check = False
music_playing = False

# -------------------- IMAGES --------------------
run_image = pygame.transform.scale(pygame.image.load("assets/samurai_run.png"), (100, 100))
jump_image = pygame.transform.scale(pygame.image.load("assets/samurai_jump.png"), (100, 100))
slide_image = pygame.transform.scale(pygame.image.load("assets/samurai_slide.png"), (100, 100))
background_image = pygame.image.load("assets/best_background.png")
start_menu = pygame.image.load('assets/start_menu.png')

# -------------------- FONTS --------------------
font = pygame.font.Font(None, 200)
font2 = pygame.font.Font(None, 50)
font3 = pygame.font.Font(None, 75)

pause_text = font.render("PAUSED", True, (30, 30, 30))

# -------------------- OBSTACLES --------------------
obstacle_1 = pygame.Rect(1280, 0, 300, 460)
obstacle_2 = pygame.Rect(1280, 310, 500, 150)
obstacle_3 = pygame.Rect(1280, 310, 200, 150)
obstacle_4 = pygame.Rect(1280, 300, 220, 220)
obstacle_5 = pygame.Rect(1300, 270, 50, 250)
obstacle_6 = pygame.Rect(1280, 470, 300, 50)
obstacle_7 = pygame.Rect(1280, 370, 150, 150)

obstacles = [obstacle_1, obstacle_2, obstacle_3, obstacle_4, obstacle_5, obstacle_6]
game_obstacles = []

# -------------------- PLATFORM --------------------
platform_rect = pygame.Rect(0, 520, 1280, 200)

# -------------------- PLAYER --------------------
player_rect = run_image.get_rect(bottom=725, right=500)
player_rect.y = 430
player_hitbox = player_rect.copy()

chr_run = True
chr_jump = False
chr_slide = False

# -------------------- GAME VARIABLES --------------------
run = True
paused = False

gravity = 1
jump_height = 25
velocity = jump_height
speed = 10

state_run = True
state_over = False
last_spawned = 0

score = 0
high_score = 0

background_image_x = 0
score_rect = pygame.Rect(870, 10, 400, 125)

time_check_2 = 0

screen_state = True
can_jump = False

# -------------------- LOOP --------------------
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            elif event.key == pygame.K_m:
                mute_check = not mute_check

                if mute_check:
                    pygame.mixer.music.set_volume(0)
                    jump_sound.set_volume(0)
                    slide_sound.set_volume(0)
                    death_sound.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(0.5)
                    jump_sound.set_volume(0.6)
                    slide_sound.set_volume(0.1)
                    death_sound.set_volume(1)

    # -------------------- PAUSE --------------------
    if paused:
        screen.blit(pause_text, (400, 200))

    # -------------------- MENU --------------------
    if screen_state:
        screen.blit(start_menu, (0, 0))
        plyr_input_67 = pygame.key.get_pressed()
        if plyr_input_67[pygame.K_SPACE]:
            screen_state = False
            can_jump = True

    # -------------------- GAME --------------------
    elif not screen_state and paused == False:

        if not mute_check:
            if not music_playing:
                pygame.mixer.music.play()
                music_playing = True

        high_score_text = font2.render(f"High Score: {high_score}", True, (30, 30, 30))
        score_text = font2.render(f"Score: {score}", True, (30, 30, 30))

        screen.blit(background_image, (background_image_x, 0))
        screen.blit(background_image, (background_image_x + 1280, 0))

        background_image_x -= .5
        if background_image_x <= -1280:
            background_image_x = 0

        pygame.draw.rect(screen, (122, 122, 122), platform_rect)

        current_time = pygame.time.get_ticks()

        # -------------------- RUNNING STATE --------------------
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
                player_hitbox = pygame.Rect(player_rect.x + 30, player_rect.y + 30,
                                            player_rect.width - 40, player_rect.height - 40)

                if jump_sound_check and not mute_check:
                    jump_sound.play()
                    jump_sound_check = False
                    slide_sound_check = True

            # SLIDE -----
            if keys_pressed[pygame.K_LCTRL] and not chr_jump:
                chr_slide = True
                chr_jump = False
                chr_run = False
                player_hitbox = pygame.Rect(player_rect.x, player_rect.y + 50,
                                            player_rect.width, player_rect.height - 50)

                if slide_sound_check and not mute_check:
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

            # HIT DETECTION -----
            if game_obstacles:
                if game_obstacles[0].colliderect(player_hitbox):
                    if not mute_check:
                        death_sound.play()

                    pygame.mixer.music.stop()

                    state_run = False
                    state_over = True
                    music_stop_check = False

            # DRAW PLAYER -----
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

            # DRAW OBSTACLES -----
            for obstacle in game_obstacles:
                pygame.draw.rect(screen, (0, 0, 0), obstacle)

            if score > high_score:
                high_score = score

            pygame.draw.rect(screen, (122, 122, 122), score_rect)
            screen.blit(score_text, (900, 25))
            screen.blit(high_score_text, (900, 75))

        # -------------------- GAME OVER --------------------
        elif state_over:

            if score > high_score:
                high_score = score

            game_over_text = font.render("GAME OVER", True, (30, 30, 30))
            screen.blit(game_over_text, (200, 200))

            inputs = pygame.key.get_pressed()

            pygame.draw.rect(screen, (122, 122, 122), score_rect)
            screen.blit(score_text, (900, 25))
            screen.blit(high_score_text, (900, 75))

            r_text = font3.render("Press 'r' to restart", True, (30, 30, 30))
            screen.blit(r_text, (400, 350))

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
                music_playing = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()