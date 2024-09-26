from kivy_app.screens.screens import ScreenPadrePlatosOrden
from kivy_app.utils.bd import TablaDivisas,BaseDatos
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import mainthread
from kivy.core.window import Window

class ScreenOrden(ScreenPadrePlatosOrden):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.bolivar = None
        self.cop = None
        self.tabla_divisas = TablaDivisas()
        self.mesa = None
        self.boton_si_dialog_pregunta.on_release = self.realizar_orden
    
    def mostrar_carga(self):
        self.contenedor = self.ids.contenedor_labels
        self.labels = self.contenedor.children[0] if isinstance(self.contenedor.children[0],MDBoxLayout) else self.labels
        super().mostrar_carga()
    
    def datos_modo_false(self):
        self.tasas = False
        
    def solicitar(self,conexion = None):
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            self.tasas = self.tabla_divisas.select(conexion)
        except Exception as e:
            print(e)
            conexion = None
            self.tasas = None
        finally:
            if conexion:
                bd.cerrar_conexion()
        self.mostrar()
    
    @mainthread
    def mostrar(self,*_):
        super().mostrar(self.tasas)
        if not self.tasas:
            return
        self.contenedor.add_widget(self.labels)
        self.bolivar = self.tasas[1][-1]
        self.cop = self.tasas[2][-1]
            
        
    def calcular(self,list):
        if self.bolivar == None or self.cop == None:
            return
        total = 0
        for item in list.children:
            total += item.precio*item.cantidad
        self.ids.label_dolar.total = total
        self.ids.label_cop.total = total*self.cop
        self.ids.label_bs.total = total*self.bolivar
        
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
        lista_platos = []
        for plato in platos:
            lista_platos.append((plato.id,plato.cantidad))
        totales = {
                    "dolar": self.ids.label_dolar.text,
                    "bs": self.ids.label_bs.text,
                    "cop": self.ids.label_cop.text
                }
        Window.children[-1].ids.screen_fin_orden.iniciar(self.mesa.id,self.mesa.libre,lista_platos,totales,self.mesa.orden_id,self.bolivar,self.cop)
        self.parent.current = "FINORDEN"
        self.dialog_pregunta.dismiss()
        self.ids.lista_platillos.clear_widgets()
