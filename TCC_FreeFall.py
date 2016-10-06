"""Trabalho de conclusão de curso de graduação apresentado ao Departamento de Engenharia Elétrica da Universidade Federal de São Carlos
como requisito parcial para a obtenção do título de Bacharel em Engenharia Elétrica.
Modulo MPU6050/Freefall
"""

import time
import random
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from ColorDialog import ColorDialog
from MPU6050 import get_accel
# The maximum frame-rate
FPS = 30
WIDTH,HEIGHT = 640,480

BLACK = (0, 0, 0)    #Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
font = pygame.font.Font(None, 25)
##You can initialize the screen yourself.
##::
screen = pygame.display.set_mode((640,480),SWSURFACE)
##

class StarControl(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)

        fg = BLACK #Color of the free fall table

        self.tr()
        self.td(gui.Label("Free Fall",color=fg),colspan=4)


        self.tr()
        self.td(gui.Label("Height: ",color=fg),align=1)
        def cb():
            print(height.value)
        height = gui.Input(value='1',size=2)
        height.connect("activate", cb)
        self.td(height)
        self.td(gui.Label("m",color=fg))
        
        
##        self.tr()
##        self.td(gui.Label("Color: ",color=fg),align=1)
##        
##        
##        default = RED
##        color = gui.Color(default,width=64,height=10,name='color')
##        color_d = ColorDialog(default)
##
##        color.connect(gui.CLICK,color_d.open,None)
##        self.td(color)
##        def update_col():
##            color.value = color_d.value
##        color_d.connect(gui.CHANGE,update_col)
##        
##        btn = gui.Switch(value=False,name='fullscreen')
##        btn.connect(gui.CHANGE, fullscreen_changed, btn)
##
##        self.tr()
##        self.td(gui.Label("Full Screen: ",color=fg),align=1)
##        self.td(btn)


        def Clear():
            global timefreefall
            global flagStart
            timefreefall= 0
            flagStart = 1
            
        btn = gui.Button("Clear")
        btn.connect(gui.CLICK, Clear)
        
        self.tr()
        self.td(gui.Label("Clear"))
        self.td(btn,colspan=3)

def Timer(Accel):
    global timefreefall
    dt = clock.tick(FPS)/1000.0
    
    if Accel > 0.9:
        pass
    else:
        timefreefall = timefreefall + dt
    
##Using App instead of Desktop removes the GUI background.  Note the call to app.init()
##::

form = gui.Form()

app = gui.App()
starCtrl = StarControl()

c = gui.Container(align=-1,valign=-1)
c.add(starCtrl,0,0)
app.init(c)
##
timefreefall = 0
flagStart = 0
##You can include your own run loop.
##::
#reset()
clock = pygame.time.Clock()
done = False
while not done:
    for e in pygame.event.get():
        if e.type is QUIT: 
            done = True
        elif e.type is KEYDOWN and e.key == K_ESCAPE: 
            done = True
        else:
            app.event(e)



    output_string = "Time: {0:.2f}".format(timefreefall)
    screen.fill(WHITE)
    text = font.render(output_string, True, BLACK)
    screen.blit(text, [200, 0])
    
    app.paint(screen)
    pygame.display.flip()
    while flagStart:
        output_string = "Time: {0:.2f}".format(timefreefall)
        text = font.render(output_string, True, BLACK)
        totalaccel = get_accel()
        Timer(totalaccel)
        screen.fill(WHITE,((200,0,100,20)))
        screen.blit(text, [200, 0])
        pygame.display.flip()
##        clock.tick(FPS)
##        print(clock.get_fps())    
        print(totalaccel)
        if totalaccel > 3:
            flagStart = 0
    clock.tick(FPS)
##    print(clock.get_fps())
##    print(timefreefall)
    

