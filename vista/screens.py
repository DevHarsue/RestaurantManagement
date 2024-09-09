from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog,MDDialogHeadlineText,MDDialogSupportingText,MDDialogButtonContainer,MDDialogContentContainer
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.menu import MDDropdownMenu
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
        for text in ["ORDEN","MESAS","CIERRE","AJUSTES"]:
            app.contenedor.ids.barra_navegacion.ids[f"boton_{text}"].active = False
        
        try:
            app.contenedor.ids.barra_navegacion.ids[f"boton_{current}"].active = True
        except:
            pass
        
    def crear_dialog_pregunta(self):
        self.boton_si = MDButton(MDButtonText(text="SI"),style="text")
        self.head_dialog_pregunta = MDDialogHeadlineText(text="")
        self.supporting_dialog_pregunta = MDDialogSupportingText(text="")
        self.text_field_dialog_pregunta= CustomTextField()
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.dialog_pregunta = MDDialog(self.head_dialog_pregunta,self.supporting_dialog_pregunta,
                            MDDialogContentContainer(self.text_field_dialog_pregunta),
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
        cantidad = int(self.text_field_dialog_pregunta.text)
        if self.item.cantidad > cantidad:
            cantidad = self.item.cantidad-cantidad
            print(self.item.nombre)
            self.item.cantidad = cantidad 
            app.contenedor.ids.screen_orden.ids.contenedor_labels.calcular(app.contenedor.ids.screen_orden.ids.lista_platillos)
        else:
            app.contenedor.ids.screen_orden.ids.lista_platillos.remove_widget(self.item)
        self.dialog_pregunta.dismiss()
        self.text_field_dialog_pregunta.text = "1"
    
    def agregar_plato(self,app):
        cantidad = int(self.text_field_dialog_pregunta.text)
        if cantidad<=0:
            return
        item_existente = tuple(filter(lambda x: x.id==self.item.id,app.contenedor.ids.screen_orden.ids.lista_platillos.children))
        if bool(item_existente):
            item_existente = item_existente[0]
            cantidad = int(item_existente.cantidad)+cantidad
            item_existente.cantidad = cantidad
            app.contenedor.ids.screen_orden.ids.contenedor_labels.calcular(app.contenedor.ids.screen_orden.ids.lista_platillos)
        else:
            app.contenedor.ids.screen_orden.ids.lista_platillos.add_widget(PlatosSeleccionadoMDListItem(icon=self.item.icon,nombre=self.item.nombre,descripcion=self.item.descripcion,precio=self.item.precio,id=self.item.id,tipo_id=self.item.tipo_id,cantidad=cantidad))
        self.cambiar_screen("ORDEN",app)
        self.text_field_dialog_pregunta.text = "1"
        self.dialog_pregunta.dismiss()
        
class ScreenPlatos(ScreenPadrePlatosOrden):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drop_menu=MDDropdownMenu(position="bottom")
        self.tabla_platos = TablaPlatos()
        self.tabla_tipos_platos = TablaTiposPlatos()
        self.menu_items = None
        
    def abir_menu_tipos_platos(self):
        if self.menu_items==None:
            return
        if self.menu_items!=self.drop_menu.items:
            self.drop_menu.items=self.menu_items
        if self.drop_menu.caller != self.ids.boton_menu_tipos_platos:
            self.drop_menu.caller= self.ids.boton_menu_tipos_platos
        self.drop_menu.open()

    def menu_callback(self, i):
        self.drop_menu.dismiss()
        
    def crear_progress_circular(self):
        circular_progress = MDCircularProgressIndicator(size_hint=(None, None),size=("50dp","50dp"),pos_hint={"center_x":0.5,"center_y":.5},determinate=True)
        circular_progress.on_determinate_complete= self.mostrar_platos
        progress = MDAnchorLayout(circular_progress)
        return progress
    
    def cargar_platos(self,conexion = None):
        for item in self.ids.lista_platos.children:
            if isinstance(item.children[0],MDCircularProgressIndicator):
                return
        self.platos = False
        self.menu_items = None
        self.ids.lista_platos.clear_widgets()
        self.ids.lista_platos.add_widget(self.crear_progress_circular())
        if not conexion:
            th.Thread(target=self.solicitar_platos_try).start()
        else:
            th.Thread(target=lambda x=conexion:self.solicitar_platos(conexion)).start()
    
    def solicitar_platos(self,conexion):
        conexion = False
        self.platos = self.tabla_mesas.select(conexion)
        
    
    def solicitar_platos_try(self):
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            # tablaMesas.definirse(conexion)
            self.platos = self.tabla_platos.select_vista(conexion)
            self.menu_items = [({"text":item[1],"leading_icon":item[2],"on_release":lambda x=item:self.filtrar(x)}) for item in self.tabla_tipos_platos.select(conexion)]
            self.menu_items.insert(0,{"text":"TODO","leading_icon":"food","on_release":self.filtrar})
        except Exception as e:
            print(e)
            conexion = None
            self.platos = None
        finally:
            if conexion:
                bd.cerrar_conexion()
    
    def mostrar_platos(self):
        self.ids.lista_platos.clear_widgets()
        if self.platos == False:
            self.ids.lista_platos.add_widget(self.crear_progress_circular())
        elif self.platos == None:
            self.ids.lista_platos.add_widget(MDAnchorLayout(MDLabel(text="Error de Conexión",size_hint=(1,1),halign="center",valign="center")))
        else:
            # Mostrar platos
            for plato in self.platos:
                self.ids.lista_platos.add_widget(PlatoSeleccionarMDListItem(id=plato[0],nombre=plato[1],descripcion=plato[2],precio=plato[3],tipo_id=plato[4],icon=plato[5]))
                
    def filtrar(self,item=None):
        if item==None:
            self.ids.chip_text_filtrado.text="TODO"
            self.mostrar_platos()
            return
        self.ids.chip_text_filtrado.text=item[1]
        self.drop_menu.dismiss()
        self.ids.lista_platos.clear_widgets()
        items_filtrados = tuple(filter(lambda x: x[4]==item[0],self.platos))
        for plato in items_filtrados:
            self.ids.lista_platos.add_widget(PlatoSeleccionarMDListItem(id=plato[0],nombre=plato[1],descripcion=plato[2],precio=plato[3],tipo_id=plato[4],icon=plato[5]))
            
        
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
        self.mesas = False
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
            self.mesas = None
        finally:
            if conexion:
                bd.cerrar_conexion()
    
    def mostrar_mesas(self):
        self.ids.grid_mesas.clear_widgets()
        if self.mesas == False:
            self.ids.grid_mesas.add_widget(self.crear_progress_circular())
        elif self.mesas == None:
            self.ids.grid_mesas.add_widget(MDAnchorLayout(MDLabel(text="Error de Conexión",size_hint=(1,1),halign="center",valign="center")))
        else:
            self.ids.grid_mesas.cols = 2
            for mesa in self.mesas:
                self.ids.grid_mesas.add_widget(Mesa(text=mesa[1]))