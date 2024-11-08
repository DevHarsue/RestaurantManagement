from kivymd.app import MDApp
from kivymd.uix.transition import MDSlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
import threading as th

class Inicio(MDBoxLayout):
    pass
class Contenedor(MDBoxLayout):
    def carga_principal(self):
        self.ids.screen_mesas.mostrar_carga()
        self.ids.screen_platos.mostrar_carga()
        self.ids.screen_orden.mostrar_carga()
        th.Thread(target=self.conectar).start()
    
    def conectar(self):
        try:
            self.ids.screen_orden.solicitar()
            self.ids.screen_mesas.solicitar()
            self.ids.screen_platos.solicitar()
        except Exception as e:
            print(e)
            self.ids.screen_orden.mostrar()
            self.ids.screen_mesas.mostrar()
            self.ids.screen_platos.mostrar()

class RestaurantApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.contenedor_zero = MDBoxLayout()
        self.contenedor = Contenedor()
        self.inicio = Inicio()
        self.inicio.ids.screen_ajustes.cargar_host()
        self.inicio.ids.screen_manager_start.transition=MDSlideTransition(direction="up")
        self.contenedor_zero.add_widget(self.inicio)
        return self.contenedor_zero

    def cambiar_inicio(self):
        self.contenedor.ids.screen_manager.transition=MDSlideTransition(direction="up")
        self.contenedor_zero.clear_widgets()
        self.contenedor_zero.add_widget(self.contenedor)
        self.contenedor.carga_principal()
        
    def cambiar_screen(self,bar, item,item_icon, item_text):
        self.contenedor.ids.screen_manager.current = item_text

if __name__=="__main__":
    Builder.load_file('kivy_app/kv/clasesMD.kv')
    Builder.load_file('kivy_app/kv/screenPlatos.kv')
    Builder.load_file('kivy_app/kv/screenFinOrden.kv')
    Builder.load_file('kivy_app/kv/screenConsulta.kv')
    Builder.load_file('kivy_app/kv/screenOrden.kv')
    Builder.load_file('kivy_app/kv/screenMesas.kv')
    Builder.load_file('kivy_app/kv/screenAjustes.kv')
    Builder.load_file('kivy_app/kv/restaurant.kv')
    RestaurantApp().run()