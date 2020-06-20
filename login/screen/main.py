from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import db_utils as db_u


class RegisterWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    


    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "" :
                # db.add_user(self.email.text, self.password.text, self.namee.text)
                db_u.add_user(self.email.text, self.password.text, self.namee.text)

                sm.current = "login"
            else:
                erro_form('senha')
        else:
            erro_form('email')

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
        if db_u.check_credentials(self.email.text, self.password.text):
            UserWindow.user_email = self.email.text
            self.reset()
            sm.current = "main"
        else:
            erro_login()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def on_enter(self):
        self.reset()



class UserWindow(Screen):
    accountName = ObjectProperty(None)
    created = ObjectProperty(None) 
    user_email = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        self.accountName.text = "Olá " + db_u.get_name(self.user_email) + "!!"
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def erro_login():
    pop = Popup(title='Erro',
                  content=Label(text='Senha ou Email incorretos.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def erro_form(string):
    if string == 'email':
        pop = Popup(title='Email não cadastrado.',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    elif string == 'senha':
        pop = Popup(title='Senha incorreta.',
                    content=Label(text='Please fill in all inputs with valid information.'),
                    size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
