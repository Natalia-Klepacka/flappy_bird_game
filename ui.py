import arcade
import arcade.gui
from arcade.gui import UIManager, UIFlatButton, UIToggle
from game import *
import csv
import os
import sys


class ExitButton(arcade.gui.UIFlatButton):
    def on_click(self):
        sys.exit()


class MenuButton(arcade.gui.UIFlatButton):
    def __init__(self, center_x, center_y, option: str, window, mode):
        super().__init__(option,
                         center_x=center_x,
                         center_y=center_y,
                         width=250)
        self.mode=mode
        self.window = window
        self.view = None
        if option == 'Play':
            self.view = GameView(self.mode)
        elif option == 'Rules':
            self.view = RulesView(self.mode)
        elif option == 'Settings':
            self.view = SettingsView()
        elif option == 'Highscores':
            self.view = HighscoresView(self.mode)
        elif option == 'About the author':
            self.view = AuthorView(self.mode)

    def on_click(self):
        self.window.show_view(self.view)


class StartView(arcade.View):
    def __init__(self, mode='easy'):
        super().__init__()
        self.ui_manager = UIManager()
        self.mode = mode

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("My Game", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.AMBER)
        self.ui_manager.purge_ui_elements()
        exit_button = ExitButton("X",
                                 center_x=SCREEN_WIDTH-10,
                                 center_y=SCREEN_HEIGHT-10,
                                 width=20,
                                 height=20,
                                 id="aaa")
        exit_button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(135, 21, 25),
            bg_color_hover=(135, 21, 25),
            bg_color_press=(122, 21, 24),
            border_color=(135, 21, 25),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.ui_manager.add_ui_element(exit_button)
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.5),
                                                  "Play",
                                                  self.window,
                                                  self.mode))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.4),
                                                  "Rules",
                                                  self.window,
                                                  self.mode))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.3),
                                                  "Settings",
                                                  self.window,
                                                  self.mode))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.2),
                                                  "Highscores",
                                                  self.window,
                                                  self.mode))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.1),
                                                  "About the author",
                                                  self.window,
                                                  self.mode))


class RulesView(arcade.View):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.BLUEBERRY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("1. You can jump using SPACE\n\n"
                         "2. Don't touch green walls\n\n"
                         "3. Collect coins\n\n"
                         "4. Survive as long, as you can\n\n",
                         SCREEN_WIDTH/2 - 250,
                         SCREEN_HEIGHT/2,
                         color=arcade.color.WHITE,
                         font_size=20,
                         width=500,
                         align='center')
        arcade.draw_text("Press esc to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/4,
                         color=arcade.color.LIGHT_GRAY,
                         font_size=10,
                         width=200,
                         align='center')

    def on_show_view(self):
        self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            view = StartView(self.mode)
            view.setup()
            self.window.show_view(view)


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.toggle = None
        self.mode = 'easy'

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.WILD_ORCHID)
        self.ui_manager.purge_ui_elements()
        self.toggle = UIToggle(center_x=SCREEN_WIDTH/2,
                               center_y=SCREEN_HEIGHT/3,
                               width=100,
                               height=40)
        self.ui_manager.add_ui_element(self.toggle)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Choose difficulty level:",
                         SCREEN_WIDTH/2 - 400,
                         SCREEN_HEIGHT/2,
                         color=arcade.color.WHITE,
                         font_size=12,
                         width=800,
                         align='center')
        arcade.draw_text("Hard",
                         SCREEN_WIDTH / 2 - 100,
                         SCREEN_HEIGHT / 3 - 20,
                         color=arcade.color.WHITE,
                         font_size=18,
                         width=100,
                         align='right')
        arcade.draw_text("Easy",
                         SCREEN_WIDTH / 2 + 50,
                         SCREEN_HEIGHT / 3 - 20,
                         color=arcade.color.WHITE,
                         font_size=18,
                         width=800,
                         align='left')
        arcade.draw_text("Press esc to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/6,
                         color=arcade.color.LIGHT_GRAY,
                         font_size=10,
                         width=200,
                         align='center')

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.toggle.value:
                self.mode = 'easy'
            else:
                self.mode = 'hard'
            view = StartView(mode=self.mode)
            view.setup()
            self.window.show_view(view)


class HighscoresView(arcade.View):
    def __init__(self, mode):
        super().__init__()
        self.scores_easy = []
        self.scores_hard = []
        self.mode = mode

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.BLUEBERRY)

    def on_draw(self):
        arcade.start_render()
        if not os.path.isfile("leaderboards.csv"):
            arcade.draw_text("You didn't play yet\n Please play to see your scores here",
                             SCREEN_WIDTH/2 - 450,
                             SCREEN_HEIGHT/2,
                             color=arcade.color.WARM_BLACK,
                             font_size=40,
                             width=900,
                             align='center')
        else:
            with open("leaderboards.csv", "r") as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    if row and not row[0] == 'easy':
                        self.scores_easy.append(row[0])
                        self.scores_hard.append(row[1])
            arcade.draw_text("Easy",
                             SCREEN_WIDTH/4 - 100,
                             SCREEN_HEIGHT * 3/4,
                             color=arcade.color.WARM_BLACK,
                             font_size=30,
                             width=200,
                             align='center')
            arcade.draw_text(f"  1. {self.scores_easy[0]}\n"
                             f"  2. {self.scores_easy[1]}\n"
                             f"  3. {self.scores_easy[2]}\n"
                             f"  4. {self.scores_easy[3]}\n"
                             f"  5. {self.scores_easy[4]}\n"
                             f"  6. {self.scores_easy[5]}\n"
                             f"  7. {self.scores_easy[6]}\n"
                             f"  8. {self.scores_easy[7]}\n"
                             f"  9. {self.scores_easy[8]}\n"
                             f"10. {self.scores_easy[9]}\n",
                             SCREEN_WIDTH/6,
                             SCREEN_HEIGHT/6,
                             color=arcade.color.WARM_BLACK,
                             font_size=20,
                             width=400,
                             align='left')
            arcade.draw_text("Hard",
                             SCREEN_WIDTH * 3/4 - 100,
                             SCREEN_HEIGHT * 3/4,
                             color=arcade.color.WARM_BLACK,
                             font_size=30,
                             width=200,
                             align='center')
            arcade.draw_text(f"  1. {self.scores_hard[0]}\n"
                             f"  2. {self.scores_hard[1]}\n"
                             f"  3. {self.scores_hard[2]}\n"
                             f"  4. {self.scores_hard[3]}\n"
                             f"  5. {self.scores_hard[4]}\n"
                             f"  6. {self.scores_hard[5]}\n"
                             f"  7. {self.scores_hard[6]}\n"
                             f"  8. {self.scores_hard[7]}\n"
                             f"  9. {self.scores_hard[8]}\n"
                             f"10. {self.scores_hard[9]}\n",
                             SCREEN_WIDTH * 2/3,
                             SCREEN_HEIGHT/6,
                             color=arcade.color.WARM_BLACK,
                             font_size=20,
                             width=400,
                             align='left')
            arcade.draw_text("Press esc to come back",
                             SCREEN_WIDTH/2 - 100,
                             SCREEN_HEIGHT/7,
                             color=arcade.color.WARM_BLACK,
                             font_size=10,
                             width=200,
                             align='center')

    def on_mouse_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            view = StartView(self.mode)
            view.setup()
            self.window.show_view(view)

    def on_show_view(self):
        self.setup()


class AuthorView(arcade.View):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.BLUEBERRY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Hi! I'm  Natalia Klepacka.\n"
                         "I'm very happy that you decided to try on my game. I hope you'll have a lot of fun.\n",
                         SCREEN_WIDTH/2 - 400,
                         SCREEN_HEIGHT/2,
                         color=arcade.color.WHITE,
                         font_size=20,
                         width=800,
                         align='center')
        arcade.draw_text("Press esc to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/6,
                         color=arcade.color.LIGHT_GRAY,
                         font_size=10,
                         width=200,
                         align='center')

    def on_show_view(self):
        self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            view = StartView(self.mode)
            view.setup()
            self.window.show_view(view)


class GameOverView(arcade.View):
    def __init__(self, score, mode):
        super().__init__()
        self.score = score
        self.mode = mode

    def setup(self):
        self.save_score()
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("GAME OVER :(",
                         SCREEN_WIDTH/2 - 450,
                         SCREEN_HEIGHT/2,
                         color=arcade.color.WHITE,
                         font_size=40,
                         width=900,
                         align='center')
        arcade.draw_text(f"Score: {self.score}",
                         SCREEN_WIDTH / 2 - 450,
                         SCREEN_HEIGHT / 4,
                         color=arcade.color.WHITE,
                         font_size=25,
                         width=900,
                         align='center')
        arcade.draw_text("Click anywhere to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/6,
                         color=arcade.color.LIGHT_GRAY,
                         font_size=10,
                         width=200,
                         align='center')

    def on_show_view(self):
        self.setup()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        view = StartView()
        view.setup()
        self.window.show_view(view)

    def save_score(self):
        if not os.path.isfile("leaderboards.csv"):
            with open("leaderboards.csv", "w") as f:
                pass
        scores_easy = []
        scores_hard = []
        with open("leaderboards.csv", "r") as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                if row and not row[0] == 'easy':
                    scores_easy.append(int(row[0]))
                    scores_hard.append(int(row[1]))
        if len(scores_easy) < 10:
            for i in range(0, 10 - len(scores_easy)):
                scores_easy.append(0)
        if len(scores_hard) < 10:
            for i in range(0, 10 - len(scores_hard)):
                scores_hard.append(0)
        if self.mode == 'easy':
            scores_easy.append(self.score)
            scores_easy.sort(reverse=True)
            del scores_easy[-1]
        elif self.mode == 'hard':
            scores_hard.append(self.score)
            scores_hard.sort(reverse=True)
            del scores_hard[-1]
        with open("leaderboards.csv", "w") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(("easy", "hard"))
            for i in range(0, 10):
                csvwriter.writerow((scores_easy[i], scores_hard[i]))

