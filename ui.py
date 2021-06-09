import arcade
import arcade.gui
from arcade.gui import UIManager
from game import *


class HardModeButton(arcade.gui.UIFlatButton):
    pass


class MenuButton(arcade.gui.UIFlatButton):
    def __init__(self, center_x, center_y, option: str, window):
        super().__init__(option,
                         center_x=center_x,
                         center_y=center_y,
                         width=250)
        self.window = window
        self.view = None
        if option == 'Play':
            self.view = GameView()
        elif option == 'Rules':
            self.view = RulesView()
        elif option == 'Settings':
            self.view = SettingsView()
        elif option == 'Highscores':
            self.view = HighscoresView()
        elif option == 'About the author':
            self.view = AuthorView()

    def on_click(self):
        self.window.show_view(self.view)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

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
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.5),
                                                  "Play",
                                                  self.window))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.4),
                                                  "Rules",
                                                  self.window))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.3),
                                                  "Settings",
                                                  self.window))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.2),
                                                  "Highscores",
                                                  self.window))
        self.ui_manager.add_ui_element(MenuButton(int(SCREEN_WIDTH / 2),
                                                  int(SCREEN_HEIGHT * 0.1),
                                                  "About the author",
                                                  self.window))


class RulesView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.BLUEBERRY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Here you'll be able to see the rules",
                         SCREEN_WIDTH/2 - 250,
                         SCREEN_HEIGHT/2,
                         color=arcade.color.WHITE,
                         font_size=20,
                         width=500,
                         align='center')
        arcade.draw_text("Click anywhere to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/4,
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


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.WILD_ORCHID)
        self.ui_manager.purge_ui_elements()
        # tu trzeba pododawać przyciski!!!

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("The chosen mode:",
                         SCREEN_WIDTH/2 - 400,
                         SCREEN_HEIGHT/2,
                         color=arcade.color.WHITE,
                         font_size=12,
                         width=800,
                         align='center')
        arcade.draw_text("Click anywhere to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/6,
                         color=arcade.color.LIGHT_GRAY,
                         font_size=10,
                         width=200,
                         align='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        view = StartView()
        view.setup()
        self.window.show_view(view)


class HighscoresView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.BLUEBERRY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Easy",
                         SCREEN_WIDTH/4 - 100,
                         SCREEN_HEIGHT * 3/4,
                         color=arcade.color.WARM_BLACK,
                         font_size=30,
                         width=200,
                         align='center')
        arcade.draw_text(" 1. \n 2. \n 3. \n 4. \n 5. \n 6. \n 7. \n 8. \n 9. \n10. \n",
                         SCREEN_WIDTH/6,
                         SCREEN_HEIGHT/6,
                         color=arcade.color.WARM_BLACK,
                         font_size=20,
                         width=40,
                         align='left')
        arcade.draw_text("Hard",
                         SCREEN_WIDTH * 3/4 - 100,
                         SCREEN_HEIGHT * 3/4,
                         color=arcade.color.WARM_BLACK,
                         font_size=30,
                         width=200,
                         align='center')
        arcade.draw_text("1. \n2. \n3. \n4. \n5. \n6. \n7. \n8. \n9. \n10. \n",
                         SCREEN_WIDTH * 2/3,
                         SCREEN_HEIGHT/6,
                         color=arcade.color.WARM_BLACK,
                         font_size=20,
                         width=40,
                         align='left')
        arcade.draw_text("Click anywhere to come back",
                         SCREEN_WIDTH/2 - 100,
                         SCREEN_HEIGHT/7,
                         color=arcade.color.WARM_BLACK,
                         font_size=10,
                         width=200,
                         align='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        view = StartView()
        view.setup()
        self.window.show_view(view)

    def on_show_view(self):
        self.setup()


class AuthorView(arcade.View):
    def __init__(self):
        super().__init__()

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


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
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
