from kivy.lang import Builder

from kivymd.app import MDApp

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("app_style_main.kv")


Example().run()