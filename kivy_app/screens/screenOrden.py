from kivy_app.screens.screens import ScreenPadrePlatosOrden
from kivy_app.utils.bd import TablaDivisas,BaseDatos
from kivymd.uix.boxlayout import MDBoxLayout

class ScreenOrden(ScreenPadrePlatosOrden):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.bolivar = None
        self.cop = None
        self.tabla_divisas = TablaDivisas()
        
    def cargar(self):
        self.contenedor = self.ids.contenedor_labels
        self.labels = self.contenedor.children[0] if isinstance(self.contenedor.children[0],MDBoxLayout) else self.labels
        super().cargar()
    
    def datos_modo_false(self):
        self.tasas = False
        
    def solicitar(self):
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
