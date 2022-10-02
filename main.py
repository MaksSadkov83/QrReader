from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons


class Tab(MDFloatLayout, MDTabsBase):
    pass
class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("app_style_main.kv")

    def on_start(self):
        list_tabs = {
            "camera": "Камера",
            "magnify": "Реузльтат сканирования",
            "chat-question": "Справка",
        }
        for icon_tab, name_tab in list_tabs.items():
            self.root.ids.tabs.add_widget(Tab(icon=icon_tab, title=name_tab))



Example().run()