import arcade
from ui import *
import arcade.gui
from arcade.gui import UIManager

GRAVITY = 0.75
PLAYER_JUMP_SPEED = 15
BOTTOM_VIEWPORT_MARGIN = 43
TOP_VIEWPORT_MARGIN = 43
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Flappy Bird Game"
CHARACTER_SCALING = 1


class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        super().__init__()
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None

    def setup(self):
        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        player_image_source = ":resources:images/space_shooter/meteorGrey_small1.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH/5
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)
        print(self.physics_engine)
        print(type(self.physics_engine))

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()

    def on_show_view(self):
        self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        pass

    def on_update(self, delta_time):
        self.physics_engine.update()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()