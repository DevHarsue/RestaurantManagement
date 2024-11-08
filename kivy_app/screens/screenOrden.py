from kivy_app.screens.screen import ScreenPadre
from ..utils.API import api
from kivymd.uix.dialog import MDDialog,MDDialogHeadlineText,MDDialogSupportingText,MDDialogButtonContainer,MDDialogContentContainer
from kivymd.uix.button import MDButton,MDButtonText
from kivy.uix.widget import Widget
from kivy_app.widgets.clasesMD import PlatosSeleccionadoMDListItem,CustomTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import mainthread
from kivy.core.window import Window

class ScreenOrden(ScreenPadre):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.crear_dialog_platos()
        self.bolivar = None
        self.cop = None
        self.mesa = None
        self.boton_si_dialog_pregunta.on_release = self.realizar_orden
    
    def mostrar_carga(self):
        self.contenedor = self.ids.contenedor_labels
        self.labels = self.contenedor.children[0] if isinstance(self.contenedor.children[0],MDBoxLayout) else self.labels
        super().mostrar_carga()
    
    def datos_modo_false(self):
        self.tasas = False
        
    def solicitar(self):
        try:
            self.tasas = api.get_divisas()
        except Exception as e:
            print(e)
        self.mostrar()
    
    @mainthread
    def mostrar(self,*_):
        super().mostrar(self.tasas)
        if not self.tasas:
            return
        self.contenedor.add_widget(self.labels)
        self.bolivar = self.tasas[0]["relacion"]
        self.cop = self.tasas[1]["relacion"]
        self.calcular()
            
        
    def calcular(self):
        if self.bolivar == None or self.cop == None:
            return
        total = 0
        for item in self.ids.lista_platillos.children:
            total += item.precio*item.cantidad
        self.ids.label_dolar.total = total
        self.ids.label_cop.total = round(total*self.cop)
        self.ids.label_bs.total = round(total*self.bolivar,2)
        
    def mostrar_dialog_orden(self):
        if not self.mesa :
            return
        if self.mesa.libre:    
            self.head_dialog_pregunta.text = "REALIZAR ORDEN"
            self.supporting_dialog_pregunta.text = f"¿Realizar orden para {self.mesa.text}?" 
        else:
            self.head_dialog_pregunta.text = "AGREGAR A LA ORDEN"
            self.supporting_dialog_pregunta.text = f"¿Agregar a la orden de {self.mesa.text}"
        self.dialog_pregunta.open()
    
    def realizar_orden(self):
        platos = self.ids.lista_platillos.children
        if len(platos) <=0:
            self.dialog_pregunta.dismiss()
            return
        totales = {
                    "dolar": self.ids.label_dolar.text,
                    "bs": self.ids.label_bs.text,
                    "cop": self.ids.label_cop.text
                }
        lista_platos = [{
                        "id":plato.id,
                        "tipo_id": plato.tipo_id,
                        "icon": plato.icon,
                        "nombre": plato.nombre,
                        "descripcion": plato.descripcion,
                        "precio": plato.precio,
                        "cantidad": plato.cantidad
                        } for plato in platos]
        Window.children[-1].children[0].ids.screen_fin_orden.iniciar(self.mesa.id,self.mesa.libre,lista_platos,totales,self.mesa.orden_id,self.bolivar,self.cop)
        self.parent.current = "FINORDEN"
        self.dialog_pregunta.dismiss()
        self.ids.lista_platillos.clear_widgets()
        self.deseleccionar_mesa()
    
    def deseleccionar_mesa(self):
        self.ids.label_mesa.text = "Seleccione una Mesa"
        self.mesa = None
        self.ids.boton_orden.text = "REALIZAR ORDEN"
    
    def agregar_plato(self):
        cantidad = int(self.text_field_dialog_platos.text)
        if cantidad<=0:
            return
        item_existente = tuple(filter(lambda x: x.id==self.item.id,self.ids.lista_platillos.children))
        if bool(item_existente):
            item_existente = item_existente[0]
            cantidad = int(item_existente.cantidad)+cantidad
            item_existente.cantidad = cantidad
            self.calcular()
        else:
            self.ids.lista_platillos.add_widget(PlatosSeleccionadoMDListItem(icon=self.item.icon,nombre=self.item.nombre,descripcion=self.item.descripcion,precio=self.item.precio,id=self.item.id,tipo_id=self.item.tipo_id,cantidad=cantidad))
        self.cambiar_screen("ORDEN")
        self.text_field_dialog_platos.text = "1"
        self.dialog_platos.dismiss()
    
    def borrar_plato(self):
        cantidad = int(self.text_field_dialog_platos.text)
        if self.item.cantidad > cantidad:
            cantidad = self.item.cantidad-cantidad
            self.item.cantidad = cantidad 
            self.calcular()
        else:
            self.ids.lista_platillos.remove_widget(self.item)
        self.dialog_platos.dismiss()
        self.text_field_dialog_platos.text = "1"
        
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
    
    def mostrar_dialog(self,accion,item):
        self.item = item
        condicion = accion=="agregar"
        self.head_dialog_platos.text = "Agregar Plato" if condicion else "Eliminar Plato"
        self.supporting_dialog_platos.text = f"¿Deseas agregar {self.item.nombre} a la orden?" if condicion else f"¿Deseas borrar {self.item.nombre} de la orden"
        self.boton_si_dialog_platos.on_release = self.agregar_plato if condicion else self.borrar_plato
        self.dialog_platos.open()