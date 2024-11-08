from kivy_app.screens.screen import ScreenPadre
from kivy_app.widgets.clasesMD import BoxReintentar,PlatosListaMDListItem
from ..utils.API import api
from kivy.clock import mainthread
from kivy.core.window import Window
import threading as th


class ScreenFinOrden(ScreenPadre):
    def iniciar(self,mesa_id,mesa_libre,lista_platos,totales,orden_id,bolivar,cop):
        self.ids.lista_platillos_agregados.clear_widgets()
        self.ids.lista_platillos_existentes.clear_widgets()
        self.ids.contenedor_fin_orden.opacity = 0
        self.mesa_id = mesa_id
        self.mesa_libre = mesa_libre
        self.lista_platos = lista_platos
        self.totales = totales
        self.orden_id = orden_id
        self.bolivar = bolivar
        self.cop = cop
        self.ids.contenedor_carga.clear_widgets()
        self.ids.contenedor_carga.add_widget(self.crear_progress_circular())
        if mesa_libre:
            self.show_snackbar("Realizando Orden")
            th.Thread(target=self.insertar).start()
        else:
            self.show_snackbar("Agregando a la Orden")
            th.Thread(target=self.actualizar).start()
            
    
    def insertar(self):
        try:
            registro_orden = api.post_orden()
            orden_id = registro_orden["id"]
            lista_platos = [ {"plato_id":plato["id"],"cantidad":plato["cantidad"]} for plato in self.lista_platos]
            api.post_mesas_ocupadas(self.mesa_id,orden_id)
            api.post_detalles_ordenes_platos(orden_id,lista_platos)
        except Exception as e:
            print(e)
            self.mostrar_error()
            return
        
        self.mostrar_final()
        self.add_items_lista_agregado()
        self.colocar_totales()
        Window.children[-1].children[0].ids.screen_mesas.cargar()

        
    def actualizar(self):
        try:
            platos_existentes = api.get_platos_orden(self.orden_id)
            platos_existentes_ids = [x["plato_id"] for x in platos_existentes]
            lista =[x for x in self.lista_platos]
            for plato in self.lista_platos:
                if plato["id"] in platos_existentes_ids:
                    api.put_detalles_ordenes_platos(self.orden_id,plato["id"],plato["cantidad"])
                    lista.remove(plato)
                    
            if bool(lista):
                lista = [{"plato_id":plato["id"],"cantidad":plato["cantidad"]} for plato in lista]
                api.post_detalles_ordenes_platos(self.orden_id,lista)
                
            total = sum([p["precio"] * p["cantidad"] for p in api.get_platos_orden(self.orden_id)])
            
        except Exception as e:
            print(e)
            self.mostrar_error()
            return
        self.mostrar_final()
        self.add_items_lista_existentes(platos_existentes)
        self.add_items_lista_agregado()
        self.colocar_totales(total)
    
    @mainthread
    def add_items_lista_agregado(self):
        for plato in self.lista_platos:
            self.ids.lista_platillos_agregados.add_widget(PlatosListaMDListItem(
                                                            id=plato["id"],
                                                            tipo_id=plato["tipo_id"],
                                                            icon=plato["icon"],
                                                            nombre=plato["nombre"],
                                                            descripcion=plato["descripcion"],
                                                            precio=plato["precio"],
                                                            cantidad=plato["cantidad"]))
    
    @mainthread
    def add_items_lista_existentes(self,platos):
        for plato in platos:
            self.ids.lista_platillos_existentes.add_widget(PlatosListaMDListItem(
                                                            id=plato["plato_id"],
                                                            tipo_id=plato["tipo_id"],
                                                            icon=plato["icon"],
                                                            nombre=plato["nombre"],
                                                            descripcion=plato["descripcion"],
                                                            precio=plato["precio"],
                                                            cantidad=plato["cantidad"]))
            
    @mainthread
    def mostrar_final(self):
        self.snack_bar.dismiss()
        self.ids.contenedor_carga.clear_widgets()
        self.ids.contenedor_fin_orden.opacity = 1
        
    @mainthread
    def colocar_totales(self,total=None):
        if total:
            self.ids.label_dolar.text = f"Total Dolar: {total}"
            self.ids.label_bs.text = f"Total BS: {round(total*self.bolivar,2)}"
            self.ids.label_cop.text = f"Total COP: {round(total*self.cop)}"
        else:
            self.ids.label_dolar.text = self.totales["dolar"]
            self.ids.label_bs.text = self.totales["bs"]
            self.ids.label_cop.text = self.totales["cop"]
    
    @mainthread
    def mostrar_error(self):
        self.snack_bar.dismiss()
        self.show_snackbar("Error de Conexión")
        self.ids.contenedor_carga.clear_widgets()
        self.ids.contenedor_carga.add_widget(BoxReintentar())
    
    def reintentar(self):
        self.ids.contenedor_carga.clear_widgets()
        self.ids.contenedor_carga.add_widget(self.crear_progress_circular())
        if self.mesa_libre:
            th.Thread(target=self.insertar).start()
        else:
            th.Thread(target=self.actualizar).start()
    
    def finalizar(self):
        self.cambiar_screen("ORDEN")
    
    def calcular_totales(self,lista_remitente,lista):
        total = 0
        for plato in lista.children:
            total += plato.precio*plato.cantidad
        
        self.ids[f"label_dolar_{lista_remitente}"].total = total
        self.ids[f"label_bs_{lista_remitente}"].total = round(total*self.bolivar,2)
        self.ids[f"label_cop_{lista_remitente}"].total = round(total*self.cop)
        
