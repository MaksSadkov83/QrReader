from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class QrReaderApp(MDApp):
    def build(self):
        return MDLabel(text="PRIVET MIR !!!", halign="center")

if __name__ == "__main__":
    QrReaderApp().run()

