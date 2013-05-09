


-- creo una tabla vacia
create table empresas_top10000 (
    id        integer,
    ruc_txt     char(11),
    empresa    char(255),
    direccion       char(255),
    distrito        char(80)
);

SET CLIENT_ENCODING TO 'LATIN1';
-- Lleno mi tabla a partir del archivo csv o texto
copy empresas_top10000 from E'C:\\empresas_top10000.csv' DELIMITERS ';'



-- creo una tabla vacia
create table empresas_transporte (
     id        integer,
     ruc    char(15),
     nombre     char(150),
     direccion       char(150),
     distrito        char(80),
     telefono char(30),
     servicio char(50)
 );
SET CLIENT_ENCODING TO 'LATIN1';
copy empresas_transporte from 'C:\empresas_final.csv' DELIMITERS ';';



--hago un backup de la capa de vias
create table nombrevial_09_30_backup  as
(
	select * from nombrevial_09_30
);


-- edicion de la tabla de las vias
-- necesito hacer un un group by sobre varios campos y un st_linemerge(st_union(the_geom)) para no tener varios
-- objetos que tienen el mismo nombre, cuadra, tipo en el mismo distrito (pero solamente para los que tienen estos campos llenos)

create table nombrevial_09_30_solinette as  
(
	select "CATEG_VIA", "NOMBRE_VIA", "NOMBRE_ALT", "CUADRA", "IZQESQUEMA", "DERESQUEMA", "UBIGEO", ubigeo2, 
	st_linemerge(st_union(the_geom)) as the_geom from nombrevial_09_30 
	where "CATEG_VIA" <> '' and "NOMBRE_VIA" <> '' and "CUADRA" <> '' and "IZQESQUEMA" is not NULL and "DERESQUEMA"is not NULL 
	and "UBIGEO" <> '' and ubigeo2 <> ''
	group by "CATEG_VIA", "NOMBRE_VIA", "NOMBRE_ALT", "CUADRA", "IZQESQUEMA", "DERESQUEMA", "UBIGEO", ubigeo2	
);

-- Agrego un campo gid
alter table nombrevial_09_30_solinette add column gid int;
CREATE temp SEQUENCE seq_id_vias START 1;
update nombrevial_09_30_solinette set gid = nextval('seq_id_vias');