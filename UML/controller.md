```mermaid
classDiagram
    class ControllerGame {
        new_game()(game: GameObject)
        update(game: GameObject, delta_time: float)
        check_collisions(game: GameObject, delta_time: float)
        save_game(game: GameObject)
        load_game()(game: GameObject)
    }

    class PlayerController {
        move(player: Player, direction: EnumObjectDirection, delta_time: float)
        shoot(bullet: Bullet)
    }

    class AlienController {
        update_movement(aliens: Alien, delta_time: float)
    }


    ControllerGame o-- GameObject : controls
    PlayerController o-- Player : controls
    AlienController o-- Alien : controls
  
```