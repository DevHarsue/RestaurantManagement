from kivy_app.screens.screen import ScreenPadre
from ..utils.API import api
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
        self.show_snackbar("CARGANDO...")
        th.Thread(target=self.solicitar).start()
    
    def solicitar(self):
        try:
            self.platos = api.get_platos_orden(self.orden_id)
            self.total = sum([ p["precio"] * p["cantidad"] for p in self.platos])
            self.divisas = api.get_divisas()
        except Exception as e:
            print(e)
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
                        id = plato["plato_id"],
                        nombre = plato["nombre"],
                        descripcion = plato["descripcion"],
                        precio = plato["precio"],
                        cantidad = plato["cantidad"],
                        tipo_id = plato["tipo_id"],
                        icon = plato["icon"]
                    ))
            self.ids.label_dolar.total=self.total
            self.ids.label_bs.total=round(self.total*self.divisas[0]["relacion"],2)
            self.ids.label_cop.total=round(self.total*self.divisas[1]["relacion"])
                