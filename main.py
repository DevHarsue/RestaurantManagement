from kivymd.app import MDApp
from kivymd.uix.transition import MDSlideTransition
from vista.screens import *
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

class RestaurantApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.contenedor = Contenedor()
        self.contenedor.ids.screen_manager.transition=MDSlideTransition(direction="up")
        #Carga Principal de la base de datos
        self.contenedor.carga_principal()
        # self.contenedor.ids.screen_mesas.cargar_mesas()
        
        
        return self.contenedor
    
    def cambiar_screen(self,bar, item,item_icon, item_text):
        self.root.ids.screen_manager.current = item_text
    
    def abir_menu_tipos_platos(self):
        menu_items = [
            {
                "leading_icon": "food",
                "text": f"Item {i}",
                "on_release": lambda x=i:self.menu_callback(i),
            } for i in range(5)
        ]
        self.drop_menu=MDDropdownMenu(
            caller=self.contenedor.ids.boton_menu_tipos_platos, items=menu_items
        )
        self.drop_menu.open()

    def menu_callback(self, i):
        self.drop_menu.dismiss()
        
if __name__=="__main__":
    Builder.load_file('vista/clasesMD.kv')
    Builder.load_file('vista/screenPlatosOrden.kv')
    Builder.load_file('vista/screenMesas.kv')
    RestaurantApp().run()