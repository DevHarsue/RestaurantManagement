from kivy_app.screens.screen import ScreenPadre
from kivy_app.utils.bd import TablaMesas,BaseDatos,TablaMesasOcupadas
from kivy_app.widgets.clasesMD import Mesa
from kivy.clock import mainthread
from kivy.core.window import Window

class ScreenMesas(ScreenPadre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_dialog_pregunta.text = "Seleccionar Mesa"
        self.boton_si_dialog_pregunta.on_release = self.seleccionar_mesa
        
    tabla_mesas = TablaMesas()
    tabla_mesas_ocupadas = TablaMesasOcupadas()
    
    @mainthread
    def mostrar_carga(self):
        self.contenedor = self.ids.grid_mesas
        super().mostrar_carga()
        
    def datos_modo_false(self):
        self.mesas = False
        
    def solicitar(self,conexion = None):
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            self.mesas = list(self.tabla_mesas.select(conexion))
            mesas_ocupadas = self.tabla_mesas_ocupadas.select(conexion)
            for i,mesa in enumerate(self.mesas):
                ocupada = tuple(filter(lambda x: mesa[0]==x[0],mesas_ocupadas))
                if ocupada:
                    ocupada = ocupada[0]
                    self.mesas[i] = (*mesa,False,ocupada[-1])
                else:
                    self.mesas[i] = (*mesa,True,0)
                
        except Exception as e:
            print(e)
            conexion = None
            self.mesas = None
        finally:
            if conexion:
                bd.cerrar_conexion()
        self.mostrar()
    
    @mainthread
    def mostrar(self,*_):
        super().mostrar(self.mesas)
        if not self.mesas:
            return
        self.contenedor.cols = 2
        for mesa in self.mesas:
            self.contenedor.add_widget(Mesa(id=mesa[0],text=mesa[1],libre=mesa[2],orden_id=mesa[3]))
            
    def mostrar_dialog_mesa(self,mesa):
        self.mesa = mesa
        self.supporting_dialog_pregunta.text = f"¿Usar {mesa.text}?" if mesa.libre else f"Agregar a {mesa.text}?" 
        if not mesa.libre and self.button_container_dialog_pregunta.children[-1] != self.boton_opc_dialog_pregunta:
                self.button_container_dialog_pregunta.add_widget(self.boton_opc_dialog_pregunta,index=3)
        elif mesa.libre and self.button_container_dialog_pregunta.children[-1] == self.boton_opc_dialog_pregunta:
            self.button_container_dialog_pregunta.remove_widget(self.boton_opc_dialog_pregunta)
            
        self.dialog_pregunta.open()

    def seleccionar_mesa(self):
        Window.children[-1].ids.screen_orden.ids.label_mesa.text = self.mesa.text
        Window.children[-1].ids.screen_orden.mesa = self.mesa
        if self.mesa.libre:
            Window.children[-1].ids.screen_orden.ids.boton_orden.text = "REALIZAR ORDEN"
        else:
            Window.children[-1].ids.screen_orden.ids.boton_orden.text = "AGREGAR A LA ORDEN"
            
        self.dialog_pregunta.dismiss()
        
        self.cambiar_screen("ORDEN")