from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from plyer import filechooser
from kivy.uix.popup import Popup
from kivy.animation import Animation
from datetime import date, datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivymd.uix.pickers import MDTimePicker


Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '268')
Config.set('graphics', 'height', '565')

class Home(Screen):
    def file_chooser(self):
        # Open the file chooser with multiselect enabled
        filechooser.open_file(on_selection=self.selected, multiselect=True)

    def selected(self, selection):
        # Store the selected files in a class attribute
        self.selected_files = selection

        # Process the selected files
        if selection:
            self.manager.get_screen('cc').ids.selected_path.text = f"{len(selection)} files selected"
        else:
            # Handle the case when no files are selected
            self.manager.get_screen('cc').ids.selected_path.text = "No files selected"

        # Enable or disable the button based on the number of selected files
        self.manager.get_screen('cc').ids.proceed_button.disabled = not bool(selection)

class Cc(Screen, MDApp): 
    unlock_date_time = None  # Initialize unlock date and time

    def invalid(self):
        name = self.capsulenameone.text
        date_text = self.ids.unlockdate.text
        time_text = self.ids.unlocktime.text

        if not name or not date_text or date_text == 'MM/DD/YYYY' or time_text == 'HH:MM AM/PM':
            # Highlight invalid fields with a red background
            if not name:
                self.capsulenameone.background_color = (1, 0, 0, 1)
            else:
                self.capsulenameone.background_color = (1, 1, 1, 1)

            if not date_text or date_text == 'MM/DD/YYYY':
                self.ids.unlockdate.background_color = (1, 0, 0, 1)
            else:
                self.ids.unlockdate.background_color = (1, 1, 1, 1)

            if not time_text or time_text == 'HH:MM AM/PM':
                self.ids.unlocktime.background_color = (1, 0, 0, 1)
            else:
                self.ids.unlocktime.background_color = (1, 1, 1, 1)

            return True
        else:
            # Reset background colors and proceed with capsule creation or other actions
            self.capsulenameone.background_color = (1, 1, 1, 1)
            self.ids.unlockdate.background_color = (1, 1, 1, 1)
            self.ids.unlocktime.background_color = (1, 1, 1, 1)
            return False
        
    def on_save_date(self, instance, value, date_range):
        # Get the current date
        current_date = date.today()

        # Check if the chosen date is less than the current date
        if value < current_date:
            # Show an error message
            self.show_error_message('Please select a date on or after the current date')
        else:
            # Update the text field with the chosen date
            self.ids.unlockdate.text = str(value) 

    def on_cancel_date(self, instance, value):
        pass

    def sdp_date(self):
        # Get the current date
        current_date = date.today()

        # Create MDDatePicker with min_date set to the current date
        d = MDDatePicker(min_date=current_date)
        
        d.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
        d.open()

    def sdp_time(self):
        if self.unlock_date_time:
            # Extract the current time from the unlock date and time
            current_time = self.unlock_date_time.time()

            # Create MDTimePicker with the current time set
            time_picker = MDTimePicker()
            time_picker.set_time(current_time)
            time_picker.bind(on_save=self.on_save_time)

            time_picker.open()

    def on_save_time(self, instance, time):
        # Update the unlock time when the user selects a time
        self.unlock_date_time = self.unlock_date_time.replace(hour=time.hour, minute=time.minute)
        self.ids.unlocktime.text = str(time.strftime("%I:%M %p"))  # Update the displayed time

    def createcapsule(self):
        name = self.capsulenameone.text
        date_text = self.ids.unlockdate.text
        time_text = self.ids.unlocktime.text

        if name and date_text != 'MM/DD/YYYY' and time_text != 'HH:MM AM/PM':
            # Convert date and time strings to datetime objects
            unlock_date = datetime.strptime(f"{date_text} {time_text}", "%m/%d/%Y %I:%M %p")

            # Calculate the remaining time until unlock
            remaining_time = (unlock_date - datetime.now()).total_seconds()

            if remaining_time <= 0:
                # Unlock the capsule if the specified date and time have passed
                self.unlock_capsule()
            else:
                # Schedule the unlocking process at the specified date and time
                Clock.schedule_once(self.unlock_capsule, remaining_time)

            # Reset input fields and background colors
            self.reset()

    def unlock_capsule(self, *args):
        # Perform the capsule unlocking process here
        # This can include displaying a message, enabling access to files, etc.
        self.show_error_message('Capsule unlocked!')

    def on_press_submit(self):
        # Check for invalid information before proceeding
        if self.invalid():
            # If information is invalid, show an error message
            self.show_error_message('Please fill out all information')
        else:
            # If information is valid, create the capsule and switch screens
            self.createcapsule()
            self.manager.current = "home"
            self.manager.transition.direction = "right"

    def show_error_message(self, message):
        ii = Label(text=message, pos_hint={'center_x': 0.5, 'center_y': 0.2}, opacity=0, color=(1, 0, 0, 1))
        anim = Animation(opacity=1, duration=0.5) + Animation(opacity=0, duration=0.7)
        self.add_widget(ii)
        anim.start(ii)

    def reset(self):
        self.capsulenameone.text = ""
        self.ids.unlockdate.text = "MM/DD/YYYY"
        self.ids.unlocktime.text = "HH:MM AM/PM"
        self.capsulenameone.background_color = (1, 1, 1, 1)  # Reset background color
        self.ids.unlockdate.background_color = (1, 1, 1, 1)  # Reset background color
        self.ids.unlocktime.background_color = (1, 1, 1, 1)  # Reset background color

class WindowManager(ScreenManager):
    pass

class FloatLayout(FloatLayout):
    pass

kv = Builder.load_file("screenstuff.kv")

class MyApp(MDApp):
    def build(self):
        self.title='DUBI'
        screenw = 268
        screenh = 565
        Window.size = (screenw,screenh)
        return kv

if __name__ == "__main__":
    MyApp().run()
