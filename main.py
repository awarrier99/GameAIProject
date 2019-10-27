"""
Authors: Ashvin Warrier and James Lowe
"""
import settings

from Game import Game
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-nv', '--no-visuals', action='store_true', help='whether to show visual sensors for debugging')
    parser.add_argument('-ns', '--no-stats', action='store_true', help='whether to show stats in screen bottom right')
    parser.add_argument('-w', '--width', type=int, help='width of the game screen')
    parser.add_argument('-he', '--height', type=int, help='height of the game screen')
    parser.add_argument('-p', '--ppg', type=int, help='pixels per grid position')
    parser.add_argument('-f', '--fps', type=int, help='frames per second')
    parser.add_argument('-m', '--move-frames', type=int, help='number of frames to move for')
    parser.add_argument('-np', '--no-pathfinding', action='store_true', help='whether to run pathfinding')
    parser.add_argument('-a', '--ai', action='store_true', help='whether to run in AI mode')
    parser.add_argument('-d', '--dirty-rects', action='store_true', help='whether to use dirty rect rendering')
    config = vars(parser.parse_args())
    settings.init(config)
    game = Game()
    game.run()
