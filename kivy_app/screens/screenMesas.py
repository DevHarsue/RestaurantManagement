from kivy_app.screens.screen import ScreenPadre
from kivy_app.widgets.clasesMD import Mesa
from kivy.clock import mainthread
from kivy.core.window import Window
from ..utils.API import api

class ScreenMesas(ScreenPadre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_dialog_pregunta.text = "Seleccionar Mesa"
        self.boton_si_dialog_pregunta.on_release = self.seleccionar_mesa
        self.boton_opc_dialog_pregunta.on_release = self.consultar_orden
        
    
    @mainthread
    def mostrar_carga(self):
        self.ids.grid_mesas.clear_widgets()
        self.contenedor = self.ids.contenedor_carga
        self.contenedor.opacity = 1
        super().mostrar_carga()
        
    def datos_modo_false(self):
        self.mesas = False
        
    def solicitar(self):
        try:
            self.mesas = api.get_mesas()
            mesas_ocupadas = api.get_mesas_ocupadas()
            self.preparar_datos(mesas_ocupadas)

        except Exception as e:
            print(e)
        self.mostrar()
    
    def preparar_datos(self,mesas_ocupadas):
        for m in self.mesas:
            existe = tuple(filter(lambda x: x["id"]==m["id"],mesas_ocupadas))
            if bool(existe):
                existe = existe[0]
                m["libre"] = False
                m["orden_id"] = existe["orden_id"]
                continue
            m["libre"] = True
            m["orden_id"] = 0
    
    @mainthread
    def mostrar(self,datos=None):
        if datos:
            self.mesas = datos["mesas"]
            mesas_ocupadas = datos["mesas_ocupadas"]
            self.preparar_datos(mesas_ocupadas)
        
        super().mostrar(self.mesas)
        self.contenedor.opacity = 0
        if not self.mesas:
            self.contenedor.opacity = 1
            return
        for m in self.mesas:
            self.ids.grid_mesas.add_widget(Mesa(id=m["id"],text=m["descripcion"],libre=m["libre"],orden_id=m["orden_id"]))
            
    def mostrar_dialog_mesa(self,mesa):
        self.mesa = mesa
        self.supporting_dialog_pregunta.text = f"¿Usar {mesa.text}?" if mesa.libre else f"Agregar a {mesa.text}?" 
        if not mesa.libre and self.button_container_dialog_pregunta.children[-1] != self.boton_opc_dialog_pregunta:
                self.button_container_dialog_pregunta.add_widget(self.boton_opc_dialog_pregunta,index=3)
        elif mesa.libre and self.button_container_dialog_pregunta.children[-1] == self.boton_opc_dialog_pregunta:
            self.button_container_dialog_pregunta.remove_widget(self.boton_opc_dialog_pregunta)
            
        self.dialog_pregunta.open()

    def seleccionar_mesa(self):
        Window.children[-1].children[0].ids.screen_orden.ids.label_mesa.text = self.mesa.text
        Window.children[-1].children[0].ids.screen_orden.mesa = self.mesa
        if self.mesa.libre:
            Window.children[-1].children[0].ids.screen_orden.ids.boton_orden.text = "REALIZAR ORDEN"
        else:
            Window.children[-1].children[0].ids.screen_orden.ids.boton_orden.text = "AGREGAR A LA ORDEN"
            
        self.dialog_pregunta.dismiss()
        
        self.cambiar_screen("ORDEN")
    
    def consultar_orden(self):
        self.cambiar_screen("CONSULTA")
        Window.children[-1].children[0].ids.screen_consulta.consultar(self.mesa.orden_id)
        self.dialog_pregunta.dismiss()