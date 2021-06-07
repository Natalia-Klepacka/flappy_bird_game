import arcade
from ui import *
import arcade.gui
from arcade.gui import UIManager
import random

GRAVITY = 1500

PLAYER_DAMPING = 0.4
DEFAULT_DAMPING = 1.0

PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

PLAYER_MASS = 2.0

PLAYER_MAX_HORIZONTAL_SPEED = 0
PLAYER_MAX_VERTICAL_SPEED = 1600

PLAYER_JUMP_IMPULSE = 1500
BOTTOM_VIEWPORT_MARGIN = 43
TOP_VIEWPORT_MARGIN = 43

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Flappy Bird Game"
CHARACTER_SCALING = 1
PIPE_SCALING = 1
PIPE_SPEED = -5


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
        self.clock = None

    def setup(self):
        self.clock = 0
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

        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, -GRAVITY))
        self.physics_engine.add_sprite(self.player_sprite,
                                       damping=PLAYER_DAMPING,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.wall_list.draw()

    def on_show_view(self):
        self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            impulse = (0, PLAYER_JUMP_IMPULSE)
            self.physics_engine.apply_impulse(self.player_sprite, impulse)

    def on_key_release(self, key, modifiers):
        pass

    def generate_pipe(self):
        bottom_length = random.randint(1, 16)
        gap_length = random.randint(5, 8)
        top_length = 25 - bottom_length - gap_length
        bottom_image_name = "graphics/pipe" + str(bottom_length) + ".png"
        top_image_name = "graphics/pipe" + str(top_length) + ".png"
        bottom_center = bottom_length * 13
        top_center = SCREEN_HEIGHT - top_length * 13
        gap_center = bottom_length * 26 + gap_length * 13
        bottom_pipe = arcade.Sprite(bottom_image_name, PIPE_SCALING)
        bottom_pipe.center_x = SCREEN_WIDTH - 40
        bottom_pipe.center_y = bottom_center
        bottom_pipe.change_y = 0
        self.wall_list.append(bottom_pipe)
        self.physics_engine.add_sprite(bottom_pipe,
                                       collision_type="wall",
                                       body_type=arcade.PymunkPhysicsEngine.KINEMATIC)
        top_pipe = arcade.Sprite(top_image_name, PIPE_SCALING)
        top_pipe.center_x = SCREEN_WIDTH - 40
        top_pipe.center_y = top_center
        bottom_pipe.change_x = 5
        self.wall_list.append(top_pipe)
        self.physics_engine.add_sprite(top_pipe,
                                       collision_type="wall",
                                       body_type=arcade.PymunkPhysicsEngine.KINEMATIC)
        bottom_pipe.draw()
        top_pipe.draw()

    def on_update(self, delta_time):
        if self.clock == 180:
            self.generate_pipe()
            self.clock = 0
        self.physics_engine.step()
        self.clock += 1
        pipes_velocity = (PIPE_SPEED * 1 / delta_time, 0)
        for pipe in self.wall_list:
            self.physics_engine.set_velocity(pipe, pipes_velocity)
            if pipe.center_x < -40:
                pipe.remove_from_sprite_lists()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()