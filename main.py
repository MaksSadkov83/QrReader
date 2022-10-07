from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
import time
from kivymd.uix.label import MDLabel

class Tab(MDFloatLayout, MDTabsBase):
    pass
class QRReaderApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("QRReader.kv")

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        count_icon = instance_tab.icon  # get the tab icon


    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.root.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))

    def reader_qr(self):
        pass

    def github(self):
        pass

    def style_change(self):
        pass

    def callback_for_menu_items(self, *args):
        toast(args[0])

    def show_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "WhatsApp": "whatsapp",
            "VK": "chat",
            "Telegram": "navigation-variant"
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()

    def write_to_developer(self):
        pass

if __name__ == "__main__":
    QRReaderApp().run()