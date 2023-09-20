import atexit
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import sqlite3

# Add this line after your imports to create a database connection.
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create a table for storing user data if it doesn't exist yet.
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

# Commit the changes and close the connection when the app exits.
atexit.register(lambda: (conn.commit(), conn.close()))


def insert_user(username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))


def user_exists(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        # Image
        self.window.add_widget(Image(source="poop.png"))

        # Buttons
        parent_button = Button(text="Parent",
                               size_hint=(1, None),
                               height=40,
                               bold=True,
                               background_color="#FFB6C1"
                               )
        child_button = Button(text="Child",
                              size_hint=(1, None),
                              height=40,
                              bold=True,
                              background_color="#FFB6C1"
                              )

        # Adding buttons to window
        self.window.add_widget(parent_button)
        self.window.add_widget(child_button)

        # Binding buttons
        parent_button.bind(on_press=self.parent_button_click)
        child_button.bind(on_press=self.child_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def parent_button_click(self, instance):
        self.manager.current = "parent_login"

    def child_button_click(self, instance):
        self.manager.current = "child_login"


class ParentLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#FFB6C1"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1, 1)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#FFB6C1"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1, 1)
                                  )
        self.login = Button(text="Login",
                            size_hint=(1, None),
                            height=40,
                            bold=True,
                            background_color="#FFB6C1"
                            )
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#FFB6C1"
                                     )
        self.error_label = Label(text="", color="#FF0000")

        # Adding widgets to window
        self.window.add_widget(self.usertitle)
        self.window.add_widget(self.user)
        self.window.add_widget(self.passtitle)
        self.window.add_widget(self.password)
        self.window.add_widget(self.login)
        self.window.add_widget(self.create_account)

        # Binding button
        self.login.bind(on_press=self.login_button_click)
        self.create_account.bind(on_press=self.create_account_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def login_button_click(self, instance):
        username = self.user.text
        password = self.password.text

        if user_exists(username, password):
            self.manager.current = "login"
        else:
            # Display an error message to the user if the login fails.
            self.ids.error_label.text = "Invalid username or password"

    def create_account_button_click(self, instance):
        self.manager.current = "account_creation"


class ChildLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#FFB6C1"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1, 1)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#FFB6C1"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1, 1)
                                  )
        self.login = Button(text="Login",
                            size_hint=(1, None),
                            height=40,
                            bold=True,
                            background_color="#FFB6C1"
                            )

        # Same as parent login screen
        self.window.add_widget(self.usertitle)
        self.window.add_widget(self.user)
        self.window.add_widget(self.passtitle)
        self.window.add_widget(self.password)
        self.window.add_widget(self.login)

        # Same as parent login screen
        self.login.bind(on_press=self.login_button_click)

        # Same shit
        self.add_widget(self.window)

    def login_button_click(self, instance):
        self.manager.current = "login"

    def create_account_button_click(self, instance):
        self.manager.current = "account_creation"


class AccountCreationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#FFB6C1"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1, 1)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#FFB6C1"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1, 1)
                                  )
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#FFB6C1"
                                     )

        # Adding widgets to window
        self.window.add_widget(self.usertitle)
        self.window.add_widget(self.user)
        self.window.add_widget(self.passtitle)
        self.window.add_widget(self.password)
        self.window.add_widget(self.create_account)

        # Binding button
        self.create_account.bind(on_press=self.create_account_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def create_account_button_click(self, instance):
        username = self.user.text
        password = self.password.text

        if username and password:
            insert_user(username, password)
            self.manager.current = "login"


class MyApp(App):
    def build(self):
        sm = ScreenManager()

        login_screen = LoginScreen(name="login")
        parent_login_screen = ParentLoginScreen(name="parent_login")
        child_login_screen = ChildLoginScreen(name="child_login")
        account_creation_screen = AccountCreationScreen(name="account_creation")

        sm.add_widget(login_screen)
        sm.add_widget(parent_login_screen)
        sm.add_widget(child_login_screen)
        sm.add_widget(account_creation_screen)

        return sm


if __name__ == '__main__':
    MyApp().run()
