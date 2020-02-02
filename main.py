import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button


class IntroShot(Screen):
    pass


class MenuShot(Screen):
    pass

class MenShot(Screen):
    pass


class ShotManager(ScreenManager):
    pass


kv = Builder.load_file("stilButton.kv")
kv = Builder.load_file("stilLabel.kv")
kv = Builder.load_file("stilMain.kv")
Window.clearcolor = (1, 1, 1, 1)





class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
