import arcade
import ui
import arcade.gui
from arcade.gui import UIManager
import random
import csv
from time import sleep

GRAVITY = 1
PLAYER_JUMP_SPEED = 15
BOTTOM_JUMP_SPEED = 3
TOP_JUMP_SPEED = -3

CHARACTER_SCALING = 1
PIPE_SCALING = 1
COIN_SCALING = 0.5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Flappy Bird Game"


class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self, mode):
        super().__init__()
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.physics_engine_player = None
        self.clock = None
        self.lives = None
        self.seconds = None
        self.points = None
        self.mode = mode
        self.vars = {}

    def setup(self):
        self.points = 0
        self.clock = 0
        self.lives = 3
        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)

        if self.mode == "easy":
            file_name = "easy.csv"
        elif self.mode == "hard":
            file_name = "hard.csv"
        with open(file_name, "r") as hardmode_file:
            csvreader = csv.reader(hardmode_file)
            for row in csvreader:
                if row and not row[0] == 'var':
                    self.vars[row[0]] = int(row[1])
            print(self.vars)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        player_image_source = ":resources:images/space_shooter/meteorGrey_small1.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH/5
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             arcade.SpriteList(),
                                                             gravity_constant=GRAVITY)

    def wall_hit(self):
        self.lives -= 1
        if not self.lives:
            game_over_view = ui.GameOverView(self.points, self.mode)
            self.window.show_view(game_over_view)
        else:
            self.clock = 0
            self.player_sprite.center_x = SCREEN_WIDTH/5
            self.player_sprite.center_y = SCREEN_HEIGHT/2
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            for pipe in self.wall_list[:]:
                pipe.remove_from_sprite_lists()
            for coin in self.coin_list[:]:
                coin.remove_from_sprite_lists()
            for i in range(1, 4):
                pass
                # self.on_restart(i)
                # sleep(1)

    #def on_restart(self, number):
     #   arcade.start_render()
      #  self.player_list.draw()
       # self.wall_list.draw()
        #arcade.draw_text(str(number),
         #                SCREEN_WIDTH / 2 - 300,
          #               SCREEN_HEIGHT / 2,
           #              color=arcade.color.WHITE,
            #             font_size=50,
             #            width=600,
              #           align='center')

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        score_text = f"SCORE: {self.points}\nLIVES: {self.lives}"
        arcade.draw_text(score_text,
                         SCREEN_WIDTH - 100,
                         SCREEN_HEIGHT - 40,
                         arcade.color.WHITE,
                         18)

    def on_show_view(self):
        self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.SPACE:
            view = StartView(self.mode)
            view.setup()
            self.window.show_view(view)

    def on_key_release(self, key, modifiers):
        pass

    def generate_pipe(self):
        bottom_length = random.randint(1, self.vars["MAX_BOTTOM_LENGTH"])
        gap_length = random.randint(self.vars["MIN_GAP_LENGTH"], self.vars["MAX_GAP_LENGTH"])
        top_length = 25 - bottom_length - gap_length
        bottom_image_name = "graphics/pipe" + str(bottom_length) + ".png"
        top_image_name = "graphics/pipe" + str(top_length) + ".png"
        bottom_center = bottom_length * 13
        top_center = SCREEN_HEIGHT - top_length * 13
        gap_center = bottom_length * 26 + gap_length * 13

        bottom_pipe = arcade.Sprite(bottom_image_name, PIPE_SCALING)
        bottom_pipe.center_x = SCREEN_WIDTH + 40
        bottom_pipe.center_y = bottom_center
        bottom_pipe.change_x = self.vars["PIPE_SPEED"]
        self.wall_list.append(bottom_pipe)
        bottom_pipe.draw()

        top_pipe = arcade.Sprite(top_image_name, PIPE_SCALING)
        top_pipe.center_x = SCREEN_WIDTH + 40
        top_pipe.center_y = top_center
        top_pipe.change_x = self.vars["PIPE_SPEED"]
        self.wall_list.append(top_pipe)
        top_pipe.draw()

        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = SCREEN_WIDTH + 40
        coin.center_y = gap_center
        coin.change_x = self.vars["PIPE_SPEED"]
        self.coin_list.append(coin)

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        if self.clock == self.vars["PIPES_FREQUENCY"]:
            self.generate_pipe()
            self.clock = 0
        self.physics_engine.update()
        self.wall_list.update()
        self.coin_list.update()
        self.clock += 1
        for pipe in self.wall_list[:]:
            if pipe.center_x < -40:
                pipe.remove_from_sprite_lists()
        for coin in self.coin_list[:]:
            if coin.center_x < -40:
                coin.remove_from_sprite_lists()
        if self.player_sprite.bottom <= 0:
            self.player_sprite.change_y = BOTTOM_JUMP_SPEED
        if self.player_sprite.top >= SCREEN_HEIGHT:
            self.player_sprite.change_y = TOP_JUMP_SPEED
        if self.player_sprite.left <= 0 or self.player_sprite.right >= SCREEN_WIDTH:
            self.wall_hit()

        wall_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.wall_list)
        if wall_hit_list:
            self.wall_hit()
        else:
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.coin_list)
            for coin in coin_hit_list:
                self.points += 1
                coin.remove_from_sprite_lists()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = ui.StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
