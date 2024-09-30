from kivy_app.screens.screen import ScreenPadre
from kivy_app.utils.bd import BaseDatos,TablaMesasOcupadas,TablaDetallesOrdenesPlatos,TablaOrdenes
from kivy_app.widgets.clasesMD import BoxReintentar,PlatosListaMDListItem
from kivy.clock import mainthread
from kivy.core.window import Window
import threading as th


class ScreenFinOrden(ScreenPadre):
    tabla_ordenes = TablaOrdenes()
    tabla_mesas_ocupadas = TablaMesasOcupadas()
    tabla_detalles_ordenes = TablaDetallesOrdenesPlatos()
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
            th.Thread(target=self.insertar).start()
        else:
            th.Thread(target=self.actualizar).start()
            
    
    def insertar(self):
        conexion = None
        try:
            bd = BaseDatos()
            conexion = bd.conectar()
            registro_orden = self.tabla_ordenes.insert(conexion)
            orden_id = registro_orden[0][0]
            lista_platos = [(plato["id"],plato["cantidad"]) for plato in self.lista_platos]
            self.tabla_detalles_ordenes.insert(conexion,orden_id,lista_platos)
            self.tabla_mesas_ocupadas.insert(conexion,self.mesa_id,orden_id)
        except Exception as e:
            print(e)
            conexion = None
            self.mostrar_error()
            return
        finally:
            if conexion:
                bd.cerrar_conexion()
        
        self.mostrar_final()
        self.add_items_lista_agregado()
        self.colocar_totales()
        Window.children[-1].ids.screen_mesas.cargar()

        
    def actualizar(self):
        conexion = None
        try:
            bd = BaseDatos()
            conexion = bd.conectar()
            platos_existentes = self.tabla_detalles_ordenes.select_platos_orden_id(conexion,self.orden_id)
            platos_existentes_ids = [x[0] for x in platos_existentes]
            lista =[x for x in self.lista_platos]
            for plato in self.lista_platos:
                if plato["id"] in platos_existentes_ids:
                    self.tabla_detalles_ordenes.update(conexion,self.orden_id,plato["id"],plato["cantidad"])
                    lista.remove(plato)
                    
            if bool(lista):
                lista = [(plato["id"],plato["cantidad"]) for plato in lista]
                self.tabla_detalles_ordenes.insert(conexion,self.orden_id,lista)
            total = self.tabla_detalles_ordenes.select_calcular_total(conexion,self.orden_id)[0]
        except Exception as e:
            print(e)
            self.mostrar_error()
            return
        finally:
            if conexion:
                bd.cerrar_conexion()
        self.mostrar_final()
        self.add_items_lista_existentes(platos_existentes)
        self.add_items_lista_agregado()
        self.colocar_totales(total)
    
    @mainthread
    def add_items_lista_agregado(self):
        for plato in self.lista_platos:
            self.ids.lista_platillos_agregados.add_widget(PlatosListaMDListItem(id=plato["id"],tipo_id=plato["tipo_id"],icon=plato["icon"],nombre=plato["nombre"],descripcion=plato["descripcion"],precio=plato["precio"],cantidad=plato["cantidad"]))
    
    @mainthread
    def add_items_lista_existentes(self,platos):
        for plato in platos:
            self.ids.lista_platillos_existentes.add_widget(PlatosListaMDListItem(id=plato[0],nombre=plato[1],descripcion=plato[2],precio=plato[3],cantidad=plato[4],tipo_id=plato[5],icon=plato[6]))
            
    @mainthread
    def mostrar_final(self):
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
        Window.children[-1].ids.screen_manager.current = "ORDEN"
    
    def calcular_totales(self,lista_remitente,lista):
        total = 0
        for plato in lista.children:
            total += plato.precio*plato.cantidad
        
        self.ids[f"label_dolar_{lista_remitente}"].total = total
        self.ids[f"label_bs_{lista_remitente}"].total = round(total*self.bolivar,2)
        self.ids[f"label_cop_{lista_remitente}"].total = round(total*self.cop)
        
