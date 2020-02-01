import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

class IntroShot(Screen):
    pass


class MenuShot(Screen):
    pass


class ShotManager(ScreenManager):
    pass


kv = Builder.load_file("stilButton.kv")
kv = Builder.load_file("stilMain.kv")
Window.clearcolor = (.13,.13,.19,1)





class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
