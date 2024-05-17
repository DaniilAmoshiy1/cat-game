import asyncio
import sys
import os

import pygame
from moviepy.editor import VideoFileClip
from PIL import Image

from constants import (
    SCREEN_SIZE,
    FPS,
    CURRENT_FOLDER,
    STEP_PIXELS,
    VIDEO_POSITION,
    BACKGROUND_POSITION,
    BLACK_FILL,
    SLEEPING_TIME_FOR_ASYNC
)


class Game(pygame.sprite.Sprite):
    """
    This is class Game which inherired by 'pygame.sprite.Sprite'.
    It has functions: '__init__' and 'start_game'
    They do not have a return command, so use outside
    the game is not recommended.
    """

    def __init__(self, video_path, image_background, image_player):
        """
        This is function for initialisation, here happening
        init Sprite through library pygame, set selfs
        and player speed.
        """
        pygame.sprite.Sprite.__init__(self)
        self.video_path = video_path
        self.image_player = image_player
        self.image_background = image_background
        self.rect = image_player.get_rect()
        self.y_speed = 0
        self.x_speed = 0
        self.video_finished = False



    async def start_game(self):
        """
        In this function we are starting game,
        code is here contains main loop for
        start screen loading,
        includes the background image
        and player image, we put player in screen centre.
        We play music here, also loop
        watches the key press a, w, s, d, buttons
        left and right for switch music, esc for
        close game and program close icon(cross).
        There is also check for borders.
        In this is code using only one loop,
        because it conition pygbag for create
        page.
        screen - set screen size.
        clip - take the video.
        player_x and player_y(in start) - set player position.
        current_music_index - this is index for play music,
        it created because type object
        where stored path to music 'list'.
        music_files - variable where stored path to music.
        running(default is True) - need for set loop
        on or off depending on conditions.
        video_started(False) - need for start loading before game.
        """
        print('Start working start_game()')
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Window for play')
        clock = pygame.time.Clock()

        clip = VideoFileClip(self.video_path)

        player_x = SCREEN_SIZE[0] // 2 - self.rect.width // 2
        player_y = SCREEN_SIZE[1] // 2 - self.rect.height // 2

        # Start music
        pygame.mixer.init()
        current_music_index = 0
        music_files = [
            os.path.join(CURRENT_FOLDER / 'game-music/Music-1.mp3'),
            os.path.join(CURRENT_FOLDER / 'game-music/Music-2.mp3'),
            os.path.join(CURRENT_FOLDER / 'game-music/Music-3.mp3'),
            os.path.join(CURRENT_FOLDER / 'game-music/Music-4.mp3'),
            os.path.join(CURRENT_FOLDER / 'game-music/Music-5.mp3')
        ]

        pygame.mixer.music.load(music_files[current_music_index])
        pygame.mixer.music.play()

        print('We are inside start_game.')

        running = True
        video_started = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Обработка события закрытия окна
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RIGHT:
                        current_music_index = (current_music_index + 1) % len(music_files)
                        pygame.mixer.music.load(music_files[current_music_index])
                        pygame.mixer.music.play()
                    elif event.key == pygame.K_LEFT:
                        current_music_index = (current_music_index - 1) % len(music_files)
                        pygame.mixer.music.load(music_files
                                                [current_music_index])
                        pygame.mixer.music.play()
            if not video_started:
                frame = clip.get_frame(pygame.time.get_ticks() / 1000)
                pil_image = Image.fromarray(frame)
                image_bytes = pil_image.tobytes()
                frame_surface = pygame.image.fromstring(image_bytes, pil_image.size, pil_image.mode)
                screen.blit(frame_surface, VIDEO_POSITION)
                pygame.display.update()

                if pygame.time.get_ticks() / 1000 >= clip.duration:
                    video_started = True

            else:
                image_surface = pygame.image.load(self.image_background)
                screen.blit(image_surface, BACKGROUND_POSITION)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    if player_y > 0:
                        player_y -= STEP_PIXELS
                if keys[pygame.K_s]:
                    if player_y < SCREEN_SIZE[1] - self.rect.height:
                        player_y += STEP_PIXELS
                if keys[pygame.K_d]:
                    if player_x < SCREEN_SIZE[0] - self.rect.width:
                        player_x += STEP_PIXELS
                if keys[pygame.K_a]:
                    if player_x > 0:
                        player_x -= STEP_PIXELS
                    # Switch music:

                # Check borders:
                player_x = max(0, min(player_x, SCREEN_SIZE[0] - self.rect.width))
                player_y = max(0, min(player_y, SCREEN_SIZE[1] - self.rect.height))

                # Check zone 'borders':
                # print(f'{SCREEN_SIZE[0] = }')
                # print(f'{SCREEN_SIZE[1] = }')
                #
                # print(f'{player_x = }')
                # print(f'{player_y = }')
                #
                # print(f'{SCREEN_SIZE[0] - self.rect.width = }')
                # print(f'{SCREEN_SIZE[1] - self.rect.height = }')

                screen.fill(BLACK_FILL)
                screen.blit(image_surface, BACKGROUND_POSITION)
                screen.blit(self.image_player, (player_x, player_y))
                pygame.display.update()

                if not pygame.mixer.music.get_busy():
                    current_music_index = (current_music_index + 1) % len(music_files)
                    pygame.mixer.music.load(music_files[current_music_index])
                    pygame.mixer.music.play()

            clock.tick(FPS)
            await asyncio.sleep(SLEEPING_TIME_FOR_ASYNC)

        # Stop music
        pygame.mixer.quit()
        print('Work start_game() completed')
