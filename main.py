from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
# from kivymd.uix.pickers import MDDatePicker

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.dialog import MDDialog

import webbrowser
import cv2
import sqlite3


ContentAddDialog = """
MDBoxLayout:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "440dp"
                                
    MDTextField:
        hint_text: "№ ИНВ"
                                
    MDTextField:
        hint_text: "Модель"
                                
    MDTextField:
        hint_text: "Кабинет"
                                
    MDTextField:
        hint_text: "Стоимость"
                                
    MDBoxLayout:
        orientation: "horizontal"
        MDFloatingActionButton:
            icon: "calendar"
            on_release: app.show_date_picker()
        MDLabel:
            text: ""
        MDLabel:
            id: datapicker
            text: ""
                                
    MDBoxLayout:
        orientation: "horizontal"
        Button:
            text: "Add"
            size_hint_y: None
            height: '48dp'
                                
        Button:
            text: "Reset"
            size_hint_y: None
            height: '48dp'
"""

class Tab(MDFloatLayout, MDTabsBase):
    pass

class InvNaetApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("InvNaet.kv")

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

    def show_date_picker(self):
        pass

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.root.ids['camera']
        result = self.root.ids['result']
        camera.export_to_png("/storage/emulated/0/Pictures/QRCODE.png")
        img_qr = cv2.imread("/storage/emulated/0/Pictures/QRCODE.png")
        detector = cv2.QRCodeDetector()
        data, bbpx, clear_qr = detector.detectAndDecode(img_qr)
        try:
            conn = sqlite3.connect("QR.db")
            cur = conn.cursor()
            res = cur.execute(f"SELECT * FROM qr WHERE inv='{data}'")
            result_bd = res.fetchone()
            result.text = f"{result_bd[2]}\n\n{result_bd[1]}\n\n{result_bd[3]}\n\n{result_bd[4]}\n\n{result_bd[5]} RUB"
            self.root.ids.tabs.switch_tab(search_by="icon", name_tab="magnify")
        except:
            dialog = MDDialog(title="Что-то пошло не так :(",
                              text="Похоже алгоритм не смог обработать фотографию.\nВозможные ошибки:\n1. На фотографии нету qr-кода;\n2. Фотография размыта.\nПожалуйста, попробуйте снова.")
            dialog.open()
        finally:
            if conn:
                conn.close()

    def search_by_inv(self):
        text_field = self.root.ids['text_field']
        result = self.root.ids['result']

        try:
            conn = sqlite3.connect("QR.db")
            cur = conn.cursor()
            res = cur.execute(f"SELECT * FROM qr WHERE inv='{text_field.text}'")
            result_bd = res.fetchone()
            result.text = f"{result_bd[2]}\n\n{result_bd[1]}\n\n{result_bd[3]}\n\n{result_bd[4]}\n\n{result_bd[5]} RUB"
        except:
            dialog = MDDialog(title="Что-то пошло не так :(",
                              text="Похоже алгоритм не смог найти оборудование.\nВозможные ошибки:\n1. Вы неправильно ввели № ИНВ, пожалуйста, попробуйте снова;\n2. Оборудования с таким ИНВ нету в базе. Обратитесь к администратору.")
            dialog.open()
        finally:
            if conn:
                conn.close()

    def content_add_equipment(self):
        self.dialog = MDDialog(
            title="Добавление оборудования:",
            type="custom",
            content_cls= Builder.load_string(ContentAddDialog),
        )
        self.dialog.open()

    def github(self):
        url = "https://github.com/MaksSadkov83/QrReader/releases"
        webbrowser.open(url, new=0, autoraise=True)

    def callback_for_menu_items(self, *args):
        if args[0] == "Telegram":
            url = "https://t.me/+79110673159"
            webbrowser.open(url, new=0, autoraise=True)
        elif args[0] == "WhatsApp":
            url = "http://Wa.me/+79110673159"
            webbrowser.open(url, new=0, autoraise=True)
        elif args[0] == "VK":
            url = "https://vk.com/smnxzmn"
            webbrowser.open(url, new=0, autoraise=True)
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

if __name__ == "__main__":
    InvNaetApp().run()