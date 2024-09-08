from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog,MDDialogHeadlineText,MDDialogSupportingText,MDDialogButtonContainer
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.anchorlayout import MDAnchorLayout
from vista.clasesMD import *
import threading as th
from bd.bd import *

class ScreenPadrePlatosOrden(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crear_dialog_pregunta()
        
    def cambiar_screen(self,current,app):
        self.parent.current = current
        boton = app.contenedor.ids.barra_navegacion.ids.boton_orden_bar
        boton.active = False if boton.active else True
        
    def crear_dialog_pregunta(self):
        self.boton_si = MDButton(MDButtonText(text="SI"),style="text")
        self.head_dialog_pregunta = MDDialogHeadlineText(text="")
        self.supporting_dialog_pregunta = MDDialogSupportingText(text="")
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.dialog_pregunta = MDDialog(self.head_dialog_pregunta,self.supporting_dialog_pregunta,
                            MDDialogButtonContainer(Widget(),boton_no,self.boton_si))
        self.boton_si.on_release = self.agregar_plato
        boton_no.on_release = self.dialog_pregunta.dismiss
    
    def mostrar_dialog(self,accion,item,app):
        self.item = item
        condicion = accion=="agregar"
        self.head_dialog_pregunta.text = "Agregar Plato" if condicion else "Eliminar Plato"
        self.supporting_dialog_pregunta.text = f"¿Deseas agregar {self.item.nombre} a la orden?" if condicion else f"¿Deseas borrar {self.item.nombre} de la orden"
        self.boton_si.on_release = (lambda app=app: self.agregar_plato(app)) if condicion else (lambda app=app: self.borrar_plato(app))
        self.dialog_pregunta.open()
    
    def borrar_plato(self,app):
        app.contenedor.ids.screen_orden.ids.lista_platillos.remove_widget(self.item)
        self.dialog_pregunta.dismiss()
    
    def agregar_plato(self,app):
        app.contenedor.ids.screen_orden.ids.lista_platillos.add_widget(PlatosSeleccionadoMDListItem(icon=self.item.icon,nombre=self.item.nombre,descripcion=self.item.descripcion,precio=self.item.precio))
        self.cambiar_screen("ORDEN",app)
        self.dialog_pregunta.dismiss()
        
class ScreenPlatos(ScreenPadrePlatosOrden):
    tabla_platos = TablaPlatos()
    tabla_tipos_platos = TablaTiposPlatos()
    def cargar_platos(self,conexion):
        pass
        
class ScreenOrden(ScreenPadrePlatosOrden):
    pass

class ScreenMesas(MDScreen):
    tabla_mesas = TablaMesas()
    def crear_progress_circular(self):
        circular_progress = MDCircularProgressIndicator(size_hint=(None, None),size=("50dp","50dp"),pos_hint={"center_x":0.5,"center_y":.5},determinate=True)
        circular_progress.on_determinate_complete= self.mostrar_mesas
        progress = MDAnchorLayout(circular_progress)
        return progress
    
    def cargar_mesas(self,conexion = None):
        for item in self.ids.grid_mesas.children:
            if isinstance(item.children[0],MDCircularProgressIndicator):
                return
        self.mesas = None
        self.ids.grid_mesas.clear_widgets()
        self.ids.grid_mesas.cols=1
        self.ids.grid_mesas.add_widget(self.crear_progress_circular())
        if not conexion:
            th.Thread(target=self.solicitar_mesas_try).start()
        else:
            th.Thread(target=lambda x=conexion:self.solicitar_mesas(conexion)).start()
    
    def solicitar_mesas(self,conexion):
        self.mesas = self.tabla_mesas.select(conexion)
        
    
    def solicitar_mesas_try(self):
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            # tablaMesas.definirse(conexion)
            self.mesas = self.tabla_mesas.select(conexion)
        except Exception as e:
            print(e)
            conexion = None
        finally:
            if conexion:
                bd.cerrar_conexion()
    
    def mostrar_mesas(self):
        self.ids.grid_mesas.clear_widgets()
        if self.mesas == None:
            self.ids.grid_mesas.add_widget(MDAnchorLayout(MDLabel(text="Error de Conexión",size_hint=(1,1),halign="center",valign="center")))
        else:
            self.ids.grid_mesas.cols = 2
            for mesa in self.mesas:
                self.ids.grid_mesas.add_widget(Mesa(text=mesa[1]))