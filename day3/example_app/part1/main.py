from kivy.app import App
from kivy.uix.button import Button


class EksempelApp(App):

    def build(self):
        return Button()


if __name__ == "__main__":
    EksempelApp().run()
