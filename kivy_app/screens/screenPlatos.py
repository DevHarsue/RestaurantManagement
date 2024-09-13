from kivymd.uix.menu import MDDropdownMenu
from kivy_app.screens.screens import ScreenPadrePlatosOrden
from kivy_app.utils.bd import TablaPlatos,TablaTiposPlatos,BaseDatos
from kivy_app.widgets.clasesMD import PlatoSeleccionarMDListItem

class ScreenPlatos(ScreenPadrePlatosOrden):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drop_menu=MDDropdownMenu(position="bottom")
        self.tabla_platos = TablaPlatos()
        self.tabla_tipos_platos = TablaTiposPlatos()
        self.menu_items = None
        
    def abir_menu_tipos_platos(self):
        if not self.menu_items:
            return
        if self.menu_items!=self.drop_menu.items:
            self.drop_menu.items=self.menu_items
        if self.drop_menu.caller != self.ids.boton_menu_tipos_platos:
            self.drop_menu.caller= self.ids.boton_menu_tipos_platos
        self.drop_menu.open()
    
    def cargar(self):
        self.contenedor = self.ids.lista_platos
        super().cargar()
    
    def datos_modo_false(self):
        self.platos = False
        self.menu_items = False
        
    def solicitar(self):
        bd = BaseDatos()
        try:
            conexion = bd.conectar()
            self.platos = self.tabla_platos.select_vista(conexion)
            self.menu_items = [({"text":item[1],"leading_icon":item[2],"on_release":lambda x=item:self.filtrar(x)}) for item in self.tabla_tipos_platos.select(conexion)]
            self.menu_items.insert(0,{"text":"TODO","leading_icon":"food","on_release":self.filtrar})
        except Exception as e:
            print(e)
            conexion = None
            self.platos = None
            self.menu_items = None
        finally:
            if conexion:
                bd.cerrar_conexion()
    
    def mostrar(self,*_):
        super().mostrar(self.platos)
        if not self.platos:
            return
        for plato in self.platos:
            self.contenedor.add_widget(PlatoSeleccionarMDListItem(id=plato[0],nombre=plato[1],descripcion=plato[2],precio=plato[3],tipo_id=plato[4],icon=plato[5]))
            
    def filtrar(self,item=None):
        if item==None:
            self.ids.chip_text_filtrado.text="TODO"
            self.mostrar()
            return
        self.ids.chip_text_filtrado.text=item[1]
        self.drop_menu.dismiss()
        self.ids.lista_platos.clear_widgets()
        items_filtrados = tuple(filter(lambda x: x[4]==item[0],self.platos))
        for plato in items_filtrados:
            self.ids.lista_platos.add_widget(PlatoSeleccionarMDListItem(id=plato[0],nombre=plato[1],descripcion=plato[2],precio=plato[3],tipo_id=plato[4],icon=plato[5]))
        