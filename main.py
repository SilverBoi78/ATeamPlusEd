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
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, account_type TEXT)")

# Commit the changes and close the connection when the app exits.
atexit.register(lambda: (conn.commit(), conn.close()))


def insert_user(username, password, account_type):
    cursor.execute("INSERT INTO users (username, password, account_type) VALUES (?, ?, ?)", (username, password, account_type))


def user_exists(username, password, account_type):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND account_type = ?", (username, password, account_type))
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
        exit_button = Button(text="Exit",
                             size_hint=(1, None),
                             height=40,
                             bold=True,
                             background_color="#FFB6C1"
                             )

        # Adding buttons to window
        self.window.add_widget(parent_button)
        self.window.add_widget(child_button)
        self.window.add_widget(exit_button)

        # Binding buttons
        parent_button.bind(on_press=self.parent_button_click)
        child_button.bind(on_press=self.child_button_click)
        exit_button.bind(on_press=exit)

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
        self.return_button = Button(text="Return to Menu",
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
        self.window.add_widget(self.return_button)

        # Binding button
        self.login.bind(on_press=self.login_button_click)
        self.create_account.bind(on_press=self.create_account_button_click)
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def return_button_click(self, instance):
        self.manager.current = "login"

    def login_button_click(self, instance):
        username = self.user.text
        password = self.password.text
        account_type = 'parent'


        if user_exists(username, password, account_type):
            self.manager.current = "parent"
        else:
            # Display an error message to the user if the login fails.
            self.manager.current = "invalid_login"

    def create_account_button_click(self, instance):
        self.manager.current = "account_creation_parent"


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
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#FFB6C1"
                                     )
        self.return_button = Button(text="Return to Menu",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#FFB6C1"
                                    )
        self.error_label = Label(text="", color="#FF0000")

        # Same as parent login screen
        self.window.add_widget(self.usertitle)
        self.window.add_widget(self.user)
        self.window.add_widget(self.passtitle)
        self.window.add_widget(self.password)
        self.window.add_widget(self.login)
        self.window.add_widget(self.create_account)
        self.window.add_widget(self.return_button)

        # Same as parent login screen
        self.login.bind(on_press=self.login_button_click)
        self.create_account.bind(on_press=self.create_account_button_click)
        self.return_button.bind(on_press=self.return_button_click)

        self.add_widget(self.window)

    def login_button_click(self, instance):
        # Same as parent login screen
        username = self.user.text
        password = self.password.text
        account_type = 'child'

        if user_exists(username, password, account_type):
            self.manager.current = "child"
        else:
            # Display an error message to the user if the login fails.
            self.manager.current = "invalid_login"

    def create_account_button_click(self, instance):
        self.manager.current = "account_creation_child"

    def return_button_click(self, instance):
        self.manager.current = "login"


class AccountCreationScreenParent(Screen):
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
        self.return_button = Button(text="Return to Login",
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
        self.window.add_widget(self.create_account)
        self.window.add_widget(self.return_button)

        # Binding button
        self.create_account.bind(on_press=self.create_account_button_click_parent)
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def create_account_button_click_parent(self, instance):
        username = self.user.text
        password = self.password.text
        account_type = "parent"

        if username and password:
            insert_user(username, password, account_type)
            self.manager.current = "login"

        else:
            # Display an error message to the user if the login fails.
            self.manager.current = "invalid_acc_creation"

    def return_button_click(self, instance):
        self.manager.current = "login"

class AccountCreationScreenChild(Screen):
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
        self.return_button = Button(text="Return to Login",
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
        self.window.add_widget(self.create_account)
        self.window.add_widget(self.return_button)

        # Binding button
        self.create_account.bind(on_press=self.create_account_button_click_child)
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def create_account_button_click_child(self, instance):
        username = self.user.text
        password = self.password.text
        account_type = "child"

        if username and password:
            insert_user(username, password, account_type)
            self.manager.current = "login"

        else:
            # Display an error message to the user if the login fails.
            self.manager.current = "invalid_acc_creation"

    def return_button_click(self, instance):
        self.manager.current = "login"


class ParentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.parent_title = Label(text="Welcome, Parent",
                                  font_size=24,
                                  color="#FFB6C1"
                                  )

        self.parent_info = Label(text="Dashboard.",
                                 font_size=16,
                                 color="#FFB6C1"
                                 )

        self.assigned_tasks_button = Button(text="Assigned Tasks",
                                            size_hint=(1, None),
                                            height=40,
                                            bold=True,
                                            background_color="#FFB6C1"
                                            )

        self.logout_button = Button(text="Logout",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#FFB6C1"
                                    )

        self.window.add_widget(self.parent_title)
        self.window.add_widget(self.parent_info)
        self.window.add_widget(self.assigned_tasks_button)
        self.window.add_widget(self.logout_button)

        self.assigned_tasks_button.bind(on_press=self.assigned_tasks_button_click)
        self.logout_button.bind(on_press=self.logout_button_click)
        self.add_widget(self.window)

    def assigned_tasks_button_click(self, instance):
        self.manager.current = "assigned_tasks"

    def logout_button_click(self, instance):
        self.manager.current = "login"


class ChildScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.child_title = Label(text="Welcome, Child",
                                 font_size=24,
                                 color="#FFB6C1"
                                 )

        self.child_info = Label(text="Dashboard.",
                                font_size=16,
                                color="#FFB6C1"
                                )

        self.tasks_button = Button(text="List of Tasks",
                                   size_hint=(1, None),
                                   height=40,
                                   bold=True,
                                   background_color="#FFB6C1"
                                   )

        self.logout_button = Button(text="Logout",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#FFB6C1"
                                    )

        self.window.add_widget(self.child_title)
        self.window.add_widget(self.child_info)
        self.window.add_widget(self.tasks_button)
        self.window.add_widget(self.logout_button)

        self.tasks_button.bind(on_press=self.tasks_button_click)
        self.logout_button.bind(on_press=self.logout_button_click)
        self.add_widget(self.window)

    def tasks_button_click(self, instance):
        self.manager.current = "child_tasks"

    def logout_button_click(self, instance):
        self.manager.current = "login"


class AssignedTasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        # Add widgets for viewing assigned tasks here
        self.tasks_label = Label(text="Assigned Tasks",
                                 font_size=24,
                                 color="#FFB6C1"
                                 )

        self.tasks_info = Label(text="List of assigned tasks goes here.",
                                font_size=16,
                                color="#FFB6C1"
                                )

        self.back_button = Button(text="Back to Parent Dashboard",
                                  size_hint=(1, None),
                                  height=40,
                                  bold=True,
                                  background_color="#FFB6C1"
                                  )

        # Adding widgets to the GridLayout
        self.window.add_widget(self.tasks_label)
        self.window.add_widget(self.tasks_info)
        self.window.add_widget(self.back_button)

        # Binding the back button to return to the parent screen
        self.back_button.bind(on_press=self.back_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def back_button_click(self, instance):
        # Navigate back to the parent screen
        self.manager.current = "parent"


class Child_Tasks(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.child_title = Label(text="Test",
                                 font_size=24,
                                 color="#FFB6C1"
                                 )

        self.back_button = Button(text="Back to Parent Dashboard",
                                  size_hint=(1, None),
                                  height=40,
                                  bold=True,
                                  background_color="#FFB6C1"
                                  )

        self.window.add_widget(self.child_title)
        self.window.add_widget(self.back_button)

        self.back_button.bind(on_press=self.back_button_click)
        self.add_widget(self.window)

    def back_button_click(self, instance):
        self.manager.current = "child"


class InvalidLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.testtile = Label(text="Invalid Credentials",
                              font_size=20,
                              color="#FFB6C1"
                              )
        self.return_button = Button(text="Try Again",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#FFB6C1"
                                    )

        self.window.add_widget(self.testtile)
        self.window.add_widget(self.return_button)

        # Binding button
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def return_button_click(self, instance):
        self.manager.current = "login"


class InvalidAccCreation(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30

        self.testtile = Label(text="Unable to create account, ensure both fields are filled in.",
                              font_size=20,
                              color="#FFB6C1"
                              )
        self.return_button = Button(text="Return",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#FFB6C1"
                                    )

        self.window.add_widget(self.testtile)
        self.window.add_widget(self.return_button)

        # Binding button
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def return_button_click(self, instance):
        self.manager.current = "login"


class MyApp(App):
    def build(self):
        sm = ScreenManager()

        login_screen = LoginScreen(name="login")
        parent_login_screen = ParentLoginScreen(name="parent_login")
        child_login_screen = ChildLoginScreen(name="child_login")
        account_creation_screen_parent = AccountCreationScreenParent(name="account_creation_parent")
        account_creation_screen_child = AccountCreationScreenChild(name="account_creation_child")
        parent_screen = ParentScreen(name="parent")
        child_screen = ChildScreen(name="child")
        invalid_login_screen = InvalidLoginScreen(name="invalid_login")
        invalid_acc_creation = InvalidAccCreation(name="invalid_acc_creation")
        assigned_tasks_screen = AssignedTasksScreen(name="assigned_tasks")
        child_tasks = Child_Tasks(name="child_tasks")

        sm.add_widget(login_screen)
        sm.add_widget(parent_login_screen)
        sm.add_widget(child_login_screen)
        sm.add_widget(account_creation_screen_parent)
        sm.add_widget(account_creation_screen_child)
        sm.add_widget(parent_screen)
        sm.add_widget(child_screen)
        sm.add_widget(invalid_login_screen)
        sm.add_widget(invalid_acc_creation)
        sm.add_widget(assigned_tasks_screen)
        sm.add_widget(child_tasks)

        return sm


if __name__ == '__main__':
    MyApp().run()
