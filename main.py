import kivy
import datetime
import time
import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.base import runTouchApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial


kivy.config.Config.set('graphics','resizable', False)

ianuadb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ianua"
)
#####################
#    SQL SELECT     #
#####################

auge = ianuadb.cursor()
auge.execute("SELECT * FROM sprechstd")
sprechstden = auge.fetchall()

#####################
#     Methods       #
#####################


def geretnamin(geretnum): #wasch
    if geretnum == 1:
        return "Trockner"
    else:
        return "WaschM."

def getwaschzeit(zeitin):
    waschzeitdict = {
        "1": "7[sup]:00[/sup]-8[sup]:15[/sup]",
        "2": "8[sup]:15[/sup]-9[sup]:30[/sup]",
        "3": "9[sup]:30[/sup]-10[sup]:45[/sup]",
        "4": "10[sup]:45[/sup]-12[sup]:00[/sup]",
        "5": "12[sup]:00[/sup]-13[sup]:15[/sup]",
        "6": "13[sup]:15[/sup]-14[sup]:30[/sup]",
        "7": "14[sup]:30[/sup]-15[sup]:45[/sup]",
        "8": "15[sup]:45[/sup]-17[sup]:00[/sup]",
        "9": "17[sup]:00[/sup]-18[sup]:15[/sup]",
        "10": "18[sup]:15[/sup]-19[sup]:30[/sup]",
        "11": "19[sup]:30[/sup]-20[sup]:45[/sup]",
        "12": "20[sup]:45[/sup]-22[sup]:00[/sup]",
        "13": "22[sup]:00[/sup]-23[sup]:15[/sup]"
    }
    waschzeitdict = waschzeitdict.get(zeitin, zeitin)
    return waschzeitdict
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




# #################################
# biblio2_list = '''<BiblioBox@BoxLayout>:
#     text: "0 Result"'''


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
        pop = Popup(title='Leere Input', content=Label(text='Sie haben\nnix geschrieben.'), size_hint=(.7, .5))
        pop.open()

    def on_leave(self, *args):
        self.suchbuchfeld.text = ""

class Biblio2Shot(Screen):
    bibliobox = ObjectProperty(None)
    pagin = ObjectProperty(None)
    locsuchbuchfeld = ObjectProperty(None)
    suchbuch = ""

    def fetchsql(self, suchn, boxn):
        if len(suchn) != 0:
            #Buecher im Regal
            papier = ianuadb.cursor()
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
                if len(x[1])  >= 15:
                    buech = x[1][0:16]+".."
                else:
                    buech = x[1]
                buchtbtncont = '''WeissButton:
        size_hint: 1, .1
        pos_hint: {"center_x": .5}
        text:"[color=2D4059]''' + buech + '''[/color]"
        #on_press: root.buchmesse()
    '''

                buchbtn = Builder.load_string(buchtbtncont)
                buchbtn.bind(on_press = partial( self.buchmesse, x[0]))
                boxn.add_widget(buchbtn)
                buchi += buchtbtncont
            if regal == []:
                pup = Popup(title='Oh pech',
                        content=Label(text='Das haben wir\nleider nicht.'),
                        size_hint=(.7, .5))
                pup.open()
    def on_enter(self, *args):
        self.fetchsql(self.suchbuch.lower(), self.bibliobox)

    def on_leave(self, *args):
        self.locsuchbuchfeld.text = ""

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
        zeil = ianuadb.cursor()
        squl = ("SELECT * FROM bibliothek WHERE id = %s")
        succh = (self.blatt,)
        zeil.execute(squl, succh)
        zeilen = zeil.fetchall()
        zlln=zeilen[0]
        if zlln[5] == True:
            verfugstand = "gebucht"
        else:
            verfugstand = "Ja"
        self.buchname.text = zlln[1]
        self.buchBox.clear_widgets()
        karte = """BoxLayout:
    orientation: 'vertical'
    padding: 20, 0
    spacing: 5
    TexFntB:
        text: 'ISBN: """+str(zlln[2])+"""'
    TexFntB:
        text: 'Verlag: """+zlln[3].upper()+"""'
    TexFntB:
        text: 'Autor: """+zlln[4].capitalize()+"""'
    TexFntB:
        text: 'Stand: """+ verfugstand +"""'
    TexFntB:
        text: 'Bei: Zim. """+str(zlln[6])+"""'"""
        karde = Builder.load_string(karte)
        self.buchBox.add_widget(karde)


class WaschShot(Screen):
    def washbtn3(self):
        Wasch2Shot.geraete = 3
        sm.current = "wasch2"
    def washbtn2(self):
        Wasch2Shot.geraete = 2
        sm.current = "wasch2"
    def washbtn1(self):
        Wasch2Shot.geraete = 1
        sm.current = "wasch2"


class Wasch2Shot(Screen):
    rowwasch1 = ObjectProperty(None)
    rowwasch2 = ObjectProperty(None)
    rowwasch3 = ObjectProperty(None)
    waschdat0 = ObjectProperty(None)
    waschdat1 = ObjectProperty(None)
    waschdat2 = ObjectProperty(None)
    geretname = ObjectProperty(None)
    geraete = ""

    def checkin_frei(self, zeits, rowzeit):
        spueler = ianuadb.cursor()
        sequl = ("SELECT * FROM waschkueche WHERE datum = %s AND gerete = %s AND zeit = %s ")
        self.waschdatum = datetime.date.today() + datetime.timedelta(days=rowzeit)
        self.waschdatumform = str(self.waschdatum.day)+"."+str(self.waschdatum.month)+"."
        koordin = (self.waschdatum, self.geraete, zeits)
        spueler.execute(sequl, koordin)
        wasser = spueler.fetchall()
        if wasser == []:
            zinum = "Frei"
        else:
            zinum = str(wasser[-1][5])
        return zinum

    def wascherow(self, wascheroww, rowwasch):
        for wass in range(1, 14):
            schichtstand = self.checkin_frei(wass, wascheroww)
            if schichtstand == "Frei":
                schichtcolor = "Blau"
            else:
                schichtcolor = "Dark"
            schicht = schichtcolor+'''Kapsel:
                    pos_hint: {"center_x": .5}
                    text:"'''+schichtstand+'''"
                '''
            wasch_eintrag = (wass, self.waschdatumform, self.geraete, self.waschdatum)
            sschicht= Builder.load_string(schicht)
            if schichtstand == "Frei": sschicht.bind(on_press=partial(self.wasch_eintragen, wasch_eintrag))
            rowwasch.add_widget(sschicht)
        if wascheroww==0: self.waschdat0.text = self.waschdatumform
        if wascheroww==1: self.waschdat1.text = self.waschdatumform
        if wascheroww==2: self.waschdat2.text = self.waschdatumform

    def on_enter(self, *args):
        self.geretname.text = geretnamin(self.geraete)+" "+str(self.geraete)
        self.wascherow(0, self.rowwasch1)
        self.wascherow(1, self.rowwasch2)
        self.wascherow(2, self.rowwasch3)

    def on_leave(self, *args):
        self.geretname.text = ""
        self.rowwasch1.clear_widgets()
        self.rowwasch2.clear_widgets()
        self.rowwasch3.clear_widgets()

    def wasch_eintragen(self, *wasch_eintragarg):
        Wasch3Shot.wasch_eintragt = wasch_eintragarg
        sm.current = "wasch3"

class Wasch3Shot(Screen):
    waschbeschreibung = ObjectProperty(None)
    wasch_eintragt = ""
    waschzinum = ObjectProperty(None)
    waschbewohner = ObjectProperty(None)

    def on_enter(self, *args):
        self.waschbeschreibung.text = geretnamin(self.wasch_eintragt[0][2])+" "+ str(self.wasch_eintragt[0][2])+"\n"+str(self.wasch_eintragt[0][1])+"\nZeit: "+getwaschzeit(str(self.wasch_eintragt[0][0]))

    def waschsubmit(self):
        if self.waschbewohner.text != "" or self.waschzinum.text != "":
            if self.waschzinum.text.isdigit():
                waschkleidung = ianuadb.cursor()
                sqlk = "INSERT INTO waschkueche (datum, gerete, zeit, bewohner, zimm) VALUES (%s, %s, %s, %s, %s)"
                kleidung = (self.wasch_eintragt[0][3], self.wasch_eintragt[0][2], self.wasch_eintragt[0][0], self.waschbewohner.text, self.waschzinum.text)
                waschkleidung.execute(sqlk, kleidung)
                ianuadb.commit()
                if ianuadb.is_connected():
                    self.waschbewohner.text = ""
                    self.waschzinum.text = ""
                    waschkleidung.close()
                    pip = Popup(title='Danke',
                                content=Label(text='Gebucht!'),
                                size_hint=(.7, .5))
                    pip.open()
                    sm.current = "wasch"
            else:
                pap = Popup(title='Entschuldigung',
                            content=Label(text='Zi. Num. \nfalsh gegeben!'),
                            size_hint=(.7, .5))
                pap.open()
        else:
            pop = Popup(title='Entschuldigung',
                        content=Label(text='Alle Felder\nausfuellen Bitte.'),
                        size_hint=(.7, .5))
            pop.open()


class FundShot(Screen):
    scrollfund = ObjectProperty(None)
    fundswitch = ObjectProperty(None)
    camer0 = ObjectProperty(None)
    def on_enter(self, *args):
        hand = ianuadb.cursor()
        hand.execute("SELECT * FROM fund")
        fundbox = hand.fetchall()
        for gefund in fundbox:

            anzeigdaten = '''BoxLayout:
	orientation: 'vertical'
	padding: 20, 10
	halign: 'left'
	valign: 'bottom'
	TexFnt:
		text_size: self.size
		text : "in: '''+gefund[2]+'''"
	TexFnt:
		text_size: self.size
		text : "am: "
	TexFnt:
		text_size: self.size
		text: "bei: '''+gefund[4]+'''"
	TexFnt:
		text_size: self.size
		text: "#'''+str(gefund[0])+'''"
'''

            anzeigdatenpy = Builder.load_string(anzeigdaten)

            anzeigdel = '''BoxLayout:
    size_hint: .4,1
    padding: 10'''
            anzeigdelpy = Builder.load_string(anzeigdel)

            anzeigbtn = '''DarkButton:
    text: 'Found'
    size_hint: 1, .6
    pos_hint: {'center_y': .5}'''
            anzeigbtnpy = Builder.load_string(anzeigbtn)
            anzeigbtnpy.bind(on_press=partial(self.foundmd, gefund[0]))
            anzeigdelpy.add_widget(anzeigbtnpy)



            anzeigroot ='''AbtLabel:
    padding: 0
    orientation: 'vertical'
    size_hint: 1, 1
    BoxLayout:
        canvas:
            RoundedRectangle:
                source: "pic/fund/'''+gefund[5]+'''"
                size: self.size
                pos: self.pos
                radius: [10, 10, 0, 0]
    BoxLayout:
        orientation: 'vertical'
        padding: 5
        TexFnt:
            text: "'''+gefund[1]+'''"
            font_size: .08*self.parent.width'''

            anzeigop = '''BoxLayout:
    orientation: "horizontal"'''
            anzeigoppy = Builder.load_string(anzeigop)

            anzeig = Builder.load_string(anzeigroot)
            anzeigoppy.add_widget(anzeigdatenpy)
            anzeigoppy.add_widget(anzeigdelpy)
            anzeig.add_widget(anzeigoppy)

            self.scrollfund.add_widget(anzeig)

        self.scrollfund.width = self.parent.width*len(fundbox)*.9


    def foundmd(self, *args):
        fing = ianuadb.cursor()
        sqldel = "DELETE FROM fund WHERE id = %s"
        idtup= (args[0],)
        fing.execute(sqldel, idtup)
        ianuadb.commit()

        deletedfund = Popup(title='Prima',
                        content=Label(text='Fundsache\nwürde gelöscht.'),
                        size_hint=(.7, .4))
        deletedfund.open()
        self.on_leave()
        self.on_enter()


    def on_leave(self, *args):
        self.scrollfund.clear_widgets()

    def switch(self, *args):
        sm.current = "fundcam"



class FundCamShot(Screen):
    fundcamarea = ObjectProperty(None)
    camera0 = ObjectProperty(None)
    def on_enter(self, *args):
        self.camera0.play = True

    def capture(self):
        camera0py = self.ids['fundcamarea']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera0py.export_to_png("pic/fund/IMG_{}.png".format(timestr))
        # outname = "pic/fund/IMG_{}.png".format(timestr)
        # Window.screenshot(name=outname)
        FundNeuShot.fundpicname = "IMG_{}.png".format(timestr)
        sm.current = "fundneu"

class FundNeuShot(Screen):
    fundpicname = ""
    capturedfund = ObjectProperty(None)
    fundwasstil = ObjectProperty(None)
    fundwostil = ObjectProperty(None)
    fundbeistil = ObjectProperty(None)
    def on_enter(self, *args):
        fundpic_source = "pic/fund/{}".format(self.fundpicname)
        fundpic_embed='''AbtLabel:
    orientation: 'vertical'
    size_hint: 1, 1
    BoxLayout:
        canvas:
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10, 10, 0, 0]
                source: "'''+fundpic_source+'''"'''

        fundpic_embedpy=Builder.load_string(fundpic_embed)
        self.capturedfund.add_widget(fundpic_embedpy)

    def fundadd(self):
        sac = ianuadb.cursor()
        sqlsac = "INSERT INTO fund (was, wo, bei, img) VALUES (%s, %s, %s, %s)"
        jib = (self.fundwasstil.text, self.fundwostil.text, self.fundbeistil.text, self.fundpicname)
        sac.execute(sqlsac, jib)
        ianuadb.commit()
        if ianuadb.is_connected():
            self.fundbeistil.text = ""
            self.fundwostil.text = ""
            self.fundwasstil.text = ""
            sac.close()
            pip = Popup(title='Danke',
                        content=Label(text='gemeldet!'),
                        size_hint=(.7, .5))
            pip.open()
            sm.current = "fund"

    def on_leave(self, *args):
        self.capturedfund.clear_widgets()



######################################################################################################################



class BlnkShot(Screen):
    pass


class Blnk2Shot(Screen):
    pass
#############################################################################################################################


class ShotManager(ScreenManager):
    pass


#####################
#       BUILDER     #
#####################

kv = Builder.load_file("stilButton.kv")
kv = Builder.load_file("stilLabel.kv")
kv = Builder.load_file("stilSprech.kv")
kv = Builder.load_file("stilBuch.kv")
kv = Builder.load_file("stilWasch.kv")
kv = Builder.load_file("stilBlank.kv")
kv = Builder.load_file("stilBlank2.kv")
kv = Builder.load_file("stilFund.kv")
kv = Builder.load_file("stilMain.kv")
Window.clearcolor = (1, 1, 1, 1)




sm = ShotManager(transition=NoTransition())
screens = [IntroShot(name="intro"),
           MenuShot(name="menu"),
           Biblio1Shot(name="biblio1"),
           Biblio2Shot(name="biblio2"),
           BlnkShot(name="blnk"),
           Blnk2Shot(name="blnk2"),
           BuchShot(name="buch"),
           SprechShot(name="sprech"),
           WaschShot(name="wasch"),
           Wasch2Shot(name="wasch2"),
           Wasch3Shot(name="wasch3"),
           FundShot(name="fund"),
           FundCamShot(name="fundcam"),
           FundNeuShot(name="fundneu")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "fundcam"

class IanuaApp(App):
    def build(self):
        Window.size = (432, 768)
        return sm


if __name__ == "__main__":
    IanuaApp().run()
