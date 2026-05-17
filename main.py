import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_HEIGHT
from old_main import keys_pressed, jump_sound_check
from player import Player
from obstacle import Obstacle

class SamuraiRun:
    def __init__(self):

        # SCREEN
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Samurai Run")

        # VARIABLES
        self.score = 0
        self.high_score = 0
        self.game_running = True
        self.gravity = GRAVITY
        self.jump_height = JUMP_HEIGHT
        self.game_state = "main_menu"
        self.background_image_x = 0
        self.paused = False
        self.jump_sound_check = True
        self.slide_sound_check = True
        self.speed = 10

        # PLAYER STATES
        self.run = Player(self, "assets/samurai_run.png", True)
        self.jump = Player(self,"assets/samurai_jump.png", False, "assets/jump_sound_2.wav")
        self.slide = Player(self, "assets/samurai_slide.png", False, "assets/slide_sound.mp3")

        # OBSTACLES
        self.obstacles = [
            Obstacle(self, "obstacle_images/blade_1.png", 1280),
            Obstacle(self, "obstacle_images/blade_2.png", 1280),
            Obstacle(self, "obstacle_images/blade_3.png", 1280),
            Obstacle(self, "spikes_1.png", 1280),
            Obstacle(self, "spikes_2.png", 1280),
            Obstacle(self, "swinging_blade.png", 1280, 0),
            Obstacle(self, "swinging_spike_block.png", 1280),
            Obstacle(self, "swinging_spike_block_2.png", 1280, 0),
            Obstacle(self, "swinging_spike_stick.png", 1280)
        ]
        self.active_obstacles = []

        # FONT
        self.font1 = pygame.font.Font(None, 200)
        self.font2 = pygame.font.Font(None, 50)
        self.font3 = pygame.font.Font(None, 75)

        # UI
        self.platform_rect = pygame.Rect(0, 520, 1280, 200)
        self.score_rect = pygame.Rect(870, 10, 400, 125)
        self.start_menu = pygame.image.load('assets/start_menu.png')
        self.pause_text = self.font1.render("PAUSED", True, (30, 30, 30))
        self.high_score_text = self.font2.render(f"High Score: {self.high_score}", True, (30, 30, 30))
        self.score_text = self.font2.render(f"Score: {self.score}", True, (30, 30, 30))
        self.background_image = pygame.image.load('assets/moving_background.png')
        self.game_over_text = self.font1.render("GAME OVER", True, (30, 30, 30))
        self.restart_text = self.font3.render("Press 'r' to restart", True, (30, 30, 30))

        # OTHER
        self.death_sound = pygame.mixer.Sound('assets/death_sound.wav')
        self.jump_sound = pygame.mixer.Sound('assets/jump_sound_2.wav')
        self.slide_sound = pygame.mixer.Sound('slide_sound.mp3')
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load("assets/backgroundmusic.wav")

    def update(self):
        player_input = pygame.key.get_pressed()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.game_state == "samurai_run":
                    self.paused = not self.paused
                    if self.paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        if self.game_state == "main_menu":
            if player_input[pygame.K_SPACE]:
                self.game_state = "samurai_run"
        elif self.game_state == "samurai_run":
            if player_input[pygame.K_SPACE]:
                self.jump.active = True
                self.run.active = False
                self.slide.active = False
                self.jump.update_rect(100, 80, self.jump.rect.x, self.jump.rect.y)
                if self.jump_sound_check:
                    self.jump.sound.play()
                    self.jump_sound_check = False
                    self.slide_sound_check = True
            if player_input[pygame.K_LCTRL] and not self.jump.active:
                self.jump.active = False
                self.run.active = True
                self.slide.active = False
                self.slide.update_rect(100, 50, self.slide.rect.x, self.slide.rect.y + 50)
                if self.slide_sound_check:
                    self.slide.sound.play()
                    self.slide_sound_check = False
                player_rect.y -= velocity
                velocity -= gravity
                if velocity < -jump_height:
                    velocity = jump_height
                    chr_jump = False
                    player_hitbox = player_rect.copy()
                    chr_run = True
                    jump_sound_check = True
            elif not self.jump.active:
                self.slide.active = False
                self.run.active = True
            for obstacle in self.active_obstacles:
                if obstacle.check_collision(self):
                    self.death_sound.play()
                    pygame.mixer.music.stop()
                    self.game_state = "restart_menu"
                obstacle.move(self.speed)


    def draw(self):
        if self.game_state == "main_menu":
            self.screen.blit(self.start_menu, (0, 0))
        elif self.game_state == "samurai_run":
            if self.paused:
                self.screen.blit(self.pause_text, (400, 200))
            else:
                self.screen.blit(self.background_image, (self.background_image_x, 0))
                self.screen.blit(self.background_image, (self.background_image_x + 1280, 0))
                pygame.draw.rect(self.screen, (122, 122, 122), self.platform_rect)
                for obstacle in self.active_obstacles:
                    obstacle.draw()
                pygame.draw.rect(self.screen, (122, 122, 122), self.score_rect)
                self.screen.blit(self.score_text, (900, 25))
                self.screen.blit(self.high_score_text, (900, 75))
                if self.run:
                    self.run.draw()
                elif self.jump:
                    self.jump.draw()
                elif self.slide:
                    self.slide.draw()
        elif self.game_state == "restart_menu":
            self.screen.blit(self.game_over_text, (0, 0))
            self.screen.blit(self.restart_text, (400, 350))
        pygame.display.flip()
        self.clock.tick(60)
