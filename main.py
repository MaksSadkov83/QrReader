from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
import time

class Tab(MDFloatLayout, MDTabsBase):
    pass
class QRReaderApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("QRReader.kv")

    def on_start(self):
        pass
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
        if count_icon == 'camera':
           pass
        elif count_icon == 'magnify':
            pass
        else:
            pass
    def capture(self):
        camera = self.root.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Есть фотка")




if __name__ == "__main__":
    QRReaderApp().run()