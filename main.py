from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons

KV = """
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    selected_color: "#0c6c4d"

MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:
                MDBoxLayout:
                    md_bg_color: "#FFFFFF"
                    orientation: "vertical"

                    MDTopAppBar:
                        title: "QR Reader"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#095EB1"
                        specific_text_color: "#FFFFFF"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                    MDTabs:
                        pos_hint: {"top": 2}
                        id: tabs

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "QR Reader"
                    text: "NAET V 0.4"
                    title_color: "#FFFFFF"
                    text_color: "#4a4939"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

                DrawerClickableItem:
                    icon: "github"
                    text: "GitHub"

                DrawerClickableItem:
                    icon: "brush"
                    text: "Поменять стиль"

                DrawerClickableItem:
                    icon: "cash"
                    text: "Спонсировать"

                DrawerClickableItem:
                    icon: "share-variant"
                    text: "Поделится"

                DrawerClickableItem:
                    icon: "account-edit"
                    text: "Написать разработчику"
"""
class Tab(MDFloatLayout, MDTabsBase):
    pass
class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        list_tabs = {
            "camera": "Камера",
            "magnify": "Реузльтат сканирования",
            "chat-question": "Справка",
        }
        for icon_tab, name_tab in list_tabs.items():
            self.root.ids.tabs.add_widget(Tab(icon=icon_tab, title=name_tab))



if __name__ == "__main__":
    Example().run()