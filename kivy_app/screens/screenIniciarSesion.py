from kivy_app.screens.screen import ScreenPadre
from kivy.core.window import Window

class ScreenIniciarSesion(ScreenPadre):
    def iniciar_sesion(self):
        usuario = self.ids.username.text
        contraseña = self.ids.password.text
        Window.children[0].children[0].ids.screen_manager_start.current = "INICIO"
        Window.children[0].children[0].iniciar_sesion(usuario,contraseña)