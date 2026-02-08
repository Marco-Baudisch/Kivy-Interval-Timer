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
from math import ceil


#Window size for desktop testing only
Config.set('graphics', 'resizable', False)
Window.size = (360, 640)


class WindowManager(ScreenManager):
    pass


class StartScreen(MDScreen):
    #Settings
    def minus(self, button_type):
        app = MDApp.get_running_app()

        if button_type == "repetitions":
             min_val = app.repetition_properties[1]
             steps = app.repetition_properties[2]
             current = app.repetition_properties[3]
        elif button_type == "dur_repetitions":
            min_val = app.duration_properties[1]
            steps = app.duration_properties[2]
            current = app.duration_properties[3]
        elif button_type == "rest":
            min_val = app.rest_properties[1]
            steps = app.rest_properties[2]
            current = app.rest_properties[3]


        if current > min_val:
            current -= steps

            if button_type == "repetitions":
                app.repetitions = current
            elif button_type == "dur_repetitions":
                app.duration = current
            elif button_type == "rest":
                app.rest = current


    def plus(self, button_type):
        app = MDApp.get_running_app()

        if button_type == "repetitions":
             max_val = app.repetition_properties[0]
             steps = app.repetition_properties[2]
             current = app.repetition_properties[3]
        elif button_type == "dur_repetitions":
            max_val = app.duration_properties[0]
            steps = app.duration_properties[2]
            current = app.duration_properties[3]
        elif button_type == "rest":
            max_val = app.rest_properties[0]
            steps = app.rest_properties[2]
            current = app.rest_properties[3]


        if current < max_val:
            current += steps

            if button_type == "repetitions":
                app.repetitions = current
            elif button_type == "dur_repetitions":
                app.duration = current
            elif button_type == "rest":
                app.rest = current


class TrainingScreen(MDScreen):
    app = MDApp.get_running_app()

    pause_button = StringProperty("PAUSE")
    status = 2
    five_seconds = 5


    def before_start(self):
        app = MDApp.get_running_app()
        self.status = 2

        Clock.schedule_interval(self.update_5_seconds, 1)
        app.status_text = "Starting ..."


    def update_5_seconds(self, dt):
        app = MDApp.get_running_app()

        if self.five_seconds > 0:
            self.five_seconds -= 1
            minutes_f = self.five_seconds // 60
            seconds_f = self.five_seconds % 60

            app.timer_text = "{:02d} : {:02d}".format(int(minutes_f), int(seconds_f))
        else:
            self.timer_text = "00 : 00"
            self.status = 1
            self.start_timer()
            return False


    def update_timer(self, dt):
        app = MDApp.get_running_app()

        if self.current_time > 0:
            self.current_time -= dt

            if self.current_time < 0:
                self.current_time = 0
            current_time_display = ceil(self.current_time)
            minutes = current_time_display // 60
            seconds = current_time_display % 60

            app.timer_text = "{:02d} : {:02d}".format(int(minutes), int(seconds))
        else:
            self.start_timer()
            return False


    def start_timer(self):
        app = MDApp.get_running_app()
        self.stop_timer()

        if app.total_seconds > 0:
            if self.status == 1:
                self.current_time = app.duration
                self.status = 0
                app.timer_text = f"00 : {app.duration}"
                left = app.repetitions - 1
                if left > 0:
                    app.status_text = f"{left} repetitions left"
                else:
                    app.status_text = "Last repetition!"
                app.total_seconds = app.total_seconds - app.duration

            elif self.status == 0:
                self.current_time = app.rest
                self.status = 1
                app.timer_text = f"00 : {app.rest}"
                app.total_seconds = app.total_seconds - app.rest
                app.repetitions = app.repetitions - 1
                app.status_text = f"Rest! {app.repetitions} repetitions left"

            Clock.schedule_interval(self.update_timer, 1/10)

        else:
            app.timer_text = "You made it!"
            app.status_text = "Well done!"


    def pause(self):
        app = MDApp.get_running_app()

        if self.status == 2:
            self.stop_timer()
            app.clear()
            self.manager.transition.direction = 'right'
            self.manager.current = 'menu'
        else:
            if self.pause_button == "PAUSE":
                self.pause_button = "RESUME"
                self.ids.pause_button.md_bg_color = [0.9, 0.3, 0.3, 1]
                self.stop_timer()

            elif self.pause_button == "RESUME":
                self.pause_button = "PAUSE"
                self.ids.pause_button.md_bg_color = app.theme_cls.primaryColor
                self.stop_timer()
                self.update_timer(0)
                Clock.schedule_interval(self.update_timer, 1/10)

    def stop_timer(self):
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.update_5_seconds)


    def intern_clear(self):
        app = MDApp.get_running_app()

        self.pause_button = "PAUSE"
        self.status = 1
        self.five_seconds = 5
        self.ids.pause_button.md_bg_color = app.theme_cls.primaryColor


class GuiApp(MDApp):
    repetitions = NumericProperty(6)
    duration = NumericProperty(40)
    rest = NumericProperty(15)
    total_seconds = NumericProperty(0)
    timer_text = StringProperty("00 : 05")
    status_text = StringProperty("Go!!!")

    #Settings properties: max, min, steps, start
    @property
    def repetition_properties(self):
        return [15, 1, 1, int(self.repetitions)]

    @property
    def duration_properties(self):
        return [60, 25, 5, int(self.duration)]

    @property
    def rest_properties(self):
        return [30, 0, 5, int(self.rest)]


    def connect_start_timer(self):
        self.total_seconds = self.duration * self.repetitions + self.rest * (self.repetitions - 1)

        training_site = self.root.get_screen('training')
        training_site.before_start()


    def clear(self):
        print("Cleared")
        self.repetitions = 6
        self.duration = 40
        self.rest = 15
        self.total_seconds = 0
        self.timer_text = "00 : 05"
        training_site = self.root.get_screen('training')
        training_site.stop_timer()
        training_site.intern_clear()


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
