-- Este archivo SQL contiene todas las consultas que se deben ejecutar antes 
-- de usar la Solinette por la primera vez.

-- 3 tablas estan mencionadas en este archivo:
-- + 'nombrevial_100930' : es la tabla obtenida luego de la importacion del shape del 
--   mismo nombre en Postgis. Es la capa de la red vial

-- + 'solinette_nombrevial_100930' : es la tabla obtenida ejecutando una consulta a partir
--   de 'nombrevial_100930'. Es sobre esta tabla que la Solinette busca las direcciones

-- + 'distritos_bd' : es la tabla obtenida luego de la importacion del shape del 
--   mismo nombre en Postgis. Es tabla sirve para afectar el código UBIGEO a las direccciones
--   a ubicar en función de su campo distrito.

-- Agrego un campo 'ubigeo2' a la tabla 'nombrevial_100930' y le doy el mismo 
-- valor que el campo 'ubigeo'
ALTER TABLE nombrevial_100930 ADD COLUMN ubigeo2 char(6);
UPDATE nombrevial_100930 SET ubigeo2 = ubigeo;


-- Creacion de la tabla de las vías para la Solinette
-- Necesito hacer un un group by sobre varios campos y un st_union(the_geom) 
-- para no tener varios objetos que tienen el mismo nombre, cuadra, tipo en 
-- el mismo distrito (pero solamente para los que tienen estos campos llenos)
create table solinette_nombrevial_100930 as  
(
	select categ_via, nombre_via, nombre_alt, cuadra, izqesquema, deresquema, ubigeo, ubigeo2, 
	st_linemerge(st_union(the_geom)) as the_geom from nombrevial_100930 
	where categ_via <> '' and nombre_via <> '' and cuadra <> '' and izqesquema is not NULL and deresquema is not NULL 
	and ubigeo <> '' and ubigeo2 <> ''
	group by categ_via, nombre_via, nombre_alt, cuadra, izqesquema, deresquema, ubigeo, ubigeo2	
);
-- Es importante notar que si se edita la tabla 'solinette_nombrevial_100930'
-- se debe volver a ejecutar esta consulta


-- Agrego un campo gid y lo lleno a partir de uan sequencia 
--(me va a servir como id)
alter table solinette_nombrevial_100930 add column gid int;
CREATE temp SEQUENCE seq_id_vias START 1;
update solinette_nombrevial_100930 set gid = nextval('seq_id_vias');


-- Agrego un campo 'nombre2' a la tabla 'distritos_bd'
ALTER TABLE distritos_bd ADD COLUMN nombre2 char(80);

-- Pimero le doy el mismo valor que el campo 'nombre'
UPDATE distritos_bd SET nombre2 = nombre;

-- Luego cambio el valor para algunos distritos para los cuales
-- hay 2 nombres o se escriben a menudo con errores ortográficos
UPDATE distritos_bd SET nombre2 = 'CERCADO DE LIMA' where nombre = 'LIMA';
UPDATE distritos_bd SET nombre2 = 'EL RIMAC' where nombre = 'RIMAC';
UPDATE distritos_bd SET nombre2 = 'CARMEN DE LA LEGUA' where nombre = 'CARMEN DE LA LEGUA REYNOSO';
UPDATE distritos_bd SET nombre2 = 'BREÑA' where nombre = 'BRENA';
UPDATE distritos_bd SET nombre2 = 'SURCO' where nombre = 'SANTIAGO DE SURCO';
UPDATE distritos_bd SET nombre2 = 'MAGDALENA VIEJA' where nombre = 'PUEBLO LIBRE';
UPDATE distritos_bd SET nombre2 = 'ATE' where nombre = 'ATE VITARTE';
UPDATE distritos_bd SET nombre2 = 'VILLA MARIA' where nombre = 'VILLA MARIA DEL TRIUNFO';
UPDATE distritos_bd SET nombre2 = 'EL CALLAO' where nombre = 'CALLAO';
UPDATE distritos_bd SET nombre2 = 'MAGDALENA' where nombre = 'MAGDALENA DEL MAR';
UPDATE distritos_bd SET nombre2 = 'SANTA MARIA' where nombre = 'SANTA MARIA DEL MAR';
UPDATE distritos_bd SET nombre2 = 'CHORILLOS' where nombre = 'CHORRILLOS';
UPDATE distritos_bd SET nombre2 = 'BARANCO' where nombre = 'BARRANCO';
UPDATE distritos_bd SET nombre2 = 'SAN MARTIN DE PORRAS' where nombre = 'SAN MARTIN DE PORRES';
UPDATE distritos_bd SET nombre2 = 'SAN PEDRO DE CARABAYLLO' where nombre = 'CARABAYLLO';


