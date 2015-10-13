from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class EksempelRoot(BoxLayout):

    def endre_label(self):
        self.ids.eksempellabel.text = self.ids.eksempelinput.text

class EksempelApp(App):

    def build(self):
        return EksempelRoot()


if __name__ == "__main__":
    EksempelApp().run()
