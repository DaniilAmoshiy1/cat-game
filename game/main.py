import asyncio
import os

import game


if __name__ == '__main__':
    video_path = os.path.join("My-game-pictures", "loading-line.mp4")
    image_background = os.path.join("My-game-pictures", "roads in nature.jpg")
    image_player = os.path.join("My-game-pictures", "Player-cat.png")
    player = game.Game(video_path, image_background, image_player)
    asyncio.run(player.start_loading())
    asyncio.run(player.update())
    asyncio.run(player.start_game())
