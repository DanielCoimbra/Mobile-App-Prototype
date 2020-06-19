from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import db_utils as db

class MyGrid(Widget):
    name = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def btn(self):
        db.insert_login(self.name.text, self.password.text)
        

class PrototypeApp(App):
    def build(self):

        return MyGrid()

if __name__ == "__main__":
    PrototypeApp().run()