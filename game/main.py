import asyncio
import os
import pygame

from game import Game
from constants import (
    CURRENT_FOLDER,
    INVISIBLE_COLOR
)


async def main():
    """
    This is function mothing return.
    Need for start game and can start only from
    'main.py'.
    video_path - path to loading-video
    image_background - path to background image
    image_player - loading the player through pygame, since
    after that I sat the color which should be transparent.
    because
    """
    print('Start main()')
    video_path = (os.path.join
                  (CURRENT_FOLDER / 'My-game-pictures/loading-line.mp4'))
    image_background = (os.path.join
                        (CURRENT_FOLDER / 'My-game-pictures/roads in nature.jpg'))
    image_player = (pygame.image.load
                    (CURRENT_FOLDER / 'My-game-pictures/Player-cat.png'))
    player = Game(video_path, image_background, image_player)
    image_player.set_colorkey(INVISIBLE_COLOR)
    await player.start_game()
    print('Function main() completed')


if __name__ == '__main__':
    asyncio.run(main())
