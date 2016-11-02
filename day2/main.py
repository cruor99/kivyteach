from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class KalkulatorRoot(GridLayout):

    def calculation(self, calculation):
        if calculation:
            try:
                self.ids.entry.text = str(eval(calculation))
            except:
                self.ids.entry.text = "Error"


class KalkulatorApp(App):

    def build(self):
        return KalkulatorRoot()


if __name__ == "__main__":
    KalkulatorApp().run()
