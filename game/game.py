import asyncio
import sys
import os

import pygame
from moviepy.editor import VideoFileClip
from PIL import Image
from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent
FPS = 50
SCREEN_SIZE = (1280, 720)
STEP_PIXELS = 50


class Game(pygame.sprite.Sprite):
    def __init__(self, video_path, image_background, image_player):
        pygame.display.set_mode((1280, 720))
        self.video_path = video_path
        self.image_background = image_background
        self.image_player = image_player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(CURRENT_FOLDER / 'My-game-pictures/Player-cat.png')  # .convert()
        self.rect = self.image.get_rect()
        self.y_speed = 0
        self.x_speed = 0


        self.scene = pygame.display.get_surface().get_rect()
        print(f'area bottom = {self.scene.bottom}')
        self.rect.centerx = self.scene.centerx
        self.rect.y = 100
        self.rect.centerx = self.scene.centerx
        self.rect.x = 100
        self.rect.centerx = self.scene.centerx

    async def update(self):
        # Проверьте, пересекается ли персонаж с границами сцены
        if not self.rect.colliderect(self.scene):
            # Если персонаж выходит за границы сцены, выполните необходимые действия
            if self.rect.bottom > self.scene.bottom or self.rect.top < self.scene.top:
                self.y_speed *= -1
                self.rect.y += self.y_speed

            if self.rect.left < self.scene.left or self.rect.right > self.scene.right:
                self.x_speed *= -1
                self.rect.x += self.x_speed

                if self.y_speed < 0:
                    self.y_speed += 0.2

    async def start_loading(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Воспроизведение видео')
        clock = pygame.time.Clock()

        scene = screen.get_rect()
        print(f'area bottom = {scene.bottom}')
        self.rect.centerx = scene.centerx
        self.rect.y = 100
        self.rect.x = 100

        # Загрузка видеофайла
        clip = VideoFileClip(self.video_path)

        print('We are inside start_loading.')

        running = True
        while running:
            for event in pygame.event.get():
                if not event.type == pygame.KEYUP:
                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

            frame = clip.get_frame(pygame.time.get_ticks() / 1000)
            pil_image = Image.fromarray(frame)
            image_bytes = pil_image.tobytes()
            frame_surface = pygame.image.fromstring(image_bytes, pil_image.size, pil_image.mode)
            screen.blit(frame_surface, (0, 0))

            pygame.display.update()

            if pygame.time.get_ticks() / 1000 >= clip.duration:
                print('We are leaving start_loading')
                break

            clock.tick(FPS)
            await asyncio.sleep(0)


    async def start_game(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Игровое окно')

        self.scene = screen.get_rect()

        image_surface = pygame.image.load(self.image_background)
        screen.blit(image_surface, (0, 0))
        pygame.display.update()
        player_x = 0
        player_y = 0
        player = pygame.image.load(self.image_player)
        player.set_colorkey((255, 255, 255))
        screen.blit(player, (player_x, player_y))
        pygame.display.update()


        # Start music
        pygame.mixer.init()
        music_files = [
            os.path.join('game-music', 'Music-1.mp3'),
            os.path.join('game-music', 'Music-2.mp3')
        ]
        current_music_index = 1
        if not pygame.mixer.get_busy():
            current_music_index = (current_music_index + 1) % len(music_files)
            music_file = music_files[current_music_index]
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()

        print('We are inside start_game.')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_w:
                        player_y -= STEP_PIXELS
                    elif event.key == pygame.K_s:
                        player_y += STEP_PIXELS
                    elif event.key == pygame.K_d:
                        player_x += STEP_PIXELS
                    elif event.key == pygame.K_a:
                        player_x -= STEP_PIXELS
                # elif event.type == pygame.KEYUP:
                #     if event.key in (pygame.K_w, pygame.K_s):
                #         self.y_speed = 0
                #     elif event.key in (pygame.K_a, pygame.K_d):
                #         self.x_speed = 0
            #
            # player_x += self.x_speed
            # player_y += self.y_speed

            screen.fill((0, 0, 0))
            screen.blit(image_surface, (0, 0))
            screen.blit(player, (player_x, player_y))
            pygame.display.update()

        # Stop music
        pygame.mixer.quit()