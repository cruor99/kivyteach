# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen


class SecondScreen(Screen):
    second_number = NumericProperty(0)

    def update_hovedtall(self, number):
        # Henter tallet fra roten
        htall = App.get_running_app().root.hovedtall
        # Oppdaterer kun htall variabelen
        htall = number
        print htall
        # Oppdater originale tallet i roten
        App.get_running_app().root.hovedtall = htall
        # Legg det til i labelen
        self.ids.hoved_test_label.text = str(htall)

    def increment_first_number(self):
        # henter tallet fra første skjermen
        first_number = self.manager.get_screen("first_screen").first_number
        # oppdaterer kun variabelen
        first_number += 1
        print first_number
        # oppdaterer originale tallet
        self.manager.get_screen("first_screen").first_number = first_number
        self.ids.increment_test_label.text = str(first_number)


class FirstScreen(Screen):
    first_number = NumericProperty(0)

    def update_hovedtall(self, number):
        htall = App.get_running_app().root.hovedtall
        print htall
        # oppdaterer htall variabel, men ikke originale tallet
        htall = number
        print htall
        # Oppdaterer originale tallet
        App.get_running_app().root.hovedtall = htall
        # Legg det til i labelen
        self.ids.hoved_test_label.text = str(htall)

    def increment_second_number(self):
        # Henter tallet fra den andre skjermen
        second_number = self.manager.get_screen("second_screen").second_number
        # oppdaterer kun variabelen
        second_number += 1
        print second_number
        # oppdaterer originale tallet i den andre skjermen
        self.manager.get_screen("second_screen").second_number = second_number
        # Legg det til i labelen
        self.ids.increment_test_label.text = str(second_number)



class EksempelRoot(BoxLayout):
    #hovedtall = NumericProperty(0)
    #hovedstring = StringProperty("")

    def __init__(self, **kwargs):
        super(EksempelRoot, self).__init__(**kwargs)
        self.hovedtall = NumericProperty(0)
        self.hovedstring = StringProperty("")


class EksempelApp(App):
    pass
    #def build(self):
        #return EksempelRoot()


if __name__ == "__main__":
    EksempelApp().run()
