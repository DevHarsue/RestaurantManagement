from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.textfield import MDTextField
from bd.bd import BaseDatos
import threading as th
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

class ContenedorLabels(MDGridLayout):
    def calcular(self,list):
        total = 0
        for item in list.children:
            total += item.precio*item.cantidad
        labels = tuple(filter(lambda item: isinstance(item,TotalMDLabel),self.children))
        labels[0].total = total*36
        labels[1].total = total*3700
        labels[2].total = total

class Contenedor(MDBoxLayout):
    bd = BaseDatos()
    conexion = None
    def carga_principal(self):
        try:
            th.Thread(target=self.conectar).start()
            self.ids.screen_mesas.cargar_mesas(self.conexion)
            self.ids.screen_platos.cargar_platos(self.conexion)
        except Exception as e:
            print(e)
            self.conexion = None
        finally:
            if self.conexion:
                self.bd.cerrar_conexion()
    
    def conectar(self):
        try:
            self.conexion = self.bd.conectar()
        except Exception as e:
            print(e)
            self.conexion = None
            self.ids.screen_mesas.mesas = None
            self.ids.screen_platos.platos = None