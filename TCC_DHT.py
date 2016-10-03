"""<title>Menus, Toolboxes, a full Application</title>
Most all widgets are used in this example.  A full custom widget
is included.  A number of connections are used to make the application
function.
"""
import pygame
import time
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

#from Python_DHT_TesteComVariaveisCnsts import *         #Import the function with gives the temperature and humidity CAN BE DELETED IN THE FINAL VERSION
##from Adafruit_Python_DHT import *                       #Import the function with reads the temperature and humidity
import Adafruit_DHT
from pgu import gui                                     #Import all gui
from SaveFilesHumidityTemp import SaveFilesHumidityTemp #Import the function with saves the files in .xls
from ChangeMonthtoPortuguese import *                   #Import the function with changes the month in a Portuguese readable format   
#from DHT11 import *

# --- Global constants ---
BLACK = (0, 0, 0)    #Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 700  
SCREEN_HEIGHT = 500
flagStart = 0
tableHumidityTemp = gui.Table()    #Creating table that will show the humidity and temperature
select = gui.Select(value=Adafruit_DHT.DHT11) #Creating the selection between the types of sensor, beeing DHT11 the default
humiditylist = []   #Making the list humidity
templist = []       #temp
Date = []           #Date
Time = []           #and Time globals
# --- Classes ---
class NewDialog(gui.Dialog): #Creating the dialog when you click File->New
    def __init__(self,**params):
        title = gui.Label("Novo Arquivo...")
        
        t = gui.Table()
        
        self.value = gui.Form()
        
        t.tr()
        t.td(gui.Label("Abrir: "))
        t.td(gui.Input(name="fname"),colspan=3)
        
        t.tr()
        e = gui.Button("Ok")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e,colspan=2)
        
        e = gui.Button("Cancelar")
        e.connect(gui.CLICK,self.close,None)
        t.td(e,colspan=2)
        
        gui.Dialog.__init__(self,title,t)
        
        gui.Dialog.__init__(self,title,t)

class AboutDialog(gui.Dialog): #Creating the dialog when you click Help->About
    def __init__(self,**params):
        title = gui.Label("Sobre o modulo DHT")
        
        width = 400
        height = 200
        doc = gui.Document(width=width)
        
        space = title.style.font.size(" ")
        
        doc.block(align=0)
        for word in """Modulo DHT v1.0""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        doc.add(gui.Image("logoufscar.png"),align=1)
        for word in """Este trabalho foi feito como trabalho de conclusao de curso por William Takeshi Pereira.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        gui.Dialog.__init__(self,title,gui.ScrollArea(doc,width,height))
##
        

class HelpDialog(gui.Dialog): #Creating the dialog when you click Help->Help
    def __init__(self,**params):
        title = gui.Label("Ajuda")
        
        doc = gui.Document(width=400)
        
        space = title.style.font.size(" ")
        
        doc.block(align=-1)
        doc.add(gui.Image("logoufscar.png"),align=1)
        for word in """O modulo DHT foi desenvolvido para acelerar e estimular o aprendizado de ciencia.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)    
        for word in """Com modulo DHT voce pode analisar e salvar dados de temperatura e umidade lidos pelo sensores DHT11/22.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)

        gui.Dialog.__init__(self,title,doc)
        
class QuitDialog(gui.Dialog): #Creating the dialog when you click File->Quit
    def __init__(self,**params):
        title = gui.Label("Sair")
        
        t = gui.Table()
        
        t.tr()
        t.add(gui.Label("Tem certeza que deseja fechar o programa?"),colspan=2)
        
        t.tr()
        e = gui.Button("Ok")
        e.connect(gui.CLICK,self.send,gui.QUIT)
        t.td(e)
        
        e = gui.Button("Cancelar")
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)

class OpenDialog(gui.Dialog):  #Creating the dialog when you click File->Open
    def __init__(self,**params):
        title = gui.Label("Abrir")
        
        t = gui.Table()
        
        self.value = gui.Form()
        
        t.tr()
        t.td(gui.Label("Abrir: "))
        t.td(gui.Input(name="fname"),colspan=3)
        
        t.tr()
        e = gui.Button("Ok")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e,colspan=2)
        
        e = gui.Button("Cancelar")
        e.connect(gui.CLICK,self.close,None)
        t.td(e,colspan=2)
        
        gui.Dialog.__init__(self,title,t)

class SaveDialog(gui.Dialog): #Creating the dialog when you click File->SaveAs
    def __init__(self,**params):
        title = gui.Label("Salvar como...")
        
        t = gui.Table()
        
        self.value = gui.Form()
        print(self.value)
        t.tr()
        t.td(gui.Label("Salvar: "))
        t.td(gui.Input(name="fname"),colspan=3)
        
        t.tr()
        e = gui.Button("Ok")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e,colspan=2)
        
        e = gui.Button("Cancelar")
        e.connect(gui.CLICK,self.close,None)
        t.td(e,colspan=2)
        
        gui.Dialog.__init__(self,title,t)
        
class StartGameButton(gui.Button): #The button that starts reading the values in the sensor
    def __init__(self,**params):
        params['value'] = 'Comecar leitura'
        gui.Button.__init__(self,**params)
        self.connect(gui.CLICK,WriteTableHomeScreen)

class ClearButton(gui.Button): #The button just to test, delete before final product
    def __init__(self,**params):
        params['value'] = 'Limpar'
        gui.Button.__init__(self,**params)
        self.connect(gui.CLICK,tableHumidityTemp.clear) 

class HomeScreen(gui.Desktop):  #Create the container of the HomeScreen and add all the buttons and tables
    def __init__(self,**params):
        gui.Desktop.__init__(self,**params)
        
        self.connect(gui.QUIT,self.quit,None)
        
        c = gui.Container(width=SCREEN_WIDTH,height=SCREEN_HEIGHT) #Create the screen with the WIDTH and HEIGHT specified before


        box = gui.ScrollArea(tableHumidityTemp,680,240)            #Create the box where all the data will be shown up
        c.add(box,10,120)

        e = StartGameButton() 

        c.add(e,20,40) ##Add the StartGameBtton

########################################################################################        
        e = ClearButton()

        c.add(e,300,40) ##Add the ClearButton
##############################################################################################
        
        select.add("DHT11",Adafruit_DHT.DHT11)                               #Sensors that can be choosen IF YOU NEED MORE YOU WILL NEED TO ADD IN THE Adafruit FUNCTION
        select.add("DHT22",Adafruit_DHT.DHT22)
        c.add(select,190,40)                                      #Create the select box that will be used to choose the sensor

        
        self.fname = 'untitled.xls'                               #Name of the .xls file
        
        self.new_d = NewDialog()                                  #Opening the file->new, open, save and qui dialong in the HomeScreen
        self.new_d.connect(gui.CHANGE,self.action_new,None)
        self.open_d = OpenDialog()
        self.open_d.connect(gui.CHANGE,self.action_open,None)
        self.save_d = SaveDialog()
        self.save_d.connect(gui.CHANGE,self.action_saveas,None)
        self.quit_d = QuitDialog()
        self.quit_d.connect(QUIT,self.quit,None)
        
        self.help_d = HelpDialog()                                #Opening the help and about dialong
        self.about_d = AboutDialog()
        
        ##Initializing the Menus, we connect to a number of Dialog.open methods for each of the dialogs.
        ##::
        menus = gui.Menus([
            ('Arquivo/Novo',self.new_d.open,None),
            ('Arquivo/Abrir',self.open_d.open,None),
            ('Arquivo/Salvar',self.action_save,None),
            ('Arquivo/Salvar como',self.save_d.open,None),
            ('Arquivo/Sair',self.quit_d.open,None),
            ('Ajuda/Ajuda',self.help_d.open,None),
            ('Ajuda/Sobre',self.about_d.open,None),
            ])
        ##
        c.add(menus,0,0)
        menus.rect.w,menus.rect.h = menus.resize()
        #print 'menus',menus.rect
        
        self.widget = c
        
    def action_new(self,value):
        self.new_d.close()
        self.fname = self.new_d.value['fname'].value
        global tableHumidityTemp
        global humiditylist
        global templist
        tableHumidityTemp.clear()
        humiditylist = []
        templist = []
    def action_save(self,value):
        SaveFilesHumidityTemp(self.fname, "DHT", humiditylist, templist, Date, Time)
        
    def action_saveas(self,value):
        self.save_d.close()
        self.fname = self.save_d.value['fname'].value
        SaveFilesHumidityTemp(self.fname, "DHT", humiditylist, templist, Date, Time)
    def action_open(self,value):
        self.open_d.close()
        self.fname = self.open_d.value['fname']
        self.painter.surface = pygame.image.load(self.fname)
        self.painter.repaint()
        
def WriteTableHomeScreen(): #Function that Reads the sensor and prints in the table
    global flagStart
    global c
    if flagStart:
        flagStart = 0
        
    else:
        flagStart = 1
    print(flagStart)
    while flagStart:
##        humidity, temp = ReadHumidityTemp(select.value,2) #(sensor,pin) ex: (11,9)
        humidity, temp = Adafruit_DHT.read_retry(select.value,2)
        print('humidity{0:0.1f} temp{0:0.1f}'.format(humidity, temp))
        humiditylist.append(humidity)
        templist.append(temp)
        DateTime = time.localtime()
        Datestring = str(DateTime[2])+"/"+str(DateTime[1])+"/"+str(DateTime[0]) #Putting the date in a string to make easier to put n the excel table
        Date.append(Datestring)
        Timestring = str(DateTime[3])+":"+str(DateTime[4])+":"+str(DateTime[5]) #Putting the time in a string to make easier to put n the excel table
        Time.append(Timestring)
        DateTime = ChangeMonthtoPortuguese(DateTime)
        tableHumidityTemp.tr()
        tableHumidityTemp.td(gui.Label(str((DateTime[9],
                                            "Umidade: ",humidity,"Temperatura: ",temp))))
        print("Umidade: ",humidity,"Temperatura: ",temp)
    
        pygame.time.wait(10000)
        app.loop()
if __name__ == "__main__":
    app = HomeScreen()
    app.run()
    
