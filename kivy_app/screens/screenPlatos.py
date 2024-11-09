from kivymd.uix.menu import MDDropdownMenu
from kivy_app.screens.screen import ScreenPadre
from ..utils.API import api
from kivy_app.widgets.clasesMD import PlatoSeleccionarMDListItem
from kivy.clock import mainthread


class ScreenPlatos(ScreenPadre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drop_menu=MDDropdownMenu(position="bottom")
        self.menu_items = None
        
    def abir_menu_tipos_platos(self):
        if not self.menu_items:
            return
        if self.menu_items!=self.drop_menu.items:
            self.drop_menu.items=self.menu_items
        if self.drop_menu.caller != self.ids.boton_menu_tipos_platos:
            self.drop_menu.caller= self.ids.boton_menu_tipos_platos
        self.drop_menu.open()
    
    def mostrar_carga(self):
        self.contenedor = self.ids.lista_platos
        super().mostrar_carga()
    
    def datos_modo_false(self):
        self.platos = False
        self.menu_items = False
        
    def solicitar(self):
        try:
            self.platos = api.get_platos()
            self.preparar_datos(api.get_tipos_platos())
        except Exception as e:
            print(e)
        self.mostrar()
    
    def preparar_datos(self,tipos_platos):
        self.menu_items = [(
                                {
                                    "text":item["nombre"],
                                    "leading_icon":item["icon"],
                                    "on_release":lambda x=item:self.filtrar(x)
                                }) for item in tipos_platos]
        self.menu_items.insert(0,{"text":"TODO","leading_icon":"food","on_release":self.filtrar})
    
    @mainthread
    def mostrar(self,datos=None):
        if datos:
            self.platos = datos["platos_tipos"]
            self.preparar_datos(datos["tipos_platos"])
        
        super().mostrar(self.platos)
        if not self.platos:
            return
        for plato in self.platos:
            self.contenedor.add_widget(PlatoSeleccionarMDListItem(
                                        id=plato["id"],
                                        nombre=plato["nombre"],
                                        descripcion=plato["descripcion"],
                                        precio=plato["precio"],
                                        tipo_id=plato["tipo_id"],
                                        icon=plato["icon"]))
        
    def filtrar(self,item=None):
        if item==None:
            self.ids.chip_text_filtrado.text="TODO"
            self.drop_menu.dismiss()
            self.mostrar()
            return
        self.ids.chip_text_filtrado.text=item["nombre"]
        self.drop_menu.dismiss()
        self.ids.lista_platos.clear_widgets()
        items_filtrados = tuple(filter(lambda x: x["tipo_id"]==item["id"],self.platos))
        for plato in items_filtrados:
            self.ids.lista_platos.add_widget(PlatoSeleccionarMDListItem(
                                        id=plato["id"],
                                        nombre=plato["nombre"],
                                        descripcion=plato["descripcion"],
                                        precio=plato["precio"],
                                        tipo_id=plato["tipo_id"],
                                        icon=plato["icon"]))