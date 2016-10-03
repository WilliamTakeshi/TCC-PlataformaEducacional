"""Trabalho de conclusão de curso de graduação apresentado ao Departamento de Engenharia Elétrica da Universidade Federal de São Carlos
como requisito parcial para a obtenção do título de Bacharel em Engenharia Elétrica.
Modulo MPU6050/Coleta de dados
"""
import pygame
import time
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

#from Python_DHT_TesteComVariaveisCnsts import *         #Import the function with gives the temperature and humidity CAN BE DELETED IN THE FINAL VERSION
from Adafruit_Python_DHT import *                       #Import the function with reads the temperature and humidity
from pgu import gui                                     #Import all gui
from SaveFilesAccelGyro import SaveFilesAccelGyro  #Import the function with saves the files in .xls
from ChangeMonthtoPortuguese import *                   #Import the function with changes the month in a Portuguese readable format   
from MPU6050 import get_accel_gyro
#from DHT11 import *

# --- Global constants ---
BLACK = (0, 0, 0)    #Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 700  
SCREEN_HEIGHT = 500
flagStart = 0
table_accel_gyro = gui.Table()    #Creating table that will show the humidity and temperature
select = gui.Select(value="DHT11") #Creating the selection between the types of sensor, beeing DHT11 the default
#Making the lists
accel_xout_scaled = []
accel_yout_scaled = []
accel_zout_scaled = []
gyro_xout = []
gyro_yout = []
gyro_zout = []
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
        title = gui.Label("Sobre o modulo MPU6050")
        
        width = 400
        height = 200
        doc = gui.Document(width=width)
        
        space = title.style.font.size(" ")
        
        doc.block(align=0)
        for word in """Modulo MPU6050 v1.0""".split(" "): 
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
        for word in """O modulo MPU6050 foi desenvolvido para acelerar e estimular o aprendizado de ciencia.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)    
        for word in """Com modulo MPU6050 voce pode analisar e salvar dados de aceleracao e mudancas em sua orientacao lidos pelo sensor MPU6050.""".split(" "): 
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

class HomeScreen(gui.Desktop):  #Create the container of the HomeScreen and add all the buttons and tables
    def __init__(self,**params):
        gui.Desktop.__init__(self,**params)
        
        self.connect(gui.QUIT,self.quit,None)
        
        c = gui.Container(width=SCREEN_WIDTH,height=SCREEN_HEIGHT) #Create the screen with the WIDTH and HEIGHT specified before


        box = gui.ScrollArea(table_accel_gyro,680,240)            #Create the box where all the data will be shown up
        c.add(box,10,120)

        e = StartGameButton() 

        c.add(e,20,40) ##Add the StartGameBtton
        
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
        global table_accel_gyro
        global accel_xout_scaled
        global accel_yout_scaled 
        global accel_zout_scaled
        global gyro_xout
        global gyro_yout
        global gyro_zout
        table_accel_gyro.clear()
        accel_xout_scaled = []
        accel_yout_scaled = []
        accel_zout_scaled = []
        gyro_xout = []
        gyro_yout = []
        gyro_zout = []
    def action_save(self,value):
        SaveFilesAccelGyro(self.fname, select.value, accel_xout_scaled,accel_yout_scaled,accel_zout_scaled,gyro_xout,gyro_yout,gyro_zout)
    def action_saveas(self,value):
        self.save_d.close()
        self.fname = self.save_d.value['fname'].value
        SaveFilesAccelGyro(self.fname, select.value, accel_xout_scaled,accel_yout_scaled,accel_zout_scaled,gyro_xout,gyro_yout,gyro_zout)
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
    while flagStart:
        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = get_accel_gyro()
        #--Writing the accels and gyros in the list to later send to excel--
        accel_xout_scaled.append(accel_x)
        accel_yout_scaled.append(accel_y)
        accel_zout_scaled.append(accel_z)
        gyro_xout.append(gyro_x)
        gyro_yout.append(gyro_y)
        gyro_zout.append(gyro_z)
        #--Writing in the table for the GUI--
        table_accel_gyro.tr()
        table_accel_gyro.td(gui.Label(str(("Aceleracao em x,y,z(g): {:.2f}, {:.2f}, {:.2f}".format(accel_x,accel_y,accel_z)))),align=-1)
        table_accel_gyro.tr()
        table_accel_gyro.td(gui.Label(str("Gyro em x,y,z: {}, {}, {}".format(gyro_x, gyro_y, gyro_z))),align=-1)
        print(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
        pygame.time.wait(1000)
        app.loop()
if __name__ == "__main__":
    app = HomeScreen()
    app.run()
