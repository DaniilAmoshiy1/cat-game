import os
import pygame
from pathlib import Path

import game
CURRENT_FOLDER = Path(__file__).parent


def main():
    video_path = os.path.join(CURRENT_FOLDER / "My-game-pictures/loading-line.mp4")
    image_background = os.path.join(CURRENT_FOLDER / "My-game-pictures/roads in nature.jpg")
    image_player = pygame.image.load(CURRENT_FOLDER / 'My-game-pictures/Player-cat.png')
    player = game.Game(video_path, image_background, image_player)
    image_player.set_colorkey((255, 255, 255))
    player.start_loading()
    player.start_game()
    return


if __name__ == '__main__':
    main()
