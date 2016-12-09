from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty

on = 0
off = 0

class OffOnRoot(FloatLayout):
    av_property = NumericProperty(0)
    paa_property = NumericProperty(0)

class OffOnApp(App):

    def build(self):
        return OffOnRoot()


if __name__ == '__main__':
    OffOnApp().run()
