BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 01: PREPARACI�N GEOGR�FICA (Morbilidad)
-- --------------------------------------------------------------------------------------
PRAGMA foreign_keys = OFF;
-- 1. INSERTAR MUNICIPIOS (usando autoincremento)
INSERT INTO municipio (nombre, id_ciudad) VALUES ('Guanipa', 1);
INSERT INTO municipio (nombre, id_ciudad) VALUES ('Independencia', 1);
INSERT INTO municipio (nombre, id_ciudad) VALUES ('Miranda', 1);
INSERT INTO municipio (nombre, id_ciudad) VALUES ('José Gregorio Monagas', 1);

-- 2. INSERTAR PARROQUIAS (usando subconsulta para obtener id_municipio)
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Miguel Otero Silva', (SELECT id_municipio FROM municipio WHERE nombre = 'Simón Rodríguez'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Atapirire', (SELECT id_municipio FROM municipio WHERE nombre = 'Simón Rodríguez'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('San José de Guanipa', (SELECT id_municipio FROM municipio WHERE nombre = 'Guanipa'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('El Chaparro', (SELECT id_municipio FROM municipio WHERE nombre = 'Guanipa'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('San José de Anaco', (SELECT id_municipio FROM municipio WHERE nombre = 'Guanipa'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Ciudad Orinoco', (SELECT id_municipio FROM municipio WHERE nombre = 'Independencia'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Mamo', (SELECT id_municipio FROM municipio WHERE nombre = 'Independencia'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Soledad', (SELECT id_municipio FROM municipio WHERE nombre = 'Independencia'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Clarines', (SELECT id_municipio FROM municipio WHERE nombre = 'Miranda'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Boca de Uchire', (SELECT id_municipio FROM municipio WHERE nombre = 'Miranda'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('San Pablo', (SELECT id_municipio FROM municipio WHERE nombre = 'Miranda'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Mapire', (SELECT id_municipio FROM municipio WHERE nombre = 'José Gregorio Monagas'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Piar', (SELECT id_municipio FROM municipio WHERE nombre = 'José Gregorio Monagas'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Santa Cruz del Orinoco', (SELECT id_municipio FROM municipio WHERE nombre = 'José Gregorio Monagas'));
PRAGMA foreign_keys = ON;
COMMIT;
