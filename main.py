"""
Kivy Interval Timer
Developed by Marco Baudisch
Focus: Logic handling and KivyMD integration
"""


from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window


#Window size
Config.set('graphics', 'resizable', False)
Window.size = (360, 640)


class WindowManager(ScreenManager):
    pass

class StartScreen(MDScreen):
    # Setting: Number of repetitions
    number_of_repetitions_max = 15
    number_of_repetitions_min = 1

    def number_of_repetitions_plus(self):
        app = MDApp.get_running_app()

        if app.repetitions < self.number_of_repetitions_max:
            app.repetitions += 1


    def number_of_repetitions_minus(self):
        app = MDApp.get_running_app()

        if app.repetitions > self.number_of_repetitions_min:
            app.repetitions -= 1


    #Setting: Duration of repetitions
    duration_of_repetitions_min = 25
    duration_of_repetitions_max = 60

    def duration_of_repetitions_plus(self):
        app = MDApp.get_running_app()

        if app.duration < self.duration_of_repetitions_max:
            app.duration += 5


    def duration_of_repetitions_minus(self):
        app = MDApp.get_running_app()

        if app.duration > self.duration_of_repetitions_min:
            app.duration -= 5

    #Setting: Rest interval
    rest_interval_max = 30
    rest_interval_min = 0

    def rest_interval_plus(self):
        app = MDApp.get_running_app()

        if app.rest < self.rest_interval_max:
            app.rest += 5


    def rest_interval_minus(self):
        app = MDApp.get_running_app()

        if app.rest > self.rest_interval_min:
            app.rest -= 5


class TrainingScreen(MDScreen):
    app = MDApp.get_running_app()

    pause_button = StringProperty("PAUSE")
    status = 1
    five_seconds = 5


    def before_start(self):
        app = MDApp.get_running_app()

        Clock.schedule_interval(self.update_5_sek, 1)
        app.status_text = "Starting ..."


    def update_5_sek(self, dt):
        app = MDApp.get_running_app()

        if self.five_seconds > 0:
            self.five_seconds -= 1

            minutes_f = self.five_seconds // 60

            seconds_f = self.five_seconds % 60

            app.timer_text = "{:02d} : {:02d}".format(int(minutes_f), int(seconds_f))
        else:
            self.timer_text = "00 : 00"
            self.start_timer()
            return False


    def update_timer(self, dt):
        MDapp = MDApp.get_running_app()
        if self.current_time > 0:
            self.current_time -= 1

            minutes = self.current_time // 60

            seconds = self.current_time % 60

            MDapp.timer_text = "{:02d} : {:02d}".format(int(minutes), int(seconds))
        else:
            self.start_timer()
            return False


    def start_timer(self):
        app = MDApp.get_running_app()

        if app.total_seconds > 0:
            if self.status == 1:
                self.current_time = app.duration
                self.status = 0
                app.timer_text = f"00 : {app.duration}"
                left = app.repetitions - 1
                if left > 0:
                    app.status_text = f"Go!!! Only {left} repetitions left"
                else:
                    app.status_text = "Last one, let’s go"
                app.total_seconds = app.total_seconds - app.duration

            elif self.status == 0:
                self.current_time = app.rest
                self.status = 1
                app.timer_text = f"00 : {app.rest}"
                app.total_seconds = app.total_seconds - app.rest
                app.repetitions = app.repetitions - 1
                app.status_text = f"Rest, only {app.repetitions} repetitions left"

            Clock.schedule_interval(self.update_timer, 1)

        else:
            app.timer_text = "You made it!"
            app.status_text = "Well done!"


    def pause(self):
        if self.pause_button == "PAUSE":
            self.pause_button = "RESUME"
            self.stop_timer()

        elif self.pause_button == "RESUME":
            self.pause_button = "PAUSE"
            self.update_timer(0)
            Clock.schedule_interval(self.update_timer, 1)


    def stop_timer(self):
        Clock.unschedule(self.update_timer)


    def intern_clear(self):
        self.pause_button = "Pause"
        self.status = 1
        self.five_seconds = 5


class GuiApp(MDApp):
    repetitions = NumericProperty(6)
    duration = NumericProperty(40)
    rest = NumericProperty(15)
    total_seconds = NumericProperty(0)
    timer_text = StringProperty("00 : 05")
    status_text = StringProperty("Go!!!")


    def connect_start_timer(self):
        self.total_seconds = self.duration * self.repetitions + self.rest * (self.repetitions - 1)

        training_seite = self.root.get_screen('training')
        training_seite.before_start()


    def clear(self):
        print("Cleared")
        self.repetitions = 6
        self.duration = 40
        self.rest = 15
        self.total_seconds = 0
        self.timer_text = "00 : 05"
        training_seite = self.root.get_screen('training')
        training_seite.stop_timer()
        training_seite.intern_clear()


    def debug(self):
        print('Debug:')
        print(self.repetitions)
        print(self.duration)
        print(self.rest)
        print(self.total_seconds)
        print(self.timer_text)


    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("gui.kv")


if __name__ == '__main__':
    GuiApp().run()
