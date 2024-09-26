from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty,NumericProperty,BooleanProperty

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
    id = NumericProperty()
    text = StringProperty()
    libre = BooleanProperty()
    orden_id = NumericProperty()
    
class CustomButton(MDButton):
    text = StringProperty()
    icon = StringProperty()
    def on_enter(self, *args):
        pass

class CustomTextField(MDTextField):
    pass
