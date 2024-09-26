from kivy_app.screens.screens import ScreenPadre
from kivy_app.utils.bd import BaseDatos,TablaMesasOcupadas,TablaDetallesOrdenesPlatos,TablaOrdenes
from kivy.clock import mainthread
import threading as th


class ScreenFinOrden(ScreenPadre):
    contenido = None
    tabla_ordenes = TablaOrdenes()
    tabla_mesas_ocupadas = TablaMesasOcupadas()
    tabla_detalles_ordenes = TablaDetallesOrdenesPlatos()
    def iniciar(self,mesa_id,mesa_libre,lista_platos,totales,orden_id,bolivar,cop):
        if self.contenido == None:
            self.contenido = self.ids.contenedor_fin_orden
        
        self.mesa_id  = mesa_id
        self.mesa_libre = mesa_libre
        self.lista_platos = lista_platos
        self.totales = totales
        self.orden_id = orden_id
        self.bolivar = bolivar
        self.cop = cop
        self.clear_widgets()
        self.add_widget(self.crear_progress_circular())
        if mesa_libre:
            th.Thread(target=self.insertar).start()
        else:
            th.Thread(target=self.agregar).start()
            
    
    def insertar(self):
        conexion = None
        try:
            bd = BaseDatos()
            conexion = bd.conectar()
            registro_orden = self.tabla_ordenes.insert(conexion)
            orden_id = registro_orden[0][0]
            self.tabla_detalles_ordenes.insert(conexion,orden_id,self.lista_platos)
            self.tabla_mesas_ocupadas.insert(conexion,self.mesa_id,orden_id)
        except Exception as e:
            print(e)
        finally:
            if conexion:
                bd.cerrar_conexion()
        
        self.mostrar_final()
        self.colocar_totales()

    def agregar(self):
        conexion = None
        try:
            bd = BaseDatos()
            conexion = bd.conectar()
            platos_existentes = self.tabla_detalles_ordenes.select_platos_orden_id(conexion,self.orden_id)
            platos_existentes = [x[0] for x in platos_existentes]
            lista =[x for x in self.lista_platos]
            
            for plato in lista:
                if plato[0] in platos_existentes:
                    self.tabla_detalles_ordenes.update(conexion,self.orden_id,plato[0],plato[1])
                    self.lista_platos.remove(plato)
                    
            if bool(self.lista_platos):
                self.tabla_detalles_ordenes.insert(conexion,self.orden_id,self.lista_platos)
            total = self.tabla_detalles_ordenes.select_calcular_total(conexion,self.orden_id)[0]
        except Exception as e:
            print(e)
        finally:
            if conexion:
                bd.cerrar_conexion()
        self.mostrar_final()
        self.colocar_totales(total)
    
    @mainthread
    def mostrar_final(self):
        self.clear_widgets()
        self.add_widget(self.contenido)
    @mainthread
    def colocar_totales(self,total=None):
        if total:
            self.ids.label_dolar.text = f"Total Dolar: {total}"
            self.ids.label_bs.text = f"Total BS: {total*self.bolivar}"
            self.ids.label_cop.text = f"Total COP: {total*self.cop}"
        else:
            self.ids.label_dolar.text = self.totales["dolar"]
            self.ids.label_bs.text = self.totales["bs"]
            self.ids.label_cop.text = self.totales["cop"]
            