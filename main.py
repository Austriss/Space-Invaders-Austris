import pygame
from typing import List
import json
from loguru import logger
from models.Game import Game
from controllers.ControllerGame import ControllerGame
from controllers.ControllerPlayer import ControllerPlayer
from controllers.ControllerAlien import ControllerAlien
from controllers.ControllerBullet import ControllerBullet
from views.ComponentGameObject import ComponentGameObject
from views.ComponentBullet import ComponentBullet
from views.ComponentPlayer import ComponentPlayer
from views.ComponentAlien import ComponentAlien
from views.factories.GameObjectFactory import GameObjectFactory
from models.Enum.EnumObjectType import EnumObjectType
from models.Observer.Observer import Subject, Observer
from models.Enum.EnumObjectDirection import EnumObjectDirection
import time
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
CELL_SIZE = 32

class Main(Observer):

    def __init__(self):
        pygame.init()
        self.controller = ControllerGame.instance()
        self.player_controller = None
        self.game = self.controller.new_game() 
        logger.info("new game started")
        self.controller.attach(self)
        self.screen_width = self.game.get_map_width # mapsize: 15 * 1 pixel cell: 32
        self.screen_height = self.game.get_map_height
        self.cell_size = self.game.get_cell_size
        self.map_size = self.game.get_map_size
        self.screen_width = self.map_size[0] * self.cell_size
        self.screen_height = self.map_size[1] * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.player_component: List[ComponentPlayer] = []
        self.alien_components: List[ComponentAlien] = []
        self.bullet_components: List[ComponentBullet] = []
        self.alien_controllers: List[ControllerAlien] = []

        self.game_components()

        self.ufo_controller = None
        self.update_display()
        self._is_game_running = True
        self.game_paused = False
        self.show()


    def is_game_paused(self):
        return self.game_paused
    
    def set_resume_game(self):
        self.game_paused = False

    def set_game_paused(self):
        self.game_paused = True

    def is_game_running(self):
        return self._is_game_running
    
    def set_stop_game(self):
        self._is_game_running = False

    def update_display(self):
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.game.player_lives}", True, (255, 255, 255))
        self.score_text = score_text
        self.lives_text = lives_text

    def on_event(self, event):
        pass

    def show(self):
        time_last = pygame.time.get_ticks()

        while self.is_game_running():
            delta_milisec = pygame.time.get_ticks() - time_last
            time_last = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.set_stop_game()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for game_object in self.game.game_objects:
                            if game_object.game_object_type == EnumObjectType.Player:
                                self.player_controller.fire(game_object, self.game.game_objects, self.game) 
                    elif event.key == pygame.K_ESCAPE:
                        if not self.is_game_paused():
                            self.save_game()
                            self.set_game_paused()
                            logger.info("game paused and saved")
                    elif event.key == pygame.K_p:
                        if self.is_game_paused():
                            self.load_game()
                            self.set_resume_game()
                            self._is_game_running = True
                            time_last = pygame.time.get_ticks()
                            logger.info("Game Loaded and Resumed")
                            break

            if self.is_game_paused():
                self.draw_pause_screen()
                pygame.display.flip()
                continue

            if not self.game.is_game_over:
                self.game_loop_update(delta_milisec)
                self.draw()
                pygame.display.flip()
                time.sleep(0.01)
            else:
                self.draw()
                pygame.display.flip()

                gameover_loop = True
                while gameover_loop:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameover_loop = False
                            self.set_stop_game()
                        if event.type == pygame.KEYDOWN:
                            gameover_loop = False
                            self.set_stop_game()
                    time.sleep(0.01)

        logger.info("Quitted game")
        pygame.quit()



    def game_loop_update(self, delta_milisec):

        self.controller.update(delta_milisec)

        if self.controller.ufo and self.ufo_controller is None:
            self.ufo_controller = ControllerAlien(self.controller.ufo)
            component = ComponentAlien(self.controller.ufo)
            self.alien_components.append(component)

        if self.controller.ufo and self.ufo_controller:
            self.ufo_controller.update_ufo(self.controller.ufo, self.game, delta_milisec)

        for controller in self.alien_controllers:
            if controller.get_alien() in self.game.game_objects:
                controller.game_update(self.game, delta_milisec)
            else:
                self.alien_controllers.remove(controller)

        if not self.controller.ufo and self.ufo_controller:
            self.ufo_controller = None

        for game_object in self.game.game_objects:
            if game_object.game_object_type == EnumObjectType.Player:
                ControllerPlayer.update(game_object, self.game.game_objects, delta_milisec, self.game)

        for bullet in list(self.game.game_objects):
            if bullet.game_object_type == EnumObjectType.Bullet or bullet.game_object_type == EnumObjectType.AlienBullet:
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
        if not self.game.is_game_over:
            self.screen.fill((0, 0, 0))
            self.update_display()
            for component in self.player_component: 
                if component.game_object in self.game.game_objects:
                    component.render(self.screen, self.cell_size)

            for component in list(self.alien_components):
                if component.game_object in self.game.game_objects:
                    component.render(self.screen, self.cell_size)
                else:
                    self.alien_components.remove(component)
            
            for bullet_component in self.bullet_components:
                if (bullet_component.game_object.game_object_type == EnumObjectType.Bullet or
        bullet_component.game_object.game_object_type == EnumObjectType.AlienBullet):
                    bullet_component.render(self.screen, self.cell_size)
    
            if self.controller.ufo:
                for component in self.alien_components:
                    if component.game_object == self.controller.ufo:
                        component.render(self.screen, self.cell_size)  

    #       for game_component in self.game_components:
    #           game_component.render(self.screen, self.cell_size) TODO shield

            if self.score_text:
                self.screen.blit(self.score_text, (10, 10))
            if self.lives_text:
                self.screen.blit(self.lives_text, (120, 10))
        #GameOver screen
        else:
            logger.info("game over!")
            self.draw_gameover_screen()


    def draw_pause_screen(self):
        font = pygame.font.Font(None, 74)
        pause_text = font.render("Game paused", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(pause_text, text_rect)

    def draw_gameover_screen(self):
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render("game over", True, (255, 0, 0))
        gameover_center = game_over_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(game_over_text, gameover_center)
        score_font = pygame.font.Font(None, 74)
        score_text = score_font.render(f"score: {self.game.score}", True, (255, 0, 0))
        score_center = score_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 50))
        self.screen.blit(score_text, score_center)

    def game_components(self):
        self.player_component: List[ComponentPlayer] = [] 
        self.alien_components: List[ComponentAlien] = []
        self.bullet_components: List[ComponentBullet] = []
        self.alien_controllers: List[ControllerAlien] = []
        self.ufo_controller = None

        for game_object in self.game.game_objects:
            if game_object.game_object_type == EnumObjectType.Player:
                self.player_component.append(ComponentPlayer(game_object))
                self.player_controller = ControllerPlayer()
            if game_object.game_object_type in (EnumObjectType.YellowAlien, 
                                                EnumObjectType.GreenAlien, 
                                                EnumObjectType.BlueAlien, 
                                                EnumObjectType.RedAlien):
                alien_controller = ControllerAlien(game_object) 
                self.alien_controllers.append(alien_controller) 
                self.controller.attach(alien_controller) 
                self.alien_components.append(ComponentAlien(game_object))        


    def save_game(self):
        game_state = {
            "score": self.game.score,
            "player_lives": self.game.player_lives,
            "is_game_over": self.game.is_game_over,
            "game_objects": []
        }
        for game_object in self.game.game_objects:
            data = {
                "object_type": game_object.game_object_type.value,
                "position": game_object.position,
                "direction": game_object.direction.value
            }
            game_state["game_objects"].append(data)

        with open("savegame.json", "w") as f:
            json.dump(game_state, f, indent=4)
        logger.info("Game saved")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                game_state = json.load(f)
            self.game.is_game_over = game_state["is_game_over"]
            self.game.score = game_state["score"]
            self.game.player_lives = game_state["player_lives"]
            self.game.game_objects = []

            factory = GameObjectFactory()

            for data_object in game_state["game_objects"]:
                enum_object_type = EnumObjectType(data_object["object_type"])
                enum_direction = EnumObjectDirection(data_object["direction"])
                game_object = factory.create_game_object(
                    object_type=enum_object_type,
                    position=tuple(data_object["position"]),
                    direction=enum_direction)
                self.game.game_objects.append(game_object)

            self.game_components()
            self.controller.set_game(self.game)
        except:
            logger.exception("savegame not found, starting new game")
            self.game = self.controller.new_game()
            self.game_components()
            self.controller.set_game(self.game)


if __name__ == "__main__":
    main = Main()
