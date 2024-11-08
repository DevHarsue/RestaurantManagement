from kivy_app.screens.screen import ScreenPadre
from ..utils.API import api
import threading as th

class ScreenAjustes(ScreenPadre):
    def cargar_host(self):
        self.ids.text_field_url.text = api.host
    
    def guardar_host(self):
        api.cambiar_host(self.ids.text_field_url.text)
        th.Thread(target=self.test).start()
        
    def test(self,show=False):
        if not api.test_host():
            self.show_snackbar("ERROR AL CONECTAR AL HOST")
            self.ids.icon_text_field_url.icon = "alert-circle-outline"
        else:
            self.show_snackbar("CONECTADO AL HOST CORRECTAMENTE")
            self.ids.icon_text_field_url.icon = "link"
            
