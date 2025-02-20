import pygame
from typing import List
from models.Game import Game
from controllers.ControllerGame import ControllerGame
from controllers.ControllerPlayer import ControllerPlayer
from controllers.ControllerAlien import ControllerAlien
from controllers.ControllerBullet import ControllerBullet
from views.ComponentGameObject import ComponentGameObject
from views.ComponentBullet import ComponentBullet
from views.ComponentPlayer import ComponentPlayer
from views.ComponentAlien import ComponentAlien
from models.Enum.EnumObjectType import EnumObjectType
import time

class Main:

    def __init__(self):
        pygame.init()

        self.game = ControllerGame.new_game()
        self.controller = ControllerGame(self.game)
       
        self.screen_width = 480 # mapsize: 15 * 1 pixel cell: 32
        self.screen_height = 480
        self.cell_size = 32

        self.map_size = self.game.map_size
        self.screen_width = self.map_size[0] * self.cell_size
        self.screen_height = self.map_size[1] * self.cell_size

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.player_component: List[ComponentPlayer] = []
        self.alien_components: List[ComponentAlien] = []
        self.bullet_components: List[ComponentBullet] = []
#        self.game_components: List[ComponentGameObject] = [] 
        
        self.alien_controllers: List[ControllerAlien] = []

        for game_object in self.game.game_objects:
            if game_object.game_object_type == EnumObjectType.Player:
                self.player_component.append(ComponentPlayer(game_object))
            if game_object.game_object_type in (EnumObjectType.YellowAlien, 
                                                EnumObjectType.GreenAlien, 
                                                EnumObjectType.BlueAlien, 
                                                EnumObjectType.RedAlien):
                self.alien_controllers.append(ControllerAlien(game_object))
                self.alien_components.append(ComponentAlien(game_object))
                
        self.ufo_controller = None
        self.is_game_running = True
        self.show()

    def show(self):

        time_last = pygame.time.get_ticks()

        while self.is_game_running:
            delta_milisec = pygame.time.get_ticks() - time_last
            time_last = pygame.time.get_ticks()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for game_object in self.game.game_objects:
                            if game_object.game_object_type == EnumObjectType.Player:
                                ControllerPlayer.fire(game_object, self.game.game_objects, self.game) 
                    

            self.update(delta_milisec)

            self.draw()

            pygame.display.flip()
            time.sleep(0.01)

        pygame.quit()

    def update(self, delta_milisec):

        self.controller.update(delta_milisec)


        if self.controller.ufo and self.ufo_controller is None:
            self.ufo_controller = ControllerAlien(self.controller.ufo)
            component = ComponentAlien(self.controller.ufo)
            self.alien_components.append(component)

        if self.ufo_controller:
            self.ufo_controller.update_ufo(self.controller.ufo, self.game, delta_milisec)

        for controller in self.alien_controllers:
            if controller.alien in self.game.game_objects:
                controller.update(self.game, delta_milisec)
            else:
                self.alien_controllers.remove(controller)

        if not self.controller.ufo and self.ufo_controller:
            self.ufo_controller = None

        for game_object in self.game.game_objects:
            if game_object.game_object_type == EnumObjectType.Player:
                ControllerPlayer.update(game_object, self.game.game_objects, delta_milisec, self.game)

        for bullet in list(self.game.game_objects):
            if bullet.game_object_type == EnumObjectType.Bullet:
                ControllerBullet.update(bullet, self.game.game_objects, delta_milisec, self.game)
                component_exists = False
                for bullet_component in self.bullet_components:
                    if bullet_component.game_object == bullet:
                        component_exists = True
                        break
                if not component_exists:
                    self.bullet_components.append(ComponentBullet(bullet))
 
        for bullet_component in list(self.bullet_components):  
            if bullet_component.game_object not in self.game.game_objects:
                self.bullet_components.remove(bullet_component)

        


    def draw(self):
        self.screen.fill((0, 0, 0))
        for player in self.player_component:
            player.render(self.screen, self.cell_size)

        for component in list(self.alien_components):
            if component.game_object in self.game.game_objects:
                component.render(self.screen, self.cell_size)
            else:
                self.alien_components.remove(component)
        
        for bullet_component in self.bullet_components:
            bullet_component.render(self.screen, self.cell_size)
 
        if self.controller.ufo:
             for component in self.alien_components:
                if component.game_object == self.controller.ufo:
                    component.render(self.screen, self.cell_size)  

 #       for game_component in self.game_components:
 #           game_component.render(self.screen, self.cell_size) TODO shield

        font = pygame.font.Font(None , 30)
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10)) 


if __name__ == "__main__":
    main = Main()
