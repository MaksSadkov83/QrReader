from kivy.lang import Builder
from plyer import storagepath

from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import TwoLineListItem
from kivy.clock import Clock
from functools import partial

import webbrowser
import cv2
import sqlite3


class Tab(MDFloatLayout, MDTabsBase):
    pass


class InvNaetApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("InvNaet.kv")

    def login(self):
        sm = self.root
        login = self.root.ids['login_name']
        password = self.root.ids['password']

        sm.current = "Load"
        sm.transition.direction = 'left'

        Clock.schedule_once(partial(self.check, login, password, sm), 5)

    def check(self, login, password, sm, *largs):
        if login.text == 'maks' and password.text == '12345':
            sm.current = "Main"
            sm.transition.direction = 'left'
            sidebar = self.root.ids['sidebar']
            sidebar.title += " maks"
            snackbar = Snackbar(
                text="Вход успешно выполнен",
                snackbar_x="10dp",
                snackbar_y="10dp",
            )
            snackbar.open()
        elif login.text == "" and password.text == "":
            sm.current = "loginview"
            sm.transition.direction = 'right'
            snackbar = Snackbar(
                text="Логин и пароль пусты",
                snackbar_x="10dp",
                snackbar_y="10dp",
            )
            snackbar.open()
        else:
            sm.current = "loginview"
            sm.transition.direction = 'right'
            snackbar = Snackbar(
                text="Неправильно введен логин или пароль",
                snackbar_x="10dp",
                snackbar_y="10dp",
            )
            snackbar.open()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
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
        result = self.root.ids['filter-result']
        filter = self.root.ids['filter']
        camera.export_to_png(f"{storagepath.get_pictures_dir()}/QRCODE.png")
        img_qr = cv2.imread(f"{storagepath.get_pictures_dir()}/QRCODE.png")
        detector = cv2.QRCodeDetector()
        data, bbpx, clear_qr = detector.detectAndDecode(img_qr)

        if result.children:
            try:
                conn = sqlite3.connect("QR.db")
                cur = conn.cursor()
                cur.execute(f"SELECT name,inv,cabinet FROM qr WHERE inv='{data}'")
                res = cur.fetchone()

                if res[2][:2] != filter.text[:2]:
                    MDDialog(title="Найдено имущество находитя не в этом кабинете!!!",
                             text=f"Имущество {res[0]} с инвентарным номером {res[1]} находится не в этом кабинете. \n"
                                  f"Он должен находится в кабиете {res[2]}. Имущество помещено в конец списка.").open()
                    item = TwoLineListItem(text=res[0],
                                           secondary_text=f'№ ИНВ: {res[1]};    Кабинет: {res[2]}',
                                           bg_color="#f7ff0d",
                                           theme_text_color="ContrastParentBackground",
                                           secondary_theme_text_color='ContrastParentBackground')
                    result.add_widget(item)

                for row in result.children:
                    if row.id == res[1]:
                        row.bg_color = "#0dff11"
                        row.theme_text_color = "ContrastParentBackground"

                cur.execute(f"UPDATE qr SET chek='1' WHERE inv='{data}'")
                conn.commit()

            except Exception as _ex:
                MDDialog(title='Что-то пошло не так :(',
                         text=f'Алгоритм не смог найти имущество {data}!!\n'
                              'Возможные ошибки:\n1. На фотографии нету qr-кода\n 2. Фотография размыта').open()
            finally:
                if conn:
                    conn.close()
        else:
            MDDialog(title="Пожалуйста выберите кабинет").open()

    def search_by_inv(self):
        '''
        Функций поиска имущества оп инвентарному номеру
        :return:
        '''
        text_field = self.root.ids['text_field']
        result = self.root.ids['filter-result']
        filter = self.root.ids['filter']

        # Проверка выбран ли кабинет для сканирования
        if result.children:
            # Поиск имущества
            try:
                conn = sqlite3.connect("QR.db")
                cur = conn.cursor()
                cur.execute(f"SELECT name, inv, cabinet FROM qr WHERE inv='{text_field.text}'")
                res = cur.fetchone()

                # Проверка, есть ли найденно имущестов в списке (совпадение с фильтром), если нет добавляется как желтая пометка
                if res[2][:2] != filter.text[:2]:
                    MDDialog(title="Найдено имущество находится не в этом кабинете",
                             text=f"Имущество {res[0]} с инвентарным номером {res[1]} находится не в этом кабинете. \n"
                                  f"Он должен находится в кабиете {res[2]}").open()
                    item = TwoLineListItem(text=res[0],
                                           secondary_text=f'№ ИНВ: {res[1]};    Кабинет: {res[2]}',
                                           bg_color="#f7ff0d",
                                           theme_text_color="ContrastParentBackground",
                                           secondary_theme_text_color='ContrastParentBackground')
                    result.add_widget(item)

                # Поиск имущества в списке и закрашивание его в списке зеленым
                for row in result.children:
                    if row.id == res[1]:
                        row.bg_color = "#0dff11"
                        row.theme_text_color = "ContrastParentBackground"

                # Обновление состояния с "0" на "1"
                cur.execute(f"UPDATE qr SET chek='1' WHERE inv='{text_field.text.upper()}'")
                conn.commit()
                text_field.text = ""

            # Вывод сообщения о ошибке
            except Exception as _ex:
                MDDialog(title="Что-то пошло не так :(",
                         text=f"Алгоритм не нашел имущество с номером {text_field.text.upper()}. \nВозможные ошибки:\n"
                              f"1. имущества с таким № ИНВ нет в базе данных;\n2. Неправильно введен № ИНВ.\n"
                              f"Пожалуйста попробуйте снова.").open()
            finally:
                if conn:
                    conn.close()

        else:
            MDDialog(title="Пожалуйста выберите кабинет").open()

    def filter_property_cabinet(self):
        '''
        Функция создания списка с фильтрами

        :return:
        '''
        # список с кабинетами
        cabinet = ["спортзал", "2", "3", "4", "мед", "столовая",
                   "6", "7", "8", "9", "10", "11", "12", "13",
                   "14", "15", "16", "17", "20", "директор", "22", "23", "24",
                   "25", "26", "27", "28", "29", "30", "31", "32",
                   "33", "34", "36", "37", "38", "акт", "хим.анализ",
                   "театр", "охрана", "холл", "склад", "подвал", "подвал-общежитие",
                   "общ"]

        # сосздание выпадающего списка с фильтрами
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.filter_property_find(x),
            } for i in cabinet
        ]
        MDDropdownMenu(
            caller=self.root.ids.button,
            items=menu_items,
            width_mult=4,
        ).open()

    def filter_property_find(self, x):
        '''
        Функция поиска оборудования по фильтру

        :param x:
        :return:
        '''
        result = self.root.ids['filter-result']
        filter = self.root.ids['filter']
        filter.text = x

        conn = sqlite3.connect("QR.db")
        cur = conn.cursor()

        if x == 'общ' or x == 'акт' or x == 'мед' or x == '20' or x == '10':
            cur.execute(f"SELECT name, inv, chek FROM qr WHERE cabinet LIKE '{x}%'")
        else:
            cur.execute(f"SELECT name, inv, chek FROM qr WHERE cabinet = '{x}'")

        res = cur.fetchall()

        if result.children:
            result.clear_widgets()

        color = {
            0: "#7d7d7d",
            1: "#0dff11"
        }

        bg_color = {
            0: "Primary",
            1: "ContrastParentBackground",
        }

        for row in res:
            item = TwoLineListItem(
                text=row[0],
                secondary_text=f'№ ИНВ: {row[1]}',
                bg_color=color[row[2]],
                theme_text_color=bg_color[row[2]],
                id=row[1]
            )

            result.add_widget(item)

        conn.close()

    def content_send_database(self):
        MDDialog(title="Отправка найденного имущества на сервер",
                 text=f"Функция отправляет ID найденного имущества и ID пользователя кто его нашел").open()

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

    def quit_app(self):
        sm = self.root
        login = self.root.ids['login_name']
        password = self.root.ids['password']

        login.text = ""
        password.text = ""

        sm.current = "loginview"
        sm.transition.direction = 'right'


if __name__ == "__main__":
    InvNaetApp().run()
