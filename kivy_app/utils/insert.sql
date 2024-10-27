INSERT INTO tipos_platos(tipo_plato_nombre,tipo_plato_icon)
values('Bebida','cup-outline') ,('Comida','bowl-outline')

INSERT INTO platos(plato_nombre,plato_descripcion,plato_precio,tipo_plato_id)
values
('Carne','Carne frita de las mas arrechisima',13, 2),
('Pollo' ,'Pollo frito vale',10,2),
('Agua Panela','Ta fria mrk',1,1),
('Agua','Agua de la llave (no esta fria)',0.3,1);


INSERT INTO mesas(mesa_descripcion) values('MESA 1'),
('MESA 2'), ('MESA 3'), ('MESA 4'), ('MESA 5'), ('MESA 6');

INSERT INTO divisas(divisa_nombre,divisa_relacion)
VALUES('Dolar',1),('Bolivar',36),('COP',3700);



