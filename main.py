from kivymd.app import MDApp
from kivymd.uix.transition import MDSlideTransition
from vista.screens import *
from kivy.lang import Builder

class RestaurantApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.contenedor = Contenedor()
        self.contenedor.ids.screen_manager.transition=MDSlideTransition(direction="up")
        #Carga Principal de la base de datos
        self.contenedor.carga_principal()
        return self.contenedor

    def cambiar_screen(self,bar, item,item_icon, item_text):
        self.root.ids.screen_manager.current = item_text

if __name__=="__main__":
    Builder.load_file('vista/clasesMD.kv')
    Builder.load_file('vista/screenPlatosOrden.kv')
    Builder.load_file('vista/screenMesas.kv')
    RestaurantApp().run()