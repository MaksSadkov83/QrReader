from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
import webbrowser
import cv2

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
        pass

    def switch_tab_by_name(self):
        self.root.ids.tabs.switch_tab("magnify", search_by='icon')

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        #/storage/emulated/0/Pictures/
        camera = self.root.ids['camera']
        result = self.root.ids['result']
        camera.export_to_png("/storage/emulated/0/Pictures/QR_CODE.png")
        self.switch_tab_by_name()
        qrimg = cv2.imread("/storage/emulated/0/Pictures/QR_CODE.png")
        detector = cv2.QRCodeDetector()
        data, bbox, clear_qrcode = detector.detectAndDecode(qrimg)
        result.text = data


    def github(self):
        url = "https://github.com/MaksSadkov83/QrReader/releases"
        webbrowser.open(url, new=0, autoraise=True)

    def style_change(self):
        pass

    def callback_for_menu_items(self, *args):
        if args[0] == "Telegram":
            url = "https://web.telegram.org/k/#1187734754"
            webbrowser.open(url, new=0, autoraise=True)
        elif args[0] == "WhatsApp":
            url = "http://Wa.me/+79110673159"
            webbrowser.open(url, new=0, autoraise=True)
        elif args[0] == "VK":
            url = "https://vk.com/smnxzmn"
            webbrowser.open(url, new=0, autoraise=True)
        toast(args[0])

    # DrawerClickableItem:
    # icon: "share-variant"
    # on_press: app.show_grid_bottom_sheet()
    # text: "Поделится"

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

if __name__ == "__main__":
    QRReaderApp().run()