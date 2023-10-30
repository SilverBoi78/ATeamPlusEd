import atexit
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.window import Window
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
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (task_user TEXT, task_id INTEGER, task_name TEXT, task_desc TEXT, task_points INTEGER, task_due TEXT)")
cursor.execute("""CREATE TABLE IF NOT EXISTS savings_goals (username TEXT,goal_name TEXT,goal_amount INTEGER)""")

# Commit the changes and close the connection when the app exits.
atexit.register(lambda: (conn.commit(), conn.close()))


def insert_task(task_user, task_id, task_name, task_desc, task_points, task_due):
    cursor.execute("INSERT INTO tasks (task_user, task_id, task_name, task_desc, task_points, task_due) VALUES (?, ?, ?, ?, ?, ?)",
                   (task_user, task_id, task_name, task_desc, task_points, task_due))


def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()


# Get the tasks for a specific user.
def get_user_tasks(task_user):
    cursor.execute("SELECT * FROM tasks WHERE task_user = ?", (task_user,))
    return cursor.fetchall()

def specific_task(task_id):
    cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
    return cursor.fetchone()


def get_task_name(task_id):
    cursor.execute("SELECT task_name FROM tasks WHERE task_id = ?", (task_id,))
    return cursor.fetchone()


def get_task_desc(task_id):
    cursor.execute("SELECT task_desc FROM tasks WHERE task_id = ?", (task_id,))
    return cursor.fetchone()


def get_task_points(task_id):
    cursor.execute("SELECT task_points FROM tasks WHERE task_id = ?", (task_id,))
    return cursor.fetchone()


def get_task_due(task_id):
    cursor.execute("SELECT task_due FROM tasks WHERE task_id = ?", (task_id,))
    return cursor.fetchone()


def check_user_task(task_user):
    cursor.execute("SELECT * FROM tasks WHERE task_user = ?", (task_user,))
    return cursor.fetchone()

def insert_user(username, password, account_type):
    cursor.execute("INSERT INTO users (username, password, account_type) VALUES (?, ?, ?)",
                   (username, password, account_type))


def insert_child(username, password, parent):
    cursor.execute("INSERT INTO users (username, password, parent) VALUES (?, ?, ?)",
                   (username, password, parent))


def insert_goal(username, goal_name, goal_amount):
    cursor.execute("SELECT * FROM savings_goals WHERE username = ? AND goal_name = ?", (username, goal_name))
    existing_goal = cursor.fetchone()

    if existing_goal:
        cursor.execute("UPDATE savings_goals SET goal_amount = ? WHERE username = ? AND goal_name = ?",
                       (goal_amount, username, goal_name))
    else:
        cursor.execute("INSERT INTO savings_goals (username, goal_name, goal_amount) VALUES (?, ?, ?)",
                       (username, goal_name, goal_amount))

    conn.commit()

def get_goals(username):
    cursor.execute("SELECT goal_amount FROM savings_goals WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return the goal amount
    else:
        return None  # Return None if there is no savings goal



def user_exists(username, password, account_type):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND account_type = ?",
                   (username, password, account_type))
    return cursor.fetchone() is not None
def child_exists(username, password, parent):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND parent = ?",
                   (username, password, parent))
    return cursor.fetchone() is not None


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 30
        # Create a vector that will store the tasks created by a parent.
        self.tasks = []
        # Place a blank username in the manager so that it can be accessed by all screens.


class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.clearcolor = (.90, .90, .90, 1)
        # Image
        self.window.add_widget(Image(source="poop.png"))
        welcome_button = Label(text="[b]WELCOME TO ATeamPlusEd![/b]",
                               font_size=40,
                               color="#0000ff",
                               markup=True
                               )
        # Buttons
        parent_button = Button(text="Parent",
                               size_hint=(1, None),
                               height=40,
                               bold=True,
                               background_color="#0000ff"
                               )
        child_button = Button(text="Child",
                              size_hint=(1, None),
                              height=40,
                              bold=True,
                              background_color="#0000ff"
                              )
        exit_button = Button(text="Exit",
                             size_hint=(1, None),
                             height=40,
                             bold=True,
                             background_color="#0000ff"
                             )

        # Adding buttons to window
        self.window.add_widget(welcome_button)
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


class ParentLoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1.5, 1.5)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1.5, 1.5),
                                  password = True
                                  )
        self.login = Button(text="Login",
                            size_hint=(1, None),
                            height=40,
                            bold=True,
                            background_color="#0000ff"
                            )
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#0000ff"
                                     )
        self.return_button = Button(text="Return to Menu",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
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
            self.manager.username = username
            self.manager.current = "parent"
        else:
            # Display an error message to the user if the login fails.
            self.manager.current = "invalid_login"

    def create_account_button_click(self, instance):
        self.manager.current = "account_creation_parent"


class ChildLoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1.5, 1.5)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1.5, 1.5),
                                  password = True
                                  )
        self.login = Button(text="Login",
                            size_hint=(1, None),
                            height=40,
                            bold=True,
                            background_color="#0000ff"
                            )
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#0000ff"
                                     )
        self.return_button = Button(text="Return to Menu",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
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
        username = self.user.text
        password = self.password.text
        account_type = 'child'

        if user_exists(username, password, account_type):
            # Update the username in the ChildScreen and SavingsGoalScreen
            self.manager.get_screen('child').username = username
            self.manager.get_screen('savings_goal').username = username

            # Navigate to the ChildScreen
            self.manager.current = "child"
        else:
            # Display an error message to the user if the login fails.
            self.manager.current = "invalid_login"

    def create_account_button_click(self, instance):
        self.manager.current = "account_creation_child"

    def return_button_click(self, instance):
        self.manager.current = "login"


class AccountCreationScreenParent(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1.5, 1.5)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1.5, 1.5),
                                  password = True
                                  )
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#0000ff"
                                     )
        self.return_button = Button(text="Return to Login",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
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


class AccountCreationScreenChild(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.usertitle = Label(text="Username:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.user = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1.5, 1.5)
                              )
        self.passtitle = Label(text="Password:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.password = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1.5, 1.5)
                                  )
        self.create_account = Button(text="Create Account",
                                     size_hint=(1, None),
                                     height=40,
                                     bold=True,
                                     background_color="#0000ff"
                                     )
        self.return_button = Button(text="Return to Login",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
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


class ParentScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parent_title = Label(text="Welcome, Parent",
                                  font_size=24,
                                  color="#0000ff"
                                  )

        self.parent_info = Label(text="Dashboard.",
                                 font_size=16,
                                 color="#0000ff"
                                 )

        self.assigned_tasks_button = Button(text="Assigned Tasks",
                                            size_hint=(1, None),
                                            height=40,
                                            bold=True,
                                            background_color="#0000ff"
                                            )

        self.logout_button = Button(text="Logout",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
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

class SavingsGoalScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.savings_goal_label = Label(text="Savings Goal",
                                        font_size=24,
                                        color="#0000ff"
                                        )

        self.savings_goal_input = TextInput(multiline=False,
                                           padding_y=(5, 5),
                                           size_hint=(1.0, .15)
                                           )

        self.set_goal_button = Button(text="Set Goal",
                                      size_hint=(1, None),
                                      height=40,
                                      bold=True,
                                      background_color="#0000ff"
                                      )

        self.return_button = Button(text="Return to Dashboard",
                                   size_hint=(1, None),
                                   height=40,
                                   bold=True,
                                   background_color="#0000ff"
                                   )

        self.window.add_widget(self.savings_goal_label)
        self.window.add_widget(self.savings_goal_input)
        self.window.add_widget(self.set_goal_button)
        self.window.add_widget(self.return_button)

        self.set_goal_button.bind(on_press=self.set_goal_button_click)
        self.return_button.bind(on_press=self.return_button_click)
        self.add_widget(self.window)

    def set_goal_button_click(self, instance):
        try:
            savings_goal = float(self.savings_goal_input.text)
        except ValueError:
            # Handle the error, e.g., show an error message to the user
            return

        username = self.manager.get_screen('child').username  # Get the actual username of the logged-in child
        goal_name = "savings_goals"

        insert_goal(username, goal_name, savings_goal)

        child_screen = self.manager.get_screen("child")
        child_screen.update_savings_goal_label(savings_goal)

        self.manager.current = "child"


    def return_button_click(self, instance):
        self.manager.current = "child"


class ChildScreen(BaseScreen):
    username = StringProperty(None)  # Define username as a Kivy property
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.child_title = Label(text="Welcome, Child",
                                 font_size=24,
                                 color="#0000ff"
                                 )
        
        self.savings_goal_label = Label(text="", 
                                       font_size=16,
                                       color="#0000ff"
                                       )

        self.child_info = Label(text="Dashboard.",
                                font_size=16,
                                color="#0000ff"
                                )

        self.tasks_button = Button(text="List of Tasks",
                                   size_hint=(1, None),
                                   height=40,
                                   bold=True,
                                   background_color="#0000ff"
                                   )
        self.savings_goal_button = Button(text="Set Savings Goal",
                                          size_hint=(1, None),
                                          height=40,
                                          bold=True,
                                          background_color="#0000ff"
                                          )
        self.reward_button = Button(text="Reward",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )

        self.logout_button = Button(text="Logout",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )

        self.window.add_widget(self.child_title)
        self.window.add_widget(self.savings_goal_label) 
        self.window.add_widget(self.child_info)
        self.window.add_widget(self.tasks_button)
        self.window.add_widget(self.savings_goal_button)
        self.window.add_widget(self.reward_button)
        self.window.add_widget(self.logout_button)

        self.tasks_button.bind(on_press=self.tasks_button_click)
        self.savings_goal_button.bind(on_press=self.savings_goal_button_click)
        self.reward_button.bind(on_press=self.reward_button_click)
        self.logout_button.bind(on_press=self.logout_button_click)
        self.add_widget(self.window)

    def reward_button_click(self, instance):
        self.manager.current = "reward"
    def tasks_button_click(self, instance):
        self.manager.current = "child_tasks"

    def on_enter(self):
        # Fetch the username of the logged-in child
        username = self.username

        # Fetch the savings goal from the database using the username
        savings_goal = get_goals(username)  # Assume this function is correctly implemented

        # Update the label to display the fetched savings goal
        if savings_goal:
            self.savings_goal_label.text = f"Savings Goal: ${savings_goal}"
        else:
            self.savings_goal_label.text = "No Savings Goal Set"

    def update_savings_goal_label(self, goal):
        self.savings_goal_label.text = f"Savings Goal: ${goal}"
        
    def savings_goal_button_click(self, instance):
        self.manager.current = "savings_goal"

    def logout_button_click(self, instance):
        self.manager.current = "login"


class AssignedTasksScreen(BaseScreen):

    def on_enter(self):
        username = self.manager.username
        get_user_tasks(username)

        # Pass the tasks to def __init__ so that they can be displayed.
        self.tasks = get_user_tasks(username)
        # Print the tasks to the console for debugging purposes.
        print(self.tasks)
        # Call display_tasks to create and add widgets
        self.display_tasks()
        # Clear the screen of any widgets from the previous screen.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tasks = []

        # Add widgets for viewing assigned tasks here
        self.tasks_label = Label(text="Assigned Tasks",
                                 font_size=24,
                                 color="#0000ff"
                                 )
        self.window.add_widget(self.tasks_label)
        self.create_task = Button(text="Create Task",
                                  size_hint=(1, None),
                                  height=40,
                                  bold=True,
                                  background_color="#0000ff"
                                  )

        self.back_button = Button(text="Back to Parent Dashboard",
                                  size_hint=(1, None),
                                  height=40,
                                  bold=True,
                                  background_color="#0000ff"
                                  )

        # Binding the back button to return to the parent screen
        self.back_button.bind(on_press=self.back_button_click)
        self.create_task.bind(on_press=self.create_task_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def display_tasks(self):
        # Create a label for each task unique to the user and add it to the window.
        for task in self.tasks:
            task_id = task[1]
            task_name = task[2]
            task_desc = task[3]
            task_points = task[4]
            task_due = task[5]

            task_label = Label(
                text=f"Task ID: {task_id}\nTask Name: {task_name}\nTask Description: {task_desc}\nTask Points: {task_points}\nTask Due Date: {task_due}",
                font_size=16,
                color="#0000ff"
                )
            self.window.add_widget(task_label)
        task_button = Button(text="Add Task",
                             size_hint=(1, None),
                             height=40,
                             bold=True,
                             background_color="#0000ff"
                             )
        task_button.bind(on_press=self.task_button_click)
        self.window.add_widget(task_button)
        # Add Back Button
        return_button = Button(text="Back to Parent Dashboard",
                                 size_hint=(1, None),
                                 height=40,
                                 bold=True,
                                 background_color="#0000ff"
                                 )
        return_button.bind(on_press=self.back_button_click)
        self.window.add_widget(return_button)


    def task_button_click(self, instance):
        self.window.clear_widgets()
        self.manager.current = "create_task"

        if not self.tasks:
            self.window.add_widget(Label(text="No tasks assigned.",
                                         font_size=16,
                                         color="#0000ff"
                                         ))

    def back_button_click(self, instance):
        self.window.clear_widgets()
        # Navigate back to the parent screen
        self.manager.current = "parent"

    def create_task_click(self, instance):
        self.manager.current = "create_task"

    def return_button_click(self, instance):
        self.window.clear_widgets()
        self.manager.current = "parent"

class Child_Tasks(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.child_title = Label(text="Test",
                                 font_size=24,
                                 color="#0000ff"
                                 )

        self.back_button = Button(text="Back to Parent Dashboard",
                                  size_hint=(1, None),
                                  height=40,
                                  bold=True,
                                  background_color="#0000ff"
                                  )

        self.window.add_widget(self.child_title)
        self.window.add_widget(self.back_button)

        self.back_button.bind(on_press=self.back_button_click)
        self.add_widget(self.window)

    def back_button_click(self, instance):
        self.manager.current = "child"


class InvalidLoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.testtile = Label(text="Invalid Credentials",
                              font_size=20,
                              color="#0000ff"
                              )
        self.return_button = Button(text="Try Again",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )

        self.window.add_widget(self.testtile)
        self.window.add_widget(self.return_button)

        # Binding button
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def return_button_click(self, instance):
        self.manager.current = "login"


class InvalidAccCreation(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.testtile = Label(text="Unable to create account, ensure both fields are filled in.",
                              font_size=20,
                              color="#0000ff"
                              )
        self.return_button = Button(text="Return",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )

        self.window.add_widget(self.testtile)
        self.window.add_widget(self.return_button)

        # Binding button
        self.return_button.bind(on_press=self.return_button_click)

        # Add the GridLayout to the screen
        self.add_widget(self.window)

    def return_button_click(self, instance):
        self.manager.current = "login"


class Create_Task(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.task_title = Label(text="Create Task",
                                 font_size=24,
                                 color="#0000ff"
                                 )
        self.task_name = Label(text="Task Name:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.task_name_input = TextInput(multiline=False,
                                padding_y=(10, 10),
                                size_hint=(1.5, 1.5)
                                )
        self.task_desc = Label(text="Task Description:",
                               font_size=20,
                               color="#0000ff"
                               )
        self.task_desc_input = TextInput(multiline=False,
                                padding_y=(10, 10),
                                size_hint=(1.5, 1.5)
                                )
        self.task_points = Label(text="Task Points:",
                                 font_size=20,
                                 color="#0000ff"
                                 )
        self.task_points_input = TextInput(multiline=False,
                                  padding_y=(10, 10),
                                  size_hint=(1.5, 1.5)
                                  )
        self.task_due = Label(text="Task Due Date:",
                                    font_size=20,
                                    color="#0000ff"
                                    )
        self.task_due_input = TextInput(multiline=False,
                                     padding_y=(10, 10),
                                     size_hint=(1.5, 1.5)
                                     )
        self.create_task = Button(text="Create Task",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )
        self.back_button = Button(text="Back to Parent Dashboard",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )

        self.window.add_widget(self.task_title)
        self.window.add_widget(self.task_name)
        self.window.add_widget(self.task_name_input)
        self.window.add_widget(self.task_desc)
        self.window.add_widget(self.task_desc_input)
        self.window.add_widget(self.task_points)
        self.window.add_widget(self.task_points_input)
        self.window.add_widget(self.task_due)
        self.window.add_widget(self.task_due_input)
        self.window.add_widget(self.create_task)
        self.window.add_widget(self.back_button)

        self.create_task.bind(on_press=self.create_task_click)
        self.back_button.bind(on_press=self.back_button_click)
        self.add_widget(self.window)

    def create_task_click(self, instance):
        task_user = self.manager.username
        task_id = len(self.tasks) + 1
        task_name = self.task_name_input.text
        task_desc = self.task_desc_input.text
        task_points = self.task_points_input.text
        task_points = int(task_points)
        task_due = self.task_due_input.text

        if task_name and task_desc and task_points and task_due:
            # Add the tasks to the task database
            insert_task(task_user, task_id, task_name, task_desc, task_points, task_due)
            self.manager.current = "assigned_tasks"
        else:
            self.manager.current = "invalid_acc_creation"

    def back_button_click(self, instance):
        self.manager.current = "assigned_tasks"

class RewardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.reward_title = Label(text="Rewards",
                                  font_size=24,
                                  color="#0000ff"
                                  )

        self.reward_info = Label(text="Dashboard.",
                                 font_size=16,
                                 color="#0000ff"
                                 )

        self.logout_button = Button(text="Logout",
                                    size_hint=(1, None),
                                    height=40,
                                    bold=True,
                                    background_color="#0000ff"
                                    )

        self.window.add_widget(self.reward_title)
        self.window.add_widget(self.reward_info)
        self.window.add_widget(self.logout_button)

        self.logout_button.bind(on_press=self.logout_button_click)
        self.add_widget(self.window)

    def logout_button_click(self, instance):
        self.manager.current = "login"

class MyScreenManager(ScreenManager):
    username = StringProperty('')


class MyApp(App):
    def build(self):
        sm = MyScreenManager()

        reward_screen = RewardScreen(name="reward")
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
        create_task = Create_Task(name="create_task")

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
        sm.add_widget(create_task)
        sm.add_widget(reward_screen)
        sm.add_widget(SavingsGoalScreen(name="savings_goal"))

        return sm


if __name__ == '__main__':
    MyApp().run()

