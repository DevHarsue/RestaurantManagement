import pg8000
import datetime
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
        
class TablaMesasOcupadas(Tabla):
    def __init__(self):
        self.nombre_tabla = "mesas_ocupadas"
        
    def insert(self,conexion: pg8000.Connection,mesa_id,orden_id):
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO mesas_ocupadas(mesa_id,orden_id) VALUES({mesa_id},{orden_id}) RETURNING *;")
        return cursor.fetchall()
    
        
class TablaOrdenes(Tabla):
    def __init__(self):
        self.nombre_tabla = "ordenes"
    
    def insert(self,conexion: pg8000.Connection):
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO ordenes(orden_fecha) VALUES('{str(datetime.datetime.today())[0:10]}') RETURNING *;")
        return cursor.fetchall()

class TablaDetallesOrdenesPlatos(Tabla):
    def __init__(self):
        self.nombre_tabla = "detalles_ordenes_platos"
    
    def insert(self,conexion: pg8000.Connection,orden_id,platos):
        cursor = conexion.cursor()
        platos_text_sql = ""
        for plato in platos:
            platos_text_sql += f"({orden_id},{plato[0]},{plato[1]}),"
        platos_text_sql = platos_text_sql[0:len(platos_text_sql)-1]
        cursor.execute(f"INSERT INTO detalles_ordenes_platos(orden_id,plato_id,detalle_orden_plato_cantidad) VALUES{platos_text_sql} RETURNING *;")
        return cursor.fetchall()
    
    def select_platos_orden_id(self,conexion: pg8000.Connection,orden_id):
        cursor = conexion.cursor()
        cursor.execute(f"SELECT plato_id FROM detalles_ordenes_platos WHERE orden_id={orden_id};")
        return cursor.fetchall()
    
    def update(self,conexion: pg8000.Connection,orden_id,plato_id,cantidad):
        cursor = conexion.cursor()
        cursor.execute(f"UPDATE detalles_ordenes_platos SET detalle_orden_plato_cantidad=detalle_orden_plato_cantidad+{cantidad} WHERE orden_id={orden_id} AND plato_id={plato_id} RETURNING *;")
        return cursor.fetchall()
    
    def select_calcular_total(self,conexion: pg8000.Connection,orden_id):
        cursor = conexion.cursor()
        cursor.execute(f"""SELECT sum(total) 
        FROM(SELECT SUM(dop.detalle_orden_plato_cantidad)*p.plato_precio as total
        FROM detalles_ordenes_platos as dop JOIN platos as p
        ON p.plato_id=dop.plato_id
        WHERE orden_id = {orden_id}
        GROUP BY p.plato_id)""")
        return cursor.fetchone()
    
