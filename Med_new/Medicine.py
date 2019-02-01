import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.audio import SoundLoader
from functools import partial
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation

import wrapper
import sms

from datetime import datetime
from threading import Timer
import smtplib

import pigpio
import sys
import time
import random

db = wrapper.Wrapper()

Window.clearcolor = get_color_from_hex("0066BA")

#root
class ServoControl:
    def servo_rotate(self, g):
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(g[0], 1300)
        time.sleep(g[1])
        pi.set_servo_pulsewidth(g[0], 0)

        pi.stop

class MainScreen(BoxLayout):
    user = ""

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.servocontrol = ServoControl()

    def switch(self, state):
        Window.allow_vkeyboard = state
        Window.single_vkeyboard = state
        Window.docked_vkeyboard = state

    def bcode(self, barcode):
        result = db.select('user', **{'uid':barcode})
        if result.rowcount > 0:
            self.user = barcode
            usertransact = db.select('transaction', **{'userID':barcode, 'date(datetime)'
            :datetime.now().date()})
            print(usertransact.rowcount)
            if usertransact.rowcount < 2:
                self.changeScreen('confirm')
            else:
                content = BoxLayout(orientation="vertical")
                self.pop = Popup(title='Error',size=(500, 200), auto_dismiss=False, content=content)
                ok_btn = Button(text="OK", on_press=self.pop.dismiss, size_hint_y=.3, font_size='20dp')
                content.add_widget(Label(text="You have reached the daily limit of withdrawing medicine.", size_hint_y=.7,font_size='30dp'))
                content.add_widget(ok_btn)
                self.pop.open()

        else:
            content = BoxLayout(orientation="vertical")
            self.pop = Popup(title='Error',size=(500, 200), auto_dismiss=False, content=content)
            ok_btn = Button(text="OK", on_press=self.pop.dismiss, size_hint_y=.3, font_size='20dp')
            content.add_widget(Label(text="Invalid Login", size_hint_y=.7,font_size='75dp'))
            content.add_widget(ok_btn)
            self.pop.open()


    def admin(self, user, passwd):
        result = db.select('admin', **{'adminUser': user, 'adminPass': passwd})
        if result.rowcount > 0:
            self.changeScreen('enter')
        else:
            content = BoxLayout(orientation="vertical")
            self.pop = Popup(title='Error',size=(500, 200), auto_dismiss=False, content=content)
            ok_btn = Button(text="OK", on_press=self.pop.dismiss, size_hint_y=.3, font_size='20dp')
            content.add_widget(Label(text="Invalid Login", size_hint_y=.7,font_size='30dp'))
            content.add_widget(ok_btn)
            self.pop.open()

    def reset(self, medID, count):
        if int(count) > 20:
            count = "20"
        db.update('medicine', 'mid', medID, **{'count':count})
        self.changeScreen("back to main screen")


    def changeScreen(self, next_screen):

        if next_screen == "admin login":
            self.switch(True)
            self.ids.kivy_screen_manager.current = "admin_screen"

        if next_screen == "enter":
            self.switch(False)
            self.ids.kivy_screen_manager.current = "count_screen"

        if next_screen == "back":
            self.switch(False)
            self.ids.kivy_screen_manager.current = "barcode_screen"

        if next_screen == "log out":
            self.switch(True)
            self.ids.kivy_screen_manager.current = "admin_screen"

        if next_screen == "go back":
            self.ids.kivy_screen_manager.current = "count_screen"

        if next_screen == "set biogesic":
            self.ids.kivy_screen_manager.current = "bio_screen"

        if next_screen == "set buscopan":
            self.ids.kivy_screen_manager.current = "busco_screen"

        if next_screen == "set decolgen no-drowse":
            self.ids.kivy_screen_manager.current = "decol_screen"

        if next_screen == "set dolfenal":
            self.ids.kivy_screen_manager.current = "dolfe_screen"

        if next_screen == "set solmux":
            self.ids.kivy_screen_manager.current = "sol_screen"

        if next_screen == "confirm":
            #user=wrapper.select()
            #if user.length > 0:
                #self.user = user.name()
            self.ids.kivy_screen_manager.current = "start_screen"

        if next_screen == "biogesic":
            self.ids.kivy_screen_manager.current = "first_screen"

        if next_screen == "buscopan":
            self.ids.kivy_screen_manager.current = "second_screen"

        if next_screen == "decolgen no-drowse":
            self.ids.kivy_screen_manager.current = "third_screen"

        if next_screen == "dolfenal":
            self.ids.kivy_screen_manager.current = "fourth_screen"

        if next_screen == "solmux":
            self.ids.kivy_screen_manager.current = "fifth_screen"

        if next_screen == "back to main screen":
            self.ids.kivy_screen_manager.current = "barcode_screen"


    def transaction(self, medName):
        result = db.select('medicine', **{'medName': medName})
        x=0
        for i in result:
            if x==0:
                value=i
                x+=1

        medID = value['mid']
        medCount = int(value['count']) - 1

        db.update('medicine', 'mid', medName, **{'count':medCount})
        transValues = {'userID':self.user, 'medID':medID, 'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'presentCount':medCount}
        db.insert('transaction', **transValues)

        if medCount <= 5:
            text = "The medicine " + medName +" is near depletion, please refill."
            sms.send_msg(text)

        #pindelay is a dictionary which contains {'medName':(pin, delay)}
        pindelay = {'Biogesic':(4, 2), 'Buscopan':(5, 4), 'Decolgen':(6, 4), 'DecolgenND':(13, 4), 'Solmux': (26, 4)}
        self.dispense(pindelay[medName])


    def pop1(self):
        self.pop = Popup(title='Information', content=Image(source='biogesic.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop2(self):
        self.pop = Popup(title='Information', content=Image(source='buscopan.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop3(self):
        self.pop = Popup(title='Information', content=Image(source='decolgen.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop4(self):
        self.pop = Popup(title='Information', content=Image(source='dolfenal.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop5(self):
        self.pop = Popup(title='Information', content=Image(source='solmux.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()


    def dispense(self, g):
        print(g)
        self.servocontrol.servo_rotate(g)
        self.popup.dismiss()
        self.changeScreen('back to main screen')

    def conpop1(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Is Biogesic the medicine you need?", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo1 = lambda x:self.transaction('Biogesic')
        yes_btn = Button(text="Yes", on_release = servo1)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop2(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Is Buscopan the medicine you need?", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo2 = lambda x:self.transaction('Buscopan')
        yes_btn = Button(text="Yes", on_release = servo2)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop3(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Is Decolgen No-Drowse the medicine you need?", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo3 = lambda x:self.transaction('DecolgenND')
        yes_btn = Button(text="Yes", on_release = servo3)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop4(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Is Dolfenal the medicine you need?", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo4 = lambda x:self.transaction('Dolfenal')
        yes_btn = Button(text="Yes", on_release = servo4)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop5(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Is Solmux the medicine you need?", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo5 = lambda x:self.transaction('Solmux')
        yes_btn = Button(text="Yes", on_release = servo5)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def sound1(self):
        fname = 'Biogesic' + ".wav"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound2(self):
        fname = 'Buscopan' + ".wav"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound3(self):
        fname = 'Decolgen No-Drowse' + ".wav"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound4(self):
        fname = 'Dolfenal' + ".wav"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound5(self):
        fname = 'Solmux' + ".wav"
        sound = SoundLoader.load(fname)
        sound.play()



#app object
class MedicineApp(App):

    def __init__(self, **kwargs):
        super(MedicineApp, self).__init__(**kwargs)
        x=datetime.today()
        y=x.replace(day=x.day, hour=21, minute=36, second=0, microsecond=0)
        delta_t=y-x
        secs=delta_t.seconds+1
        t = Timer(secs, self.mail)
        t.start()

    def build(self):
        self.title = 'Smart Medicine Dispenser'
        return MainScreen()

    def mail(self):
        gmail_user = 'smartdispenser0@gmail.com'
        gmail_pwd = 'abcd@12345_678'
        gmail_send = 'smartdispenser0@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        message = 'Please be advised to check the status of the database. It can be accesed through local host'
        server.sendmail(gmail_user, gmail_send, message)
        server.quit()

if __name__== '__main__':
    MedicineApp().run()

#result = wrapper.select("Users", UserId = inp)
