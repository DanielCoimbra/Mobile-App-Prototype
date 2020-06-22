from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
import db_utils as db_u
import os

picture = []

class RegisterWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)    

    def submit(self):

        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "" :
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
        pass


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class UserWindow(Screen):
    text_input = ObjectProperty(None)
    savefile = ObjectProperty(None)


    def show_reports(self):
        sm.current = 'all_reports'
        

    def dismiss_popup(self):
        self._popup.dismiss()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
        self.dismiss_popup()

    def show_selected(self):
        sm.current = 'picture'

    def logout(self):
        sm.current = 'login'


class PictureViewer(Screen):
    selected = ObjectProperty(None)
    cancel = ObjectProperty(None)
    pic = None
    
  

    def this_root(self):
        return os.path.abspath(__file__)

    def display_image(self):
        return self.pic

    def selected(self,filename):
        try:
            self.ids.image.source = filename[0]
            self.pic = filename[0]
            picture.append(filename[0])
        except:
            pass

    def continuar(self):
        sm.current = 'form'
        #root.ids.foto_escolhida.source = filename[0]
        # print(filename[0])
        # print('\n')
        # print(os.path.abspath(__file__))
    def back(self):
        sm.current = 'main'


class ButtonsLayout(BoxLayout):
    def btn(self):
        pass


class ReportWindow(Screen):
    def back(self):
        sm.current = 'main'

    def btn(self):
        sm.current = 'all_reports'
        #sm.get_screen('all_reports').
    def on_enter(self):
        box = BoxLayout()
        scrl = ScrollView()
        btnlyt = BoxLayout()

        self.add_widget(box)
        
        box.add_widget(scrl)

        scrl.add_widget(btnlyt)

        size = db_u.report_table_size()
        
        button = Button(text='Voltar')
        button.bind(on_release=self.back)
        btnlyt.add_widget(button)
        # button.bind(on_release=self.back())
        
        for x in range(size):
            print(x)
            button = Button(text='Report' + str(x+1))
            button.bind(on_release=self.btn)
            self.ids.button_layout.add_widget(button)
            
    


class AllReportsWindow(Screen):
    def on_enter(self):
        pass

class FormWindow(Screen):
    # descricao = ObjectProperty(None)

    def back(self):
        sm.current = 'picture'

    def save_file_on_db(self, txt):
        pic = sm.get_screen('picture').display_image()
        if txt != '':
            db_u.insert_report(pic, txt)
            sm.current = 'main'
        else:
            pop = Popup(
                        title='Erro',
                        content=Label(text='Insira descrição'),
                        size_hint=(None, None), size=(400, 400)
                        )
            pop.open()


def erro_login():
    pop = Popup(
                title='Erro',
                content=Label(text='Senha ou Email incorretos.'),
                size_hint=(None, None), size=(400, 400)
                )
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


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")
sm = WindowManager()
foto = None

screens = [
            LoginWindow(name="login"),
            RegisterWindow(name="create"),
            UserWindow(name="main"), 
            PictureViewer(name="picture"),
            FormWindow(name='form'),
            ReportWindow(name='all_reports'),
            AllReportsWindow(name='one_report')
            ]

for screen in screens:

    sm.add_widget(screen)

sm.current = "main"

class MyMainApp(App):

    def build(self):

        return sm


if __name__ == "__main__":

    MyMainApp().run()