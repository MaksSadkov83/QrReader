from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers.datepicker.datepicker import MDDatePicker
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button

import webbrowser
import cv2
import sqlite3

class UpdatePropertyContent(MDBoxLayout):
    date = None

    def find_update_property(self):

        def show_datapicker_update(x):
            print(x)
            datapicker = MDDatePicker()
            datapicker.bind(on_save=on_save, on_cancel=on_cancel)
            datapicker.open()

        def on_save(instance, value, date_range):
            '''
            Events called when the "OK" dialog box button is clicked.

            :type instance: <kivymd.uix.picker.MDDatePicker object>;
            :param value: selected date;
            :type value: <class 'datetime.date'>;
            :param date_range: list of 'datetime.date' objects in the selected range;
            :type date_range: <class 'list'>;
            '''
            self.date = str(value)
            label_claendar.text = str(value)

        def on_cancel(instance, value):
            '''Events called when the "CANCEL" dialog box button is clicked.'''

        def loud_update_content(x):
            conn = sqlite3.connect("QR.db")
            cur = conn.cursor()
            cur.execute(f"UPDATE qr SET name='{model.text}', inv='{inv.text}', cabinet='{cabinet.text}', date='{self.date}', price='{price.text}' WHERE id='{result_bd[0]}'")
            conn.commit()
            MDDialog(title=f"Имущество с инвентарным номером {inv.text} обновлена !!!").open()


        inv_update = self.ids['inv_update']
        button_update = self.ids['button_update']

        conn = sqlite3.connect("QR.db")
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM qr WHERE inv='{inv_update.text}'")
        result_bd = res.fetchone()

        if result_bd is None:
            MDDialog(title=f"Имущества с ивнентарным номером {inv_update.text} нет в базу данных").open()

        else:
            self.remove_widget(inv_update)
            self.remove_widget(button_update)

            inv = MDTextField(id="inv", hint_text="№ ИНВ")
            model = MDTextField(id="model", hint_text="Модель")
            cabinet = MDTextField(id="cabinet", hint_text="Кабинет")
            price = MDTextField(id="price", hint_text="Стоимость")
            calendar_button = MDFloatingActionButton(icon="calendar")
            calendar_button.bind(on_release=show_datapicker_update)
            box = MDBoxLayout(orientation="horizontal")
            label_claendar = MDLabel(text="", id="calendar")
            box1 = MDBoxLayout(orientation="horizontal")
            update_button = Button(text="Update", size_hint_y=None, height="48dp")
            update_button.bind(on_press=loud_update_content)

            self.add_widget(inv)
            self.add_widget(model)
            self.add_widget(cabinet)
            self.add_widget(price)
            box.add_widget(calendar_button)
            box.add_widget(MDLabel(text=""))
            box.add_widget(label_claendar)
            self.add_widget(box)
            box1.add_widget(update_button)
            self.add_widget(box1)

            inv.text = f"{result_bd[2]}"
            model.text = f"{result_bd[1]}"
            cabinet.text = f"{result_bd[3]}"
            price.text = f"{result_bd[5]}"
            label_claendar.text = f"{result_bd[4]}"
            self.date = f"{result_bd[4]}"

class DeletePropertyContent(MDBoxLayout):
    def delete_property(self):
        inv_delete = self.ids['inv_delete']

        if inv_delete.text != "":
            conn = sqlite3.connect("QR.db")
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM qr WHERE inv = '{inv_delete.text}'")
            if cur.fetchone() is None:
                MDDialog(title="Что-то пошло не так :(",
                         text=f"Имущества с номером {inv_delete.text} нет в базе данных").open()
            else:
                cur.execute(f"DELETE FROM qr WHERE inv='{inv_delete.text}'")
                conn.commit()
                MDDialog(title=f"Имущество с номером {inv_delete.text} успешно удалено !!!").open()

                inv_delete.text = ""

            conn.close()
        else:
            MDDialog(title="Поле обязательно для заполнения !!!").open()

    def reset_form(self):
        inv_delete = self.ids['inv_delete']
        inv_delete.text = ""

class AddPropertyContent(MDBoxLayout):
    date = None

    def show_datapicker(self):
        datapicker = MDDatePicker()
        datapicker.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        datapicker.open()

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        self.date = str(value)
        data = self.ids['calendar']
        data.text = str(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def add_property(self):
        inv = self.ids['inv']
        model = self.ids['model']
        cabinet = self.ids['cabinet']
        price = self.ids['price']
        data = self.ids['calendar']

        if inv.text != "" and model.text != "" and cabinet.text != "" and price.text != "" and data.text != "":
            if float(price.text) >= 0:
                try:
                    conn = sqlite3.connect("QR.db")
                    cur = conn.cursor()
                    cur.execute(
                        f"INSERT INTO qr(name, inv, cabinet, date, price) VALUES('{model.text}', '{inv.text}', '{cabinet.text}', '{data.text}', '{price.text}')")
                    conn.commit()
                    MDDialog(title="Запись успешно добавлена !!!").open()
                    inv.text = ""
                    model.text = ""
                    cabinet.text = ""
                    price.text = ""
                    data.text = ""

                except:
                    MDDialog(title="Что-то пошло не так :(",
                             text="Возможные ошибки: \n1. Нету соединения с базой данных").open()
                finally:
                    if conn:
                        conn.close()
            else:
                MDDialog(title="Поле 'Цена' должна быть цифрой больше или равно 0").open()
                price.text = ""

    def reset_form(self):
        inv = self.ids['inv']
        model = self.ids['model']
        cabinet = self.ids['cabinet']
        price = self.ids['price']
        data = self.ids['calendar']

        inv.text = ""
        model.text = ""
        cabinet.text = ""
        price.text = ""
        data.text = ""

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
            text_field.text = ""
        except:
            dialog = MDDialog(title="Что-то пошло не так :(",
                              text="Похоже алгоритм не смог найти оборудование.\nВозможные ошибки:\n1. Вы неправильно ввели № ИНВ, пожалуйста, попробуйте снова;\n2. Оборудования с таким ИНВ нету в базе. Обратитесь к администратору.")
            dialog.open()
            result.text = ""
        finally:
            if conn:
                conn.close()

    def content_add_property(self):
        self.dialog = MDDialog(
            title="Добавление оборудования:",
            type="custom",
            content_cls= AddPropertyContent(),
        )
        self.dialog.open()

    def content_delete_property(self):
        self.dialog = MDDialog(
            title="Удаление имущества:",
            type="custom",
            content_cls=DeletePropertyContent(),
        )
        self.dialog.open()

    def content_update_property(self):
        self.dialog = MDDialog(
            title="Обновление имущества:",
            type="custom",
            content_cls=UpdatePropertyContent(),
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