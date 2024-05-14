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
pygame.init()


class Game(pygame.sprite.Sprite):
    def __init__(self, video_path, image_background, image_player):
        """
        This is function for initialisation, here happening
        init Sprite with library pygame, set selfS, player speed
        and get rect from player.
        Also, class game inherired by 'pygame.sprite.Sprite'.
        """
        pygame.sprite.Sprite.__init__(self)
        self.video_path = video_path
        self.image_player = image_player
        self.image_background = image_background
        self.rect = image_player.get_rect()
        self.y_speed = 0
        self.x_speed = 0

    def start_loading(self):
        """
        This is code starting loading-screen, we are using
        for these libraries: pygame, moviepy.editor and PIL.
        Video put to centre, loading in variable clip, after:
        get seconds through division on 1000,
        transforms frame in type(format) PIL,
        transforms image to subsequence bytes,
        create place for image with pygame,
        and ultimately demonstrates video in positions
        (0, 0) through blit.
        """
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

    def start_game(self):
        """
        In this function we are starting game, it's working
        after update(), this includes the background image
        and player image, we put player in screen centre.
        We also play music here, and there is a loop that
        watches the key press a, w, s, d and esc.
        There is also check for borders.
        """
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Игровое окно')

        image_surface = pygame.image.load(self.image_background)
        screen.blit(image_surface, (0, 0))
        pygame.display.update()

        player_x = SCREEN_SIZE[0] // 2 - self.rect.width // 2
        player_y = SCREEN_SIZE[1] // 2 - self.rect.height // 2

        # Start music
        pygame.mixer.init()
        music_files = [
            os.path.join(CURRENT_FOLDER / 'game-music/Music-1.mp3'),
            os.path.join(CURRENT_FOLDER / 'game-music/Music-2.mp3')
        ]
        current_music_index = 0

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
                        if player_y > 0:  # проверка границы экрана сверху
                            player_y -= STEP_PIXELS
                    elif event.key == pygame.K_s:
                        if player_y < SCREEN_SIZE[1] - self.rect.height:  # проверка границы экрана снизу
                            player_y += STEP_PIXELS
                    elif event.key == pygame.K_d:
                        if player_x < SCREEN_SIZE[0] - self.rect.width:  # проверка границы экрана справа
                            player_x += STEP_PIXELS
                    elif event.key == pygame.K_a:
                        if player_x > 0:  # проверка границы экрана слева
                            player_x -= STEP_PIXELS

            player_x = max(0, min(player_x, SCREEN_SIZE[0] - self.rect.width))
            player_y = max(0, min(player_y, SCREEN_SIZE[1] - self.rect.height))

            print(f'{SCREEN_SIZE[0] = }')
            print(f'{SCREEN_SIZE[1] = }')

            print(f'{player_x = }')
            print(f'{player_y = }')

            print(f'{SCREEN_SIZE[0] - self.rect.width = }')
            print(f'{SCREEN_SIZE[1] - self.rect.height = }')

            screen.fill((0, 0, 0))
            screen.blit(image_surface, (0, 0))
            screen.blit(self.image_player, (player_x, player_y))
            pygame.display.update()
            if not pygame.mixer.music.get_busy():
                current_music_index = (current_music_index + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_music_index])
                pygame.mixer.music.play()

        # Stop music
        pygame.mixer.quit()
