import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ianua"
)

auge = mydb.cursor()
auge.execute("SELECT * FROM sprechstd")
sprechstden = auge.fetchall()






class IntroShot(Screen):
    pass


class MenuShot(Screen):
    pass

class SprechShot(Screen):
    def sprechen(self):
        sprch = ''
        for x in sprechstden:
            sprch += str(x[1])+' /  '+ x[2] + ' - '+ x[3]+'\n'
        return sprch

class BlnkShot(Screen):
    pass


class ShotManager(ScreenManager):
    pass



kv = Builder.load_file("stilButton.kv")
kv = Builder.load_file("stilLabel.kv")
kv = Builder.load_file("stilSprech.kv")
kv = Builder.load_file("stilBlank.kv")
kv = Builder.load_file("stilMain.kv")
Window.clearcolor = (1, 1, 1, 1)





class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
