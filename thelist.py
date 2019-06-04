from kivy.app import App
from kivy.lang import Builder
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from database import DataBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
import random


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""
    
    def logOut(self):
        sm.current = "login"

    def on_enter(self,*args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
        self.password = password
    def motivated(self,**kwargs):
        a = ['Your limitation—it’s only your imagination.','Push yourself, because no one else is going to \n do it for you.','Sometimes later becomes never. Do it now.',' Great things never come from comfort zones.','Dream it. Wish it. Do it.','Success doesn’t just find you. \n You have to go out and get it.','The harder you work for something, the greater you’ll feel \n when you achieve it.','Dream bigger. Do bigger.',' Don’t stop when you’re tired. Stop when you’re done.','Wake up with determination. Go to bed with satisfaction.','Do something today that your future self will thank you for.','Little things make big days.','It’s going to be hard, but hard does not mean impossible.',' Don’t wait for opportunity. Create it.','Sometimes we’re tested not to show our weaknesses, \n but to discover our strengths.',' The key to success is to focus on goals, not obstacles.','Dream it. Believe it. Build it.']
        results= random.choice(a)
        pop = Popup(title="Motivation",
                  content=Label(text=results),
                  size_hint=(0.6, 0.4), size=(400, 400))
        pop.open()

class TodoList(Screen):
    todo_text_input = ObjectProperty(None)
    datum_text_input = ObjectProperty(None)
    thelist = ObjectProperty(None)

    def Add_Mission(self,):
        Mission = self.todo_text_input.text+ " " + self. datum_text_input.text
        self.thelist.adapter.data.extend([Mission])
        self.thelist._trigger_reset_populate()
    
    def Delete_Mission(self, *args):
        if self.thelist.adapter.selection:

            selection = self.thelist.adapter.selection[0].text
            self.thelist.adapter.data.remove(selection)
            self.thelist._trigger_reset_populate()


    def Replace_Mission(self,*args):
        if self.thelist.adapter.selection:

            selection = self.thelist.adapter.selection[0].text
            self.thelist.adapter.data.remove(selection)
            Mission = self.todo_text_input.text+ " " + self. datum_text_input.text
            self.thelist.adapter.data.extend([Mission])
            self.thelist._trigger_reset_populate()

class WindowManager(ScreenManager):
    pass



def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()



kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"), TodoList(name="todo")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()