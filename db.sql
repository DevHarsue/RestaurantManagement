CREATE TABLE CLIENTES (
  cliente_id SERIAL PRIMARY KEY,
  cliente_nacionalidad VARCHAR NOT NULL,
  cliente_cedula INT NOT NULL,
  cliente_nombre TEXT NOT NULL,
  cliente_apellido TEXT NOT NULL,
  cliente_telefono TEXT,
  cliente_direccion TEXT
);

CREATE TABLE PLATOS (
  plato_id SERIAL PRIMARY KEY,
  plato_nombre TEXT NOT NULL,
  plato_descripcion TEXT NOT NULL,
  plato_precio FLOAT NOT NULL
);

CREATE TABLE DIVISAS (
  divisa_id SERIAL PRIMARY KEY,
  divisa_nombre TEXT NOT NULL,
  divisa_relacion FLOAT NOT NULL
);

CREATE TABLE MESAS (
  mesa_id SERIAL PRIMARY KEY,
  mesa_descripcion TEXT NOT NULL
);

CREATE TABLE ORDENES (
  orden_id SERIAL PRIMARY KEY,
  orden_fecha TIMESTAMP NOT NULL,
  mesa_id INT NOT NULL,
  cliente_id INT NOT NULL,
  FOREIGN KEY (mesa_id) REFERENCES MESAS (mesa_id),
  FOREIGN KEY (cliente_id) REFERENCES CLIENTES (cliente_id)
);

CREATE TABLE DETALLES_ORDENES_DIVISAS (
  detalle_orden_divisa SERIAL PRIMARY KEY,
  orden_id INT NOT NULL,
  divisa_id INT NOT NULL,
  detalle_orden_divisa_cantidad FLOAT NOT NULL,
  FOREIGN KEY (orden_id) REFERENCES ORDENES (orden_id),
  FOREIGN KEY (divisa_id) REFERENCES DIVISAS (divisa_id)
);

CREATE TABLE DETALLES_ORDENES_PLATOS (
  detalle_orden_plato_id SERIAL PRIMARY KEY,
  orden_id INT NOT NULL,
  plato_id INT NOT NULL,
  detalle_orden_plato_cantidad INT NOT NULL,
  FOREIGN KEY (orden_id) REFERENCES ORDENES (orden_id),
  FOREIGN KEY (plato_id) REFERENCES PLATOS (plato_id)
);

