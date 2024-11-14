from kivymd.app import MDApp
from kivymd.uix.transition import MDSlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText,MDSnackbarButtonContainer,MDSnackbarCloseButton
from kivy.lang import Builder
from kivy.clock import mainthread
import threading as th
from kivy_app.utils.API import api

class Inicio(MDBoxLayout):
    def iniciar_sesion(self,usuario,contraseña):
        self.ids.contenedor_carga_iniciar_sesion.opacity = 1
        self.ids.contenedor_carga_iniciar_sesion.disabled = True
        app.contenedor.show_snackbar("INICIANDO SESION")
        th.Thread(target=self.iniciar,args=[usuario,contraseña]).start()
    
    def iniciar(self,usuario,contraseña):
        if api.login(usuario,contraseña):
            app.cambiar_inicio()
        else:
            app.contenedor.show_snackbar("ERROR AL INICIAR SESION")
            self.quitar_carga()
    
    @mainthread
    def quitar_carga(self):
        self.ids.contenedor_carga_iniciar_sesion.opacity = 0
        self.ids.contenedor_carga_iniciar_sesion.disabled = False
    
        
class Contenedor(MDBoxLayout):
    snackbar = None
    def carga_principal(self):
        self.ids.screen_mesas.mostrar_carga()
        self.ids.screen_platos.mostrar_carga()
        self.ids.screen_orden.mostrar_carga()
        th.Thread(target=self.conectar).start()
    
    def conectar(self):
        try:
            data = api.get_initial_android()
            self.ids.screen_orden.mostrar(data["section_divisas"])
            self.ids.screen_mesas.mostrar(data["section_mesas"])
            self.ids.screen_platos.mostrar(data["section_platos"])
        except Exception as e:
            print(e)
            for x in ["screen_orden","screen_mesas","screen_platos"]:
                self.ids[x].mostrar()
            import time
            time.sleep(1)
            self.show_snackbar("ERROR DE\nCARGA INICIAL")
    
    @mainthread
    def show_snackbar(self,text):
        if self.snackbar:
            self.snackbar.dismiss()
        close_button = MDSnackbarCloseButton(
                        icon="close",
                    )
        
        self.snackbar = MDSnackbar(
            MDSnackbarText(
                text=text,
                pos_hint= {'center_x': 0.5},
                halign="center"
            ),
            MDSnackbarButtonContainer(
                close_button,
                pos_hint={"center_y": 0.5}
            ),
            y="90dp",
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        )
        self.snackbar.open()
        close_button.on_press = self.snackbar.dismiss

class RestaurantApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.contenedor_zero = MDBoxLayout()
        
        self.contenedor = Contenedor()
        self.inicio = Inicio()
        self.inicio.ids.screen_ajustes.cargar_host()
        self.inicio.ids.screen_ajustes.contenedor = self.contenedor
        self.inicio.ids.screen_manager_start.transition=MDSlideTransition(direction="up")
        
        if not api.detectar_token():
            self.inicio.ids.button_cerrar_sesion.disabled = True
        
        self.contenedor_zero.add_widget(self.inicio)
        return self.contenedor_zero

    @mainthread
    def cambiar_inicio(self):
        if not api.detectar_token():
            self.inicio.ids.screen_manager_start.current = "INICIAR_SESION"
            return
        self.contenedor.ids.screen_manager.transition=MDSlideTransition(direction="up")
        self.contenedor_zero.clear_widgets()
        self.contenedor_zero.add_widget(self.contenedor)
        self.contenedor.carga_principal()

    def borrar_token(self):
        api.borrar_token()
        self.inicio.ids.button_cerrar_sesion.disabled = True
        
    
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
    Builder.load_file('kivy_app/kv/screenIniciarSesion.kv')
    Builder.load_file('kivy_app/kv/restaurant.kv')
    app = RestaurantApp()
    app.run()