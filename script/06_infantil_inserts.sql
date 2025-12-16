BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 06: INSERCIÓN EN MORTALIDAD INFANTIL (3 Tablas en Cascada)
-- --------------------------------------------------------------------------------------

-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);

-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 83, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 84, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 93, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Santa Cruz del Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 28, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mamo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 80, Sector Vía Clarines, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 75, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 51, Sector Casco Central, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 22, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 62, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 99, Sector Las Malvinas, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 1, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 98, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 35, Sector Vía Clarines, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 82, Sector Los Olivos, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 22, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mamo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 81, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 75, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 98, Sector Vía Clarines, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 25, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Santa Cruz del Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 28, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Santa Cruz del Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 19, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 44, Sector El Casco, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Boca de Uchire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 82, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 46, Sector El Casco, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Boca de Uchire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 54, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 36, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 55, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 90, Sector Las Malvinas, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 59, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 31, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 2, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 9, Sector Las Malvinas, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Boca de Uchire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 99, Sector Las Malvinas, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 92, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 18, Sector Vía San Tomé, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 25, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 73, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 91, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 70, Sector El Casco, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 84, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 35, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Piar'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 89, Sector El Casco, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Clarines'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 29, Sector Los Olivos, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 56, Sector Los Olivos, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 90, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 39, Sector Los Olivos, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 5, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 86, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 91, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 1, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 14, Sector Km 55, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mamo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 9, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 57, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 96, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 62, Sector Km 55, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mamo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 25, Sector Km 55, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 86, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 47, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 47, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 24, Sector Vía Clarines, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San Pablo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 40, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 1, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 86, Sector Vía Clarines, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San Pablo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 99, Sector Casco Central, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 34, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Piar'));

-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_INFANTIL (Detalle)
DELETE FROM mortalidad_infantil;
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 64, '56299650', 'Isaac Maldonado Borjas', '21/06/2021', '13/04/2025', '03:42:00', '14/04/2025', '03:42:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 83, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Catalina Zambrano Contreras');
-- IDx Infantil: 30000 : 40000
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 63, '76481404', 'Ninoska Cicero Castillo', '28/01/2021', '30/05/2025', '00:10:00', '31/05/2025', '00:10:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 84, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Camila Arteaga Flores');
-- IDx Infantil: 30001 : 40001
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 62, '91008118', 'Julian Santana Rojas', '02/05/2021', '28/05/2024', '04:51:00', '29/05/2024', '04:51:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 93, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.', 'Accidentes de tránsito', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Marta Mejía Paredes');
-- IDx Infantil: 30002 : 40002
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 61, '41548632', 'César Cedeno Betancourt', '16/11/2020', '27/07/2024', '15:31:00', '27/07/2024', '15:31:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 28, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.', 'Accidentes de tránsito', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gabriela Causado Mejía');
-- IDx Infantil: 30003 : 40003
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 60, '34731835', 'Rosa Castillo Caballero', '04/12/2020', '25/11/2024', '03:40:00', '26/11/2024', '03:40:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 80, Sector Vía Clarines, cerca del CDI. (Miranda)' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yulimar Serrano Rincón');
-- IDx Infantil: 30004 : 40004
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 59, '13552402', 'Bernardo Zambrano Torres', '20/10/2019', '21/12/2024', '20:07:00', '21/12/2024', '20:07:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 75, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.', 'Cardiopatías congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Irma Trujillo Medina');
-- IDx Infantil: 30005 : 40005
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 58, '73304789', 'Francisca Guerrero Asuaje', '01/12/2021', '15/12/2024', '23:38:00', '16/12/2024', '23:38:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 51, Sector Casco Central, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Verónica Álvarez Téllez');
-- IDx Infantil: 30006 : 40006
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 57, '77513878', 'Salvador Salinas Navia', '01/12/2018', '03/03/2024', '04:26:00', '03/03/2024', '04:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 22, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Soledad Aguilar Arcila');
-- IDx Infantil: 30007 : 40007
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 56, '36373525', 'Fidel Galindo Rosales', '11/10/2021', '28/11/2025', '17:05:00', '29/11/2025', '17:05:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 62, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ruth Quintana Fernández');
-- IDx Infantil: 30008 : 40008
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 55, '98218260', 'Fernanda Chávez Benitez', '27/09/2021', '22/08/2024', '12:01:00', '23/08/2024', '12:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 99, Sector Las Malvinas, cerca del CDI. (Miranda)' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Silvia Quintero Casas');
-- IDx Infantil: 30009 : 40009
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 54, '35432696', 'Daniela Salcedo Aular', '04/09/2020', '23/07/2024', '11:22:00', '23/07/2024', '11:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 1, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lismar Rodríguez Contreras');
-- IDx Infantil: 30010 : 40010
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 53, '64346423', 'Rosa Trejo Calles', '22/11/2021', '17/07/2024', '08:15:00', '17/07/2024', '08:15:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 98, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elena Rosales Lozano');
-- IDx Infantil: 30011 : 40011
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 52, '38143458', 'Susana Paz Báez', '27/01/2021', '15/08/2024', '10:37:00', '15/08/2024', '10:37:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 35, Sector Vía Clarines, cerca del CDI. (Miranda)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Daniela Valera Peña');
-- IDx Infantil: 30012 : 40012
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 51, '54693971', 'Petra Palacios Gómez', '14/04/2020', '08/06/2024', '23:27:00', '09/06/2024', '23:27:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 82, Sector Los Olivos, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elvira Marín Palma');
-- IDx Infantil: 30013 : 40013
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 50, '27897312', 'Gabriela Cruz Ramos', '29/11/2018', '04/07/2024', '04:00:00', '05/07/2024', '04:00:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 22, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yosmary Bello Salazar');
-- IDx Infantil: 30014 : 40014
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 49, '19418603', 'Alonso Prieto Núñez', '30/07/2022', '30/12/2025', '12:58:00', '31/12/2025', '12:58:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 81, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ruth Bandres Murillo');
-- IDx Infantil: 30015 : 40015
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 48, '28658132', 'Gregorio Herrera Mora', '29/11/2022', '08/09/2025', '05:36:00', '08/09/2025', '05:36:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 75, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Nora Rojas Valera');
-- IDx Infantil: 30016 : 40016
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 47, '23966721', 'Ninoska Causado Santana', '05/07/2023', '14/09/2025', '09:43:00', '14/09/2025', '09:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 98, Sector Vía Clarines, cerca del CDI. (Miranda)' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Luisana Cicero Quintero');
-- IDx Infantil: 30017 : 40017
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 46, '64581270', 'Manuel Quiroz Guerra', '27/06/2021', '18/04/2025', '04:13:00', '19/04/2025', '04:13:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 25, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lismar Zabala Pulido');
-- IDx Infantil: 30018 : 40018
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 45, '25083852', 'Berta Villalobos Baron', '02/09/2021', '05/09/2024', '23:33:00', '05/09/2024', '23:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 28, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'deposiciones líquidas frecuentes, deshidratación, ojos hundidos, boca seca, letargo.', 'Diarrea aguda', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elena Izquierdo Arroyo');
-- IDx Infantil: 30019 : 40019
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 44, '95484885', 'Rosa Abreu Guerra', '04/06/2020', '31/07/2025', '15:49:00', '01/08/2025', '15:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 19, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yulimar Briceño Briceño');
-- IDx Infantil: 30020 : 40020
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 43, '84897444', 'Cristóbal Avila Mendoza', '04/10/2020', '08/06/2025', '16:26:00', '08/06/2025', '16:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 44, Sector El Casco, cerca del CDI. (Miranda)' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Beatriz Barros Rangel');
-- IDx Infantil: 30021 : 40021
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 42, '74303564', 'Alberto Baron Quiñones', '29/12/2021', '23/08/2024', '00:40:00', '23/08/2024', '00:40:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 82, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Nelly Cicero Urdaneta');
-- IDx Infantil: 30022 : 40022
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 41, '42582634', 'Damián Álvarez Jaimes', '29/03/2023', '27/09/2025', '21:16:00', '28/09/2025', '21:16:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 46, Sector El Casco, cerca del CDI. (Miranda)' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Marta Fernández Suárez');
-- IDx Infantil: 30023 : 40023
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 40, '16205381', 'Ángela Hernández Bautista', '17/08/2021', '14/12/2025', '22:48:00', '15/12/2025', '22:48:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 54, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Miriam Briceño Palacios');
-- IDx Infantil: 30024 : 40024
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 39, '34590928', 'Pedro Olivo Vera', '17/11/2020', '05/09/2025', '01:48:00', '05/09/2025', '01:48:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 36, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre alta, rigidez de nuca, vómitos, irritabilidad, fontanela abombada, convulsiones.', 'Meningitis', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Daniela Quiñones Zambrano');
-- IDx Infantil: 30025 : 40025
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 38, '95696553', 'Gabriela Del Castillo Pereira', '27/10/2021', '26/10/2024', '14:01:00', '27/10/2024', '14:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 55, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Alicia Morales Rosales');
-- IDx Infantil: 30026 : 40026
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 37, '16467040', 'Victoria Ramos Aular', '28/07/2021', '14/11/2025', '22:26:00', '14/11/2025', '22:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 90, Sector Las Malvinas, cerca del CDI. (Miranda)' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Alicia Quintero Paz');
-- IDx Infantil: 30027 : 40027
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 36, '97772850', 'Fernando Toro Casas', '25/10/2022', '20/03/2025', '01:59:00', '21/03/2025', '01:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 59, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yusmary Rodríguez Avila');
-- IDx Infantil: 30028 : 40028
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 35, '21844788', 'Verónica Arcila Valera', '01/02/2020', '24/03/2025', '09:07:00', '25/03/2025', '09:07:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 31, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.', 'Dengue grave', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Fernanda León Barreto');
-- IDx Infantil: 30029 : 40029
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 34, '88911433', 'Lorenzo Quintana Montes', '23/07/2021', '08/06/2024', '15:33:00', '09/06/2024', '15:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 2, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ángela Aguilar Méndez');
-- IDx Infantil: 30030 : 40030
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 33, '16480396', 'Rita Zabala Campos', '05/12/2019', '22/11/2024', '01:17:00', '23/11/2024', '01:17:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 9, Sector Las Malvinas, cerca del CDI. (Miranda)' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Josefina Arjona Guevara');
-- IDx Infantil: 30031 : 40031
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 32, '32691426', 'Ramiro Castro Barros', '24/05/2022', '17/05/2025', '18:22:00', '17/05/2025', '18:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 99, Sector Las Malvinas, cerca del CDI. (Miranda)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Olga Barrios Figueroa');
-- IDx Infantil: 30032 : 40032
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 31, '78463220', 'Marta Benitez Burgos', '18/02/2020', '01/03/2025', '13:36:00', '01/03/2025', '13:36:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 92, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre, tos, dificultad respiratoria, aleteo nasal, retracciones intercostales, cianosis.', 'Neumonía', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Sofía Cordero Ibarra');
-- IDx Infantil: 30033 : 40033
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 30, '69975972', 'Marco Caballero Romero', '26/11/2020', '18/01/2025', '22:56:00', '18/01/2025', '22:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 18, Sector Vía San Tomé, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Fernanda Cortez Arguello');
-- IDx Infantil: 30034 : 40034
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 29, '57975039', 'Xiomara López Caballero', '27/03/2020', '16/11/2024', '16:41:00', '16/11/2024', '16:41:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 25, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Susana Romero Sierra');
-- IDx Infantil: 30035 : 40035
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 28, '61128280', 'Teodoro Bolivar Sierra', '24/08/2020', '20/08/2025', '05:31:00', '21/08/2025', '05:31:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 73, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'fiebre, tos, dificultad respiratoria, aleteo nasal, retracciones intercostales, cianosis.', 'Neumonía', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mercedes Varela Lozano');
-- IDx Infantil: 30036 : 40036
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 27, '63406869', 'Laura Jaimes Márquez', '22/11/2019', '08/07/2024', '00:21:00', '08/07/2024', '00:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 91, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mercedes Carvajal Amaya');
-- IDx Infantil: 30037 : 40037
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 26, '62829336', 'Fidel Valdez Silva', '05/01/2022', '22/08/2024', '12:37:00', '22/08/2024', '12:37:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 70, Sector El Casco, cerca del CDI. (Miranda)' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Juana Zapata Borjas');
-- IDx Infantil: 30038 : 40038
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 25, '65998388', 'Milagros Miranda Vera', '24/01/2021', '25/05/2025', '14:50:00', '25/05/2025', '14:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 84, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ruth Gómez Roldán');
-- IDx Infantil: 30039 : 40039
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 24, '30173136', 'Patricio Herrera Báez', '15/04/2022', '21/09/2024', '18:32:00', '21/09/2024', '18:32:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 35, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Silvia Ruiz Zambrano');
-- IDx Infantil: 30040 : 40040
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 23, '98798378', 'Ángel García Zabala', '19/11/2022', '20/12/2025', '12:59:00', '20/12/2025', '12:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 89, Sector El Casco, cerca del CDI. (Miranda)' LIMIT 1), 'cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.', 'Cardiopatías congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gladys Bernal Parra');
-- IDx Infantil: 30041 : 40041
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 22, '18058980', 'Felipe Arrate Arjona', '06/06/2019', '23/10/2024', '21:15:00', '24/10/2024', '21:15:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 29, Sector Los Olivos, cerca del CDI. (Guanipa)' LIMIT 1), 'cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.', 'Cardiopatías congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Alejandra Navarro Márquez');
-- IDx Infantil: 30042 : 40042
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 21, '14876994', 'César Arismendi Salinas', '17/09/2022', '18/12/2024', '21:05:00', '18/12/2024', '21:05:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 56, Sector Los Olivos, cerca del CDI. (Guanipa)' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Juana Torres Acosta');
-- IDx Infantil: 30043 : 40043
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 20, '59357909', 'Gerardo Abreu Cordero', '25/07/2021', '15/12/2024', '18:53:00', '16/12/2024', '18:53:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 90, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mariángel Bautista Cortez');
-- IDx Infantil: 30044 : 40044
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 19, '39281105', 'Pablo Salazar Casas', '20/01/2019', '28/05/2024', '12:01:00', '28/05/2024', '12:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 39, Sector Los Olivos, cerca del CDI. (Guanipa)' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lismar Arismendi Barros');
-- IDx Infantil: 30045 : 40045
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 18, '85816199', 'Julio Santana Barrios', '10/05/2021', '27/08/2024', '22:21:00', '28/08/2024', '22:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 5, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Raquel Miranda Palacios');
-- IDx Infantil: 30046 : 40046
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 17, '97744046', 'Luisana Acosta Lucena', '23/07/2021', '30/05/2025', '14:58:00', '30/05/2025', '14:58:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 86, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Daniela Cabrera Aular');
-- IDx Infantil: 30047 : 40047
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 16, '37627400', 'Ramón Celis Arcila', '02/01/2020', '29/05/2025', '23:01:00', '30/05/2025', '23:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 91, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Camila Salinas Bermúdez');
-- IDx Infantil: 30048 : 40048
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 15, '22658162', 'Ramón Quiñones González', '07/12/2021', '21/12/2024', '12:55:00', '21/12/2024', '12:55:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 1, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Marta Brito Izquierdo');
-- IDx Infantil: 30049 : 40049
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 14, '97749520', 'Antonio Ortega Paz', '02/12/2021', '09/02/2024', '11:17:00', '10/02/2024', '11:17:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 14, Sector Km 55, cerca del CDI. (Independencia)' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Carmen Brito Rincón');
-- IDx Infantil: 30050 : 40050
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 13, '32313942', 'Oriana Miranda Arjona', '07/10/2023', '21/10/2025', '23:14:00', '22/10/2025', '23:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 9, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre alta, rigidez de nuca, vómitos, irritabilidad, fontanela abombada, convulsiones.', 'Meningitis', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lucía López Arismendi');
-- IDx Infantil: 30051 : 40051
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 12, '95170293', 'Génesis Cadenas Pulido', '20/09/2022', '19/09/2024', '15:25:00', '20/09/2024', '15:25:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 57, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mercedes Baron Carvajal');
-- IDx Infantil: 30052 : 40052
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 11, '74115486', 'Aarón Roldán Suárez', '16/02/2021', '09/08/2025', '12:22:00', '10/08/2025', '12:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 96, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gloria Cadenas Baron');
-- IDx Infantil: 30053 : 40053
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 10, '75424096', 'Berta Villegas Granados', '22/03/2023', '17/07/2025', '02:51:00', '18/07/2025', '02:51:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 62, Sector Km 55, cerca del CDI. (Independencia)' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yusmary Chávez Reyes');
-- IDx Infantil: 30054 : 40054
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 9, '30883314', 'Walter Contreras Paz', '04/06/2022', '09/05/2025', '02:12:00', '09/05/2025', '02:12:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 25, Sector Km 55, cerca del CDI. (Independencia)' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Claudia Álvarez Varela');
-- IDx Infantil: 30055 : 40055
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 8, '57559493', 'Zulimar Trejo Yánez', '11/11/2021', '13/08/2025', '14:43:00', '14/08/2025', '14:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 86, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Alicia Briceño Velásquez');
-- IDx Infantil: 30056 : 40056
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 7, '66752253', 'Francisca Bohorquez Arguello', '21/10/2018', '28/02/2024', '13:59:00', '29/02/2024', '13:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 47, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'lesiones inexplicables, miedo a adultos, retraso en el desarrollo, retraimiento.', 'Abuso infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Noelia Caraballo Silva');
-- IDx Infantil: 30057 : 40057
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 6, '20460050', 'Yosmary Arias Gómez', '01/05/2022', '19/04/2025', '08:49:00', '20/04/2025', '08:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 47, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Antonieta Asuaje Figueroa');
-- IDx Infantil: 30058 : 40058
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 5, '42235854', 'Alejandro Lara Ruiz', '03/01/2023', '29/12/2025', '18:53:00', '29/12/2025', '18:53:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 24, Sector Vía Clarines, cerca del CDI. (Miranda)' LIMIT 1), 'lesiones inexplicables, miedo a adultos, retraso en el desarrollo, retraimiento.', 'Abuso infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Adriana Amaya Cantillo');
-- IDx Infantil: 30059 : 40059
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 4, '84966115', 'Noé Padilla Arguello', '09/05/2022', '11/05/2025', '11:51:00', '11/05/2025', '11:51:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 40, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ninoska Figueroa Bolivar');
-- IDx Infantil: 30060 : 40060
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 3, '26152178', 'Cristóbal Soto Causado', '11/02/2021', '22/11/2024', '10:51:00', '22/11/2024', '10:51:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 1, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Teresa Olivo Redondo');
-- IDx Infantil: 30061 : 40061
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 2, '61117022', 'César Celis Álvarez', '27/09/2021', '24/04/2025', '01:22:00', '24/04/2025', '01:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 86, Sector Vía Clarines, cerca del CDI. (Miranda)' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Bernarda Sierra Aranda');
-- IDx Infantil: 30062 : 40062
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 1, '66019662', 'Irma Díaz Escobar', '13/04/2020', '14/10/2024', '23:36:00', '15/10/2024', '23:36:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 99, Sector Casco Central, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'fiebre, tos, dificultad respiratoria, aleteo nasal, retracciones intercostales, cianosis.', 'Neumonía', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Jimena Arjona Padilla');
-- IDx Infantil: 30063 : 40063
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 0, '16878024', 'Gloria Palma Vargas', '03/06/2020', '23/08/2025', '12:32:00', '23/08/2025', '12:32:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 34, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.', 'Cardiopatías congénitas', '2025-12-16');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lidia Márquez Medina');
-- IDx Infantil: 30064 : 40064
COMMIT;

-- TOTAL DE REGISTROS DE MORTALIDAD INFANTIL GENERADOS: 65
-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.
