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

Window.clearcolor = get_color_from_hex("0066BA")

#root
class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def changeScreen(self, next_screen):

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
            self.ids.kivy_screen_manager.current = "start_screen"


    def confirm(self, *args):
        #wrapper.insert("Medicines", userID=self.user, medID=args[0], transTime=)
        self.ids.kivy_screen_manager.current = "barcode_screen"
        #if wrapper.select().length > 0:


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

    def conpop1(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Biogesic", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        yes_btn = Button(text="Yes", on_press=lambda *args: self.confirm('1', *args), on_release =self.popup.dismiss)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop2(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Buscopan", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)

        yes_btn = Button(text="Yes", on_press=self.confirm, on_release=self.popup.dismiss)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop3(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Decolgen No-Drowse", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        yes_btn = Button(text="Yes", on_press=self.confirm, on_release=self.popup.dismiss)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop4(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Dolfenal", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        yes_btn = Button(text="Yes", on_press=self.confirm, on_release=self.popup.dismiss)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop5(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Solmux", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        yes_btn = Button(text="Yes", on_press=self.confirm, on_release=self.popup.dismiss)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def sound1(self):
        fname = 'Biogesic' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound2(self):
        fname = 'Buscopan' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound3(self):
        fname = 'Decolgen No-Drowse' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound4(self):
        fname = 'Dolfenal' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound5(self):
        fname = 'Solmux' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()


#app object
class MedicineApp(App):

    def __init__(self, **kwargs):
        super(MedicineApp, self).__init__(**kwargs)


    def build(self):
        self.title = 'Smart Medicine Dispenser'
        return MainScreen()

if __name__== '__main__':
    MedicineApp().run()

#result = wrapper.select("Users", UserId = inp)
