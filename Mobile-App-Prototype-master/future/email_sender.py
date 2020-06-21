# -----------------------------------
# Copyright by Victor Hugo Garzo Prado.
# -----------------------------------

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql

Builder.load_string("""
#:import get_color_from_hex kivy.utils.get_color_from_hex
<LoginScreen>:
    name: "login_gui"
    FloatLayout:
        canvas.before:
            Color:
                rgba: get_color_from_hex('#D3D4D5')
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            size_hint: .5, .5
            pos_hint: {"center_x": .5, "center_y": .7}
            source: 'Logo/python.png'  
        RecycleBoxLayout:
            size_hint: .4, .2
            pos_hint: {"center_x": .5, "center_y": .55}
            orientation: 'vertical'
        Button:
            text: "Login"
            pos_hint: {"center_x": .65, "center_y": .1}
            color: get_color_from_hex('#FFFFFF')
            font_size: 20
            size_hint: .2, .075
            on_press:
                app.btn_login()
        Button:
            text: "Verify"
            pos_hint: {"center_x": .35, "center_y": .1}
            color: get_color_from_hex('#FFFFFF')
            font_size: 20
            size_hint: .2, .075
            on_press:
                app.open_test()
        Label:
            text: "Username"
            pos_hint: {"center_x": .3, "center_y": .35}
            font_size: 20
            color: get_color_from_hex('#000000')
        TextInput:
            id: user
            multiline: False
            pos_hint: {"center_x": .5, "center_y": .3}
            size_hint: .5, .05
        Label:
            text: "Password"
            pos_hint: {"center_x": .3, "center_y": .25}
            font_size: 20
            color: get_color_from_hex('#000000')
        Label:
            text: "Show password"
            pos_hint: {"center_x": .48, "center_y": .25}
            font_size: 15
            color: get_color_from_hex('#000000')
        CheckBox:
            color: get_color_from_hex('#000000')
            id: chk
            size_hint: .05, .05
            pos_hint: {"center_x": .4, "center_y": .25}
        TextInput:
            id: password
            multiline: False
            password: False if root.ids.chk.active else True
            pos_hint: {"center_x": .5, "center_y": .2}
            size_hint: .5, .05
<SenderScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: get_color_from_hex('#D3D4D5')
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            text: "Send"
            pos_hint: {"center_x": .405, "center_y": .1}
            color: get_color_from_hex('#FFFFFF')
            font_size: 20
            size_hint: .2, .075
            on_press:
                app.btn_send()
        Label:
            text: "To"
            pos_hint: {"center_x": .03, "center_y": 0.95}
            font_size: 20
            color: get_color_from_hex('#000000')
        TextInput:
            id: to_user
            multiline: False
            pos_hint: {"center_x": .27, "center_y": .90}
            size_hint: .5, .05
        Label:
            text: "Subject"
            pos_hint: {"center_x": .06, "center_y": .85}
            font_size: 20
            color: get_color_from_hex('#000000')
        TextInput:
            id: subject
            multiline: False
            pos_hint: {"center_x": .27, "center_y": .80}
            size_hint: .5, .05
        Label:
            text: "Message"
            pos_hint: {"center_x": .41, "center_y": .72}
            font_size: 40
            color: get_color_from_hex('#000000')
        TextInput:
            id: message
            multiline: True
            pos_hint: {"center_x": .42, "center_y": .42}
            size_hint: .8, .5
        Spinner:
            id: email
            text: 'Email List'
            pos_hint: {"center_x": .76, "center_y": .9}
            size_hint: .3, .09
            on_text: app.on_spinner_select(self.text)
<LoginErrorPopup>
    auto_dismiss: False
    title: 'Incorrect username or password!'
    size_hint: .31, .2
    Button:
        size_hint: .5, .6
        pos_hint: {"center_x": .5, "center_y": .5}
        text: 'Close'
        on_release: root.dismiss()
        
<EmailSentPopup>
    auto_dismiss: False
    title: 'Email Sent!'
    size_hint: .2, .2
    Button:
        size_hint: .5, .6
        pos_hint: {"center_x": .5, "center_y": .5}
        text: 'Close'
        on_release: root.dismiss()
""")


class LoginScreen(Screen):
    pass


class SenderScreen(Screen):
    pass


class CustomDropDown(Screen):
    pass


class LoginErrorPopup(Popup):
    pass


class EmailSentPopup(Popup):
    pass


screen_manager = ScreenManager()

screen_manager.add_widget(LoginScreen(name="screen_login"))
screen_manager.add_widget(SenderScreen(name="screen_sender"))
screen_manager.add_widget(CustomDropDown(name="screen_drop_down"))

outlook_server = smtplib.SMTP('smtp.office365.com', 587)
outlook_server.ehlo()
outlook_server.starttls()
outlook_server.ehlo()

# ---------------------------------------------------------------------------
# Database

dbcon = pymysql.connect(host="localhost", user="root", password="icedb", db="emai_list", charset="utf8mb4")

# ---------------------------------------------------------------------------
# Set emails to the email list

cursor = dbcon.cursor()
cursor2 = dbcon.cursor()

email_value = screen_manager.get_screen("screen_sender").ids.email
cursor.execute("select email_name from emails_info")
rows = cursor.fetchall()
email_name = [str(t[0]) for t in rows]
email_value.values = email_name

cursor.execute("select email from emails_info")
email_rows = cursor.fetchall()


# ---------------------------------------------------------------------------
# Class to build and show the screen, and set some functions to the buttons.

class KivSenderApp(App):

    def build(self):
        return screen_manager

    def btn_login(self):
        username = self.root.get_screen("screen_login").ids.user.text
        password = self.root.get_screen("screen_login").ids.password.text
        try:
            outlook_server.login(username, password)
            screen_manager.current = "screen_sender"
        except smtplib.SMTPAuthenticationError:
            LoginErrorPopup().open()

    def on_spinner_select(self, text):
        x = email_name.index(text)
        email = [str(t1[0]) for t1 in email_rows]
        self.root.get_screen("screen_sender").ids.to_user.text = email[x]

    def btn_send(self):
        user_from = self.root.get_screen("screen_login").ids.user.text
        email_user = self.root.get_screen("screen_sender").ids.to_user.text
        subject_user = self.root.get_screen("screen_sender").ids.subject.text
        message_user = self.root.get_screen("screen_sender").ids.message.text

        msg = MIMEMultipart()
        msg["From"] = user_from
        msg["To"] = email_user
        msg["Subject"] = subject_user

        message_user = MIMEText(message_user, 'html')
        msg.attach(message_user)

        outlook_server.sendmail(user_from, email_user, msg.as_string())
        EmailSentPopup().open()


sender_app = KivSenderApp()
sender_app.run()