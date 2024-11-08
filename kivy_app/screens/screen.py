from kivy.uix.widget import Widget
from kivy.clock import mainthread
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog,MDDialogHeadlineText,MDDialogSupportingText,MDDialogButtonContainer,MDDialogContentContainer
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText,MDSnackbarButtonContainer,MDSnackbarCloseButton
import threading as th


class ScreenPadre(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crear_dialog_pregunta()
        self.contenedor = None
        self.snack_bar = None
        
    def crear_progress_circular(self):
        circular_progress = MDCircularProgressIndicator(size_hint=(None, None),size=("50dp","50dp"),pos_hint={"center_x":0.5,"center_y":.5})
        progress = MDAnchorLayout(circular_progress)
        return progress
    
    @mainthread
    def cargar(self):
        for item in self.contenedor.children:
            if isinstance(item.children[0],MDCircularProgressIndicator):
                return
        self.mostrar_carga()
        self.show_snackbar("CARGANDO...")
        th.Thread(target=self.solicitar).start()
    
    def mostrar_carga(self):
        self.datos_modo_false()
        self.contenedor.clear_widgets()
        self.contenedor.add_widget(self.crear_progress_circular())
    
    def datos_modo_false(self):
        pass
    
    def solicitar(self):
        pass
    
    def mostrar(self,var):
        self.contenedor.clear_widgets()
        if self.snack_bar:
            self.snack_bar.dismiss()
        if not var:
            self.contenedor.add_widget(MDAnchorLayout(MDLabel(text="Error de Conexión",size_hint=(1,1),halign="center",valign="center")))
            self.show_snackbar("Error de Conexión")
            
    
    def crear_dialog_pregunta(self):
        self.head_dialog_pregunta = MDDialogHeadlineText(text="")
        self.supporting_dialog_pregunta = MDDialogSupportingText(text="")
        self.boton_si_dialog_pregunta = MDButton(MDButtonText(text="SI"),style="text")
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.boton_opc_dialog_pregunta = MDButton(MDButtonText(text="VER"),style="text")
        self.button_container_dialog_pregunta = MDDialogButtonContainer(Widget(),boton_no,self.boton_si_dialog_pregunta)
        self.dialog_pregunta = MDDialog(self.head_dialog_pregunta,self.supporting_dialog_pregunta,
                        self.button_container_dialog_pregunta)
        boton_no.on_release = self.dialog_pregunta.dismiss
    
    def cambiar_screen(self,current):
        Window.children[-1].children[0].ids.screen_manager.current = current
        for text in ["ORDEN","MESAS","PLATOS"]:
            Window.children[-1].children[0].ids.barra_navegacion.ids[f"boton_{text}"].active = False
        try:
            Window.children[-1].children[0].ids.barra_navegacion.ids[f"boton_{current}"].active = True
        except:
            pass
    @mainthread
    def show_snackbar(self,text):
        close_button = MDSnackbarCloseButton(
                        icon="close",
                    )
        
        self.snack_bar = MDSnackbar(
            MDSnackbarText(
                text=text,
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
        self.snack_bar.open()
        close_button.on_press = self.snack_bar.dismiss