import pygame
from typing import List
from models.Game import Game
from controllers.ControllerGame import ControllerGame
from views.ComponentGameObject import ComponentGameObject
import time

class Main:

    def __init__(self):
        pygame.init()

        self.controller = ControllerGame()
        self.game = ControllerGame.new_game()
        self.screen_width = 480 # mapsize: 15 * 1 pixel cell: 32
        self.screen_height = 480
        self.cell_size = 32

        self.map_size = self.game.map_size
        self.screen_width = self.map_size[0] * self.cell_size
        self.screen_height = self.map_size[1] * self.cell_size

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.game_components: List[ComponentGameObject] = []
        for game_object in self.game.game_objects:
            self.game_components.append(ComponentGameObject(game_object))

        self.is_game_running = True
        self.show()

    def show(self):

        time_last = pygame.time.get_ticks()
        while self.is_game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_running = False

            # get delta seconds
#            time_current = pygame.time.get_ticks()
#            delta_milisec = time_current - time_last
#            time_last = time_current
#
#            self.update(delta_milisec)

            self.draw()

            pygame.display.flip()
#            time.sleep(0.01)

        pygame.quit()

    def update(self, delta_milisec):
        pass


    def draw(self):
        self.screen.fill((0, 0, 0))
        for game_component in self.game_components:
            game_component.render(self.screen, self.cell_size)

if __name__ == "__main__":
    main = Main()
