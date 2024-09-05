from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty,NumericProperty
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.transition import MDSlideTransition
from kivymd.uix.list import MDListItem
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivy.core.window import Window


class BaseMDNavigationItem(MDNavigationItem):
    text = StringProperty()
    icon = StringProperty()

class MesasMDListItem(MDListItem):
    text = StringProperty()
                
class PlatosSeleccionadoMDListItem(MDListItem):
    icon = StringProperty()
    nombre = StringProperty()
    descripcion = StringProperty()
    precio = NumericProperty()
    
    def on_release(self):
        boton_si = MDButton(MDButtonText(text="SI"),style="text")
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.dialog = MDDialog(MDDialogHeadlineText(text="Borrar Plato"),
                            MDDialogSupportingText(text=f'¿Quieres Borrar {self.nombre} de la orden?'),
                            MDDialogButtonContainer(Widget(),boton_no,boton_si))
        boton_si.on_release = self.eliminar
        boton_no.on_release = self.dialog.dismiss
        self.dialog.open()
    
    def eliminar(self):  
        self.parent.remove_widget(self)
        self.dialog.dismiss()

class PlatoMDListItem(PlatosSeleccionadoMDListItem):
    def on_release(self):
        boton_si = MDButton(MDButtonText(text="SI"),style="text")
        boton_no = MDButton(MDButtonText(text="NO"),style="text")
        self.dialog = MDDialog(MDDialogHeadlineText(text="Agregar Plato"),
                            MDDialogSupportingText(text=f'¿Quieres Agregar {self.nombre} a la orden?'),
                            MDDialogButtonContainer(Widget(),boton_no,boton_si))
        boton_si.on_release = self.agregar
        boton_no.on_release = self.dialog.dismiss
        self.dialog.open()
    
    def agregar(self):  
        Window.children[-1].ids.lista_platillos.add_widget(PlatosSeleccionadoMDListItem(icon=self.icon,nombre=self.nombre,descripcion=self.descripcion,precio=self.precio))
        self.dialog.dismiss()

class TotalMDLabel(MDLabel):
    total = NumericProperty()

class Contenedor(MDBoxLayout):
    pass

class RestaurantApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.contenedor = Contenedor()
        self.contenedor.ids.screen_manager.transition=MDSlideTransition(direction="up")
        for i in range(1,11):
            self.contenedor.ids.lista_mesas.add_widget(MesasMDListItem(text=f"MESA {i}"))
        return self.contenedor
    
    def cambiar_screen(self,bar, item,item_icon, item_text):
        self.root.ids.screen_manager.current = item_text
    
    def calcular(self):
        total = 0
        for item in self.contenedor.ids.lista_platillos.children:
            total += item.precio
        
        self.contenedor.ids.label_dolar.total = total
        self.contenedor.ids.label_cop.total = total*3700
        self.contenedor.ids.label_bs.total = total*36
    
    def elegir_plato(self):
        boton = MDButton(MDButtonText(text="Cerrar"),style="text")
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Selecciona un Plato",),
            MDDialogContentContainer(MDDivider(),
                                    PlatoMDListItem(icon="food-drumstick-outline",nombre="Pollo",descripcion="Pollo frito a la inglesa",precio=15.0),
                                    PlatoMDListItem(icon="food-steak",nombre="Carne",descripcion="Agua panela pues",precio=12.0),
                                    PlatoMDListItem(icon="cup-outline",nombre="Agua Panela",descripcion="Carne frita arrechisima",precio=1.0),
                                    MDDivider(),orientation="vertical"),
            MDDialogButtonContainer(Widget(),boton)
        )
        self.dialog.open()
        boton.on_release = self.dialog.dismiss
        
if __name__=="__main__":
    RestaurantApp().run()