from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog,MDDialogHeadlineText,MDDialogSupportingText,MDDialogButtonContainer,MDDialogContentContainer
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivy_app.widgets.clasesMD import CustomTextField,PlatosSeleccionadoMDListItem
import threading as th

class ScreenPadre(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crear_dialog_pregunta()
    contenedor = None
    def crear_progress_circular(self):
        circular_progress = MDCircularProgressIndicator(size_hint=(None, None),size=("50dp","50dp"),pos_hint={"center_x":0.5,"center_y":.5})
        progress = MDAnchorLayout(circular_progress)
        return progress
    
    def cargar(self):
        for item in self.contenedor.children:
            if isinstance(item.children[0],MDCircularProgressIndicator):
                return
        self.mostrar_carga()
        th.Thread(target=self.solicitar).start()
    
    def mostrar_carga(self):
        self.datos_modo_false()
        self.contenedor.clear_widgets()
        self.contenedor.add_widget(self.crear_progress_circular())
    
    def datos_modo_false(self):
        pass
    
    def solicitar(self,conexion = None):
        pass
    
    def mostrar(self,var):
        self.contenedor.clear_widgets()
        if var == None:
            self.contenedor.add_widget(MDAnchorLayout(MDLabel(text="Error de Conexión",size_hint=(1,1),halign="center",valign="center")))
    
    def crear_dialog_pregunta(self):
        self.boton_si_dialog_pregunta = MDButton(MDButtonText(text="SI"),style="text")
        self.head_dialog_pregunta = MDDialogHeadlineText(text="")
        self.supporting_dialog_pregunta = MDDialogSupportingText(text="")
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.dialog_pregunta = MDDialog(self.head_dialog_pregunta,self.supporting_dialog_pregunta,
                        MDDialogButtonContainer(Widget(),boton_no,self.boton_si_dialog_pregunta))
        boton_no.on_release = self.dialog_pregunta.dismiss

class ScreenPadrePlatosOrden(ScreenPadre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crear_dialog_platos()
        
    def cambiar_screen(self,current,app):
        self.parent.current = current
        for text in ["ORDEN","MESAS","AJUSTES"]:
            app.contenedor.ids.barra_navegacion.ids[f"boton_{text}"].active = False
        
        try:
            app.contenedor.ids.barra_navegacion.ids[f"boton_{current}"].active = True
        except:
            pass
        
    def crear_dialog_platos(self):
        self.boton_si_dialog_platos = MDButton(MDButtonText(text="SI"),style="text")
        self.head_dialog_platos = MDDialogHeadlineText(text="")
        self.supporting_dialog_platos = MDDialogSupportingText(text="")
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.text_field_dialog_platos= CustomTextField()
        self.dialog_platos = MDDialog(self.head_dialog_platos,self.supporting_dialog_platos,
                        MDDialogContentContainer(self.text_field_dialog_platos),
                        MDDialogButtonContainer(Widget(),boton_no,self.boton_si_dialog_platos))
        boton_no.on_release = self.dialog_platos.dismiss
        self.boton_si_dialog_platos.on_release = self.agregar_plato
    
    def mostrar_dialog(self,accion,item,app):
        self.item = item
        condicion = accion=="agregar"
        self.head_dialog_platos.text = "Agregar Plato" if condicion else "Eliminar Plato"
        self.supporting_dialog_platos.text = f"¿Deseas agregar {self.item.nombre} a la orden?" if condicion else f"¿Deseas borrar {self.item.nombre} de la orden"
        self.boton_si_dialog_platos.on_release = (lambda app=app: self.agregar_plato(app)) if condicion else (lambda app=app: self.borrar_plato(app))
        self.dialog_platos.open()
    
    def borrar_plato(self,app):
        cantidad = int(self.text_field_dialog_platos.text)
        if self.item.cantidad > cantidad:
            cantidad = self.item.cantidad-cantidad
            self.item.cantidad = cantidad 
            app.contenedor.ids.screen_orden.calcular(app.contenedor.ids.screen_orden.ids.lista_platillos)
        else:
            app.contenedor.ids.screen_orden.ids.lista_platillos.remove_widget(self.item)
        self.dialog_platos.dismiss()
        self.text_field_dialog_platos.text = "1"
    
    def agregar_plato(self,app):
        cantidad = int(self.text_field_dialog_platos.text)
        if cantidad<=0:
            return
        item_existente = tuple(filter(lambda x: x.id==self.item.id,app.contenedor.ids.screen_orden.ids.lista_platillos.children))
        if bool(item_existente):
            item_existente = item_existente[0]
            cantidad = int(item_existente.cantidad)+cantidad
            item_existente.cantidad = cantidad
            app.contenedor.ids.screen_orden.calcular(app.contenedor.ids.screen_orden.ids.lista_platillos)
        else:
            app.contenedor.ids.screen_orden.ids.lista_platillos.add_widget(PlatosSeleccionadoMDListItem(icon=self.item.icon,nombre=self.item.nombre,descripcion=self.item.descripcion,precio=self.item.precio,id=self.item.id,tipo_id=self.item.tipo_id,cantidad=cantidad))
        self.cambiar_screen("ORDEN",app)
        self.text_field_dialog_platos.text = "1"
        self.dialog_platos.dismiss()
        
