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
from kivy.base import runTouchApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ianua"
)
#####################
#    SQL SELECT     #
#####################

auge = mydb.cursor()
auge.execute("SELECT * FROM sprechstd")
sprechstden = auge.fetchall()



#####################
#   ScreensmANAGE   #
#####################


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




#################################
biblio2_list = '''<BiblioBox@BoxLayout>:
    text: "0 Result"'''


class Biblio1Shot(Screen):
    suchbuchfeld = ObjectProperty(None)

    def buchbtn(self):
        if (self.suchbuchfeld.text != ''):
            Biblio2Shot.suchbuch = self.suchbuchfeld.text
            self.reset()
            sm.current = "biblio2"
        else:
            self.errorsuch()

    def reset(self):
        self.suchbuchfeld.text = ""

    def errorsuch(self):
        pop = Popup(title='Leere Input', content=Label(text='Sie haben nix geschrieben.'), size_hint=(None, None), size=(400, 400))
        pop.open()


class Biblio2Shot(Screen):
    bibliobox = ObjectProperty(None)
    pagin = ObjectProperty(None)
    locsuchbuchfeld = ObjectProperty(None)
    suchbuch = ""

    def fetchsql(self, suchn, boxn):

        #Buecher im Regal
        papier = mydb.cursor()
        sqla="SELECT * FROM bibliothek WHERE XyX LIKE %s"
        prozess = ('buch', 'autor', 'ISBN', 'verlag')
        suche = ('%'+suchn+'%',)
        regal = []
        for prz in prozess:
            sqla = sqla.replace("XyX", prz)
            sql = (sqla)
            papier.execute(sql, suche)
            sqla = sqla.replace(prz, "XyX")
            reg = papier.fetchall()
            regal += reg


        # Buecher soertieren
        boxn.clear_widgets()
        buchi= ''
        for x in regal:
            buchtbtncont = '''WeissButton:
    text:"[color=2D4059]''' + x[1] + '''[/color]"
    #on_press: root.buchmesse()
'''

            buchbtn = Builder.load_string(buchtbtncont)
            buchbtn.bind(on_press = partial( self.buchmesse, x[0]))
            boxn.add_widget(buchbtn)
            buchi += buchtbtncont
        print(buchi)

    def on_enter(self, *args):
        self.fetchsql(self.suchbuch.lower(), self.bibliobox)

    def locbuchbtn(self):
        self.fetchsql(self.locsuchbuchfeld.text.lower(), self.bibliobox)

    def buchmesse(self, *args):
        buchid = args[0]
        BuchShot.blatt = buchid
        sm.current = "buch"


class BuchShot(Screen):
    buchBox = ObjectProperty(None)
    buchname = ObjectProperty(None)
    blatt = ""
    def on_enter(self, *args):
        #self.show.text = "haaaa"+ self.fullin
        zeil = mydb.cursor()
        squl = ("SELECT * FROM bibliothek WHERE id = %s")
        succh = (self.blatt,)
        zeil.execute(squl, succh)
        zeilen = zeil.fetchall()
        zlln=zeilen[0]
        if zlln[5] == True:
            verfugstand = "Ausgeliehen"
        else:
            verfugstand = "Verfuegbar"
        self.buchname.text = zlln[1]
        self.buchBox.clear_widgets()
        karte = """BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 20
    TexFntB:
        text: 'ISBN: """+str(zlln[2])+"""'
    TexFntB:
        text: 'Verlag: """+zlln[3].upper()+"""'
    TexFntB:
        text: 'Autor: """+zlln[4].capitalize()+"""'
    TexFntB:
        text: 'Verfuegber: """+ verfugstand +"""'
    TexFntB:
        text: 'Bei: Zimmer"""+str(zlln[6])+"""'"""
        print(karte)
        karde = Builder.load_string(karte)
        self.buchBox.add_widget(karde)

###########################################################################################################################

class BlnkShot(Screen):
    submit = ObjectProperty(None)
    def send(self):
        self.submit.text
        Blnk2Shot.current = self.submit.text
        self.reset()
        sm.current = "blnk2"

    def reset(self):
        self.submit.text = ""


class Blnk2Shot(Screen):
    show = ObjectProperty(None)
    def on_enter(self, *args):
        self.show.text = "haaaa"
#############################################################################################################################


class ShotManager(ScreenManager):
    pass


#####################
#       BUILDER     #
#####################

kv = Builder.load_file("stilButton.kv")
kv = Builder.load_file("stilLabel.kv")
kv = Builder.load_file("stilSprech.kv")
kv = Builder.load_file("stilBiblio1.kv")
kv = Builder.load_file("stilBiblio2.kv")
kv = Builder.load_file("stilBuch.kv")
kv = Builder.load_file("stilBlank.kv")
kv = Builder.load_file("stilBlank2.kv")
kv = Builder.load_file("stilMain.kv")
Window.clearcolor = (1, 1, 1, 1)




sm = ShotManager()
screens = [IntroShot(name="intro"),
           MenuShot(name="menu"),
           Biblio1Shot(name="biblio1"),
           Biblio2Shot(name="biblio2"),
           BlnkShot(name="blnk"),
           Blnk2Shot(name="blnk2"),
           BuchShot(name="buch")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "intro"

class IanuaApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    IanuaApp().run()
