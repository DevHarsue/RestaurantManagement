from kivy_app.screens.screen import ScreenPadre
from ..utils.API import api
# from kivy_app.widgets.clasesMD import PlatosListaMDListItem
# from kivy.clock import mainthread
# import threading as th

class ScreenAjustes(ScreenPadre):
    def cargar_host(self):
        self.ids.text_field_url.text = api.host
    def guardar_host(self):
        api.cambiar_host(self.ids.text_field_url.text)