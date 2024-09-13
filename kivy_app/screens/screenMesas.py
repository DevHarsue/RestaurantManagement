from kivy_app.screens.screens import ScreenPadre
from kivy_app.utils.bd import TablaMesas,BaseDatos
from kivy_app.widgets.clasesMD import Mesa


class ScreenMesas(ScreenPadre):
    tabla_mesas = TablaMesas()
    def cargar(self):
        self.contenedor = self.ids.grid_mesas
        super().cargar()
    def datos_modo_false(self):
        self.mesas = False
    def solicitar(self):
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            self.mesas = self.tabla_mesas.select(conexion)
        except Exception as e:
            print(e)
            conexion = None
            self.mesas = None
        finally:
            if conexion:
                bd.cerrar_conexion()
    
    def mostrar(self,*_):
        super().mostrar(self.mesas)
        if not self.mesas:
            return
        self.contenedor.cols = 2
        for mesa in self.mesas:
            self.contenedor.add_widget(Mesa(text=mesa[1]))
