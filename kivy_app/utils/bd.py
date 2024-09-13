import pg8000

class BaseDatos:
    conexion = None
    def __init__(self) -> None:
        pass
    
    def conectar(self) -> pg8000.Connection:
        self.conexion = pg8000.connect(user="user_admin",host="dpg-crd7e5jqf0us73atkp9g-a.oregon-postgres.render.com",database="restaurantdb_qv75",port=5432,password="gVqTQMHsYU4HcdR8I9bG36X5pCrdculu")
        return self.conexion
    
    def cerrar_conexion(self):
        self.conexion.commit()
        self.conexion.close()

class Tabla:
    def __init__(self):
        self.nombre_tabla = ""
    
    def definirse(self,conexion: pg8000.Connection):
        cursor = conexion.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.nombre_tabla}';")
        self.columnas = tuple(i[0] for i in cursor.fetchall())
    
    def select(self,conexion: pg8000.Connection):
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {self.nombre_tabla}")
        return cursor.fetchall()
        
class TablaMesas(Tabla):
    def __init__(self):
        self.nombre_tabla = "mesas"

class TablaPlatos(Tabla):
    def __init__(self):
        self.nombre_tabla = "platos"
        
    def select_vista(self,conexion):
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM vista_platos")
        return cursor.fetchall()

class TablaTiposPlatos(Tabla):
    def __init__(self):
        self.nombre_tabla = "tipos_platos"

class TablaDivisas(Tabla):
    def __init__(self):
        self.nombre_tabla = "divisas"
        
