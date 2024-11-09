from kivy_app.screens.screen import ScreenPadre
from ..utils.API import api
import threading as th
from kivy.clock import mainthread
from kivy.core.window import Window

class ScreenAjustes(ScreenPadre):
    testeando = False
    contenedor = None
    def cargar_host(self):
        self.ids.text_field_url.text = api.host
    
    def guardar_host(self):
        if self.testeando:
            return
        self.testeando = True
        api.cambiar_host(self.ids.text_field_url.text)
        
        self.show_snackbar("PROBANDO CONEXIÓN")
        th.Thread(target=self.test).start()

    def test(self,show=False):
        result = api.test_host()
        if not result:
            self.show_snackbar("ERROR AL\nCONECTAR AL HOST")
            self.ids.icon_text_field_url.icon = "alert-circle-outline"
        else:
            self.show_snackbar("CONECTADO AL\nHOST CORRECTAMENTE")
            self.ids.icon_text_field_url.icon = "link"
            
        self.testeando = False
            
    @mainthread
    def show_snackbar(self, text):
        self.contenedor.show_snackbar(text)