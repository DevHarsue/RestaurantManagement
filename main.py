from kivymd.app import MDApp
from kivymd.uix.transition import MDSlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
import threading as th
from kivy_app.utils.bd import BaseDatos

class Contenedor(MDBoxLayout):
    def carga_principal(self):
        self.ids.screen_mesas.mostrar_carga()
        self.ids.screen_platos.mostrar_carga()
        self.ids.screen_orden.mostrar_carga()
        th.Thread(target=self.conectar).start()
    
    def conectar(self):
        conexion = None
        try:
            bd = BaseDatos()
            conexion = bd.conectar()
            self.ids.screen_orden.solicitar(conexion)
            self.ids.screen_mesas.solicitar(conexion)
            self.ids.screen_platos.solicitar(conexion)
        except Exception as e:
            self.ids.screen_orden.tasas = None
            self.ids.screen_mesas.mesas = None
            self.ids.screen_platos.platos = None
            self.ids.screen_orden.mostrar()
            self.ids.screen_mesas.mostrar()
            self.ids.screen_platos.mostrar()
            print(e)
        finally:
            if conexion:
                bd.cerrar_conexion()

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
    Builder.load_file('kivy_app/kv/clasesMD.kv')
    Builder.load_file('kivy_app/kv/screenPlatos.kv')
    Builder.load_file('kivy_app/kv/screenFinOrden.kv')
    Builder.load_file('kivy_app/kv/screenOrden.kv')
    Builder.load_file('kivy_app/kv/screenMesas.kv')
    Builder.load_file('kivy_app/kv/restaurant.kv')
    RestaurantApp().run()