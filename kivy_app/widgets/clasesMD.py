from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty,NumericProperty

class PlatoPadreMDListItem(MDListItem):
    id = NumericProperty()
    tipo_id = NumericProperty()
    icon = StringProperty()
    nombre = StringProperty()
    descripcion = StringProperty()
    precio = NumericProperty()

class PlatosSeleccionadoMDListItem(PlatoPadreMDListItem):
    cantidad = NumericProperty()

class PlatoSeleccionarMDListItem(PlatoPadreMDListItem):
    pass

class BaseMDNavigationItem(MDNavigationItem):
    text = StringProperty()
    icon = StringProperty()

class TotalMDLabel(MDLabel):
    total = NumericProperty()

class Mesa(MDCard):
    text = StringProperty()
    
class CustomButton(MDButton):
    def on_enter(self, *args):
        pass

class CustomTextField(MDTextField):
    pass
class Contenedor(MDBoxLayout):
    def carga_principal(self):
        self.ids.screen_mesas.cargar()
        self.ids.screen_platos.cargar()
        self.ids.screen_orden.cargar()