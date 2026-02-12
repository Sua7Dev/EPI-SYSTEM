BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 01: PREPARACIÓN GEOGRÁFICA (Morbilidad)
-- --------------------------------------------------------------------------------------
PRAGMA foreign_keys = OFF;
-- 1. INSERTAR MUNICIPIOS (usando autoincremento)
INSERT INTO municipio (nombre, id_ciudad) VALUES ('Guanipa', 1);

-- 2. INSERTAR PARROQUIAS (usando subconsulta para obtener id_municipio)
INSERT INTO parroquia (nombre, id_municipio) VALUES ('Miguel Otero Silva', (SELECT id_municipio FROM municipio WHERE nombre = 'Simón Rodríguez'));
INSERT INTO parroquia (nombre, id_municipio) VALUES ('San José de Guanipa', (SELECT id_municipio FROM municipio WHERE nombre = 'Guanipa'));
PRAGMA foreign_keys = ON;
COMMIT;
