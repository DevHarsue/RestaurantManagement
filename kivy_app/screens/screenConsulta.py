from kivy_app.screens.screen import ScreenPadre
from kivy_app.utils.bd import TablaDetallesOrdenesPlatos,BaseDatos,TablaDivisas
from kivy_app.widgets.clasesMD import PlatosListaMDListItem
from kivy.clock import mainthread
import threading as th

class ScreenConsulta(ScreenPadre):
    def consultar(self,orden_id):
        self.orden_id = orden_id
        self.ids.contenedor_consulta.opacity = 0
        self.ids.contenedor_carga.opacity = 1
        self.ids.contenedor_carga.clear_widgets()
        self.ids.contenedor_carga.add_widget(self.crear_progress_circular())
        self.contenedor = self.ids.contenedor_carga
        th.Thread(target=self.solicitar).start()
    
    def solicitar(self):
        tabla = TablaDetallesOrdenesPlatos()
        tabla_divisas = TablaDivisas()
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            self.platos = tabla.select_platos_orden_id(conexion,self.orden_id)
            self.total = tabla.select_calcular_total(conexion,self.orden_id)[0]
            self.divisas = tabla_divisas.select(conexion)
        except Exception as e:
            print(e)
            conexion = None
            self.platos = None
            self.total = None
            self.divisas = None
        finally:
            if conexion:
                bd.cerrar_conexion()
        self.mostrar()
    
    @mainthread
    def mostrar(self):
        super().mostrar(self.platos)
        if self.platos:
            self.ids.contenedor_carga.opacity = 0
            self.ids.contenedor_carga.clear_widgets()
            self.ids.contenedor_consulta.opacity = 1
            self.ids.lista_platos_consulta.clear_widgets()
            for plato in self.platos:
                self.ids.lista_platos_consulta.add_widget(
                    PlatosListaMDListItem(
                        id = plato[0],
                        nombre = plato[1],
                        descripcion = plato[2],
                        precio = plato[3],
                        cantidad = plato[4],
                        tipo_id = plato[5],
                        icon = plato[6]
                    ))
            self.ids.label_dolar.total=self.total
            self.ids.label_bs.total=round(self.total*self.divisas[1][-1],2)
            self.ids.label_cop.total=round(self.total*self.divisas[2][-1])
                