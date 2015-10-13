from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class EksempelRoot(BoxLayout):
    pass


class EksempelApp(App):

    def build(self):
        return EksempelRoot()


if __name__ == "__main__":
    EksempelApp().run()
