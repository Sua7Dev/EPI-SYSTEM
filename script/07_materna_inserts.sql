BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 07: INSERCIÓN EN MORTALIDAD MATERNA (3 Tablas en Cascada)
-- --------------------------------------------------------------------------------------

-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)
INSERT INTO persona_paciente (edad) VALUES (32);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (25);
INSERT INTO persona_paciente (edad) VALUES (30);
INSERT INTO persona_paciente (edad) VALUES (20);
INSERT INTO persona_paciente (edad) VALUES (31);
INSERT INTO persona_paciente (edad) VALUES (18);
INSERT INTO persona_paciente (edad) VALUES (22);
INSERT INTO persona_paciente (edad) VALUES (22);
INSERT INTO persona_paciente (edad) VALUES (30);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (39);
INSERT INTO persona_paciente (edad) VALUES (36);
INSERT INTO persona_paciente (edad) VALUES (35);
INSERT INTO persona_paciente (edad) VALUES (24);
INSERT INTO persona_paciente (edad) VALUES (31);
INSERT INTO persona_paciente (edad) VALUES (29);
INSERT INTO persona_paciente (edad) VALUES (27);
INSERT INTO persona_paciente (edad) VALUES (36);
INSERT INTO persona_paciente (edad) VALUES (24);
INSERT INTO persona_paciente (edad) VALUES (21);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (34);
INSERT INTO persona_paciente (edad) VALUES (21);
INSERT INTO persona_paciente (edad) VALUES (18);
INSERT INTO persona_paciente (edad) VALUES (20);
INSERT INTO persona_paciente (edad) VALUES (27);
INSERT INTO persona_paciente (edad) VALUES (26);
INSERT INTO persona_paciente (edad) VALUES (22);
INSERT INTO persona_paciente (edad) VALUES (36);
INSERT INTO persona_paciente (edad) VALUES (24);
INSERT INTO persona_paciente (edad) VALUES (18);
INSERT INTO persona_paciente (edad) VALUES (24);
INSERT INTO persona_paciente (edad) VALUES (30);
INSERT INTO persona_paciente (edad) VALUES (26);
INSERT INTO persona_paciente (edad) VALUES (35);
INSERT INTO persona_paciente (edad) VALUES (36);

-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 18, Sector El Palomar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 49, Sector Casco Central, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 69, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Piar'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 78, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mamo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 67, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 77, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 52, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 49, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 70, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 78, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Ciudad Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 79, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 100, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 6, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 13, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Santa Cruz del Orinoco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 81, Sector El Casco, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Boca de Uchire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 97, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'El Chaparro'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 46, Sector Casco Central, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 62, Sector Km 55, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 18, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 42, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 63, Sector Casco Central, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 65, Sector El Centro, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 85, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 9, Sector La Esperanza, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Soledad'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 30, Sector El Centro, cerca del CDI. (Independencia)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mamo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 12, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 22, Sector Las Malvinas, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San Pablo'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 7, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 64, Sector Las Malvinas, cerca del CDI. (Miranda)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Boca de Uchire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 37, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 79, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Anaco'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 1, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Piar'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 10, Sector Centro, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 8, Sector Casco Central, cerca del CDI. (Simón Rodríguez)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Atapirire'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 8, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Piar'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 85, Sector Los Olivos, cerca del CDI. (Guanipa)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 79, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Mapire'));

-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_MATERNA (Detalle)
DELETE FROM mortalidad_materna;
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 36, '36247668', 'Irene Rivas Salas', '28/11/1992', '08/11/2025', '12:05:00', '11/11/2025', '09:09:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 18, Sector El Palomar, cerca del CDI. (Guanipa)' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50000 : 60000
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 35, '25404242', 'Consuelo Rodríguez Vásquez', '24/06/1986', '13/01/2024', '10:12:00', '17/01/2024', '00:23:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 49, Sector Casco Central, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'dolor abdominal súbito, sangrado vaginal, pérdida de tono uterino, sufrimiento fetal.', 'Ruptura uterina', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50001 : 60001
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 34, '67734584', 'Gloria Avila Guerra', '16/03/1999', '25/11/2024', '22:35:00', '25/11/2024', '22:23:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 69, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50002 : 60002
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 33, '70943276', 'Rocío Mendoza Rivera', '25/01/1995', '24/09/2025', '07:04:00', '28/09/2025', '02:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 78, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'ausencia de control, detección tardía de complicaciones.', 'Falta de atención prenatal', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50003 : 60003
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 32, '72776681', 'Victoria Benitez Zambrano', '03/02/2005', '05/09/2025', '09:04:00', '08/09/2025', '21:11:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 67, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50004 : 60004
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 31, '66258953', 'Elvira Ibarra Ortega', '17/01/1994', '03/08/2025', '07:20:00', '07/08/2025', '18:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 77, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50005 : 60005
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 30, '64790746', 'Josefina Navarro Zabala', '16/02/2006', '25/01/2025', '10:47:00', '29/01/2025', '14:57:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 52, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'disnea súbita, dolor torácico, taquicardia, hemoptisis.', 'Embolia pulmonar', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50006 : 60006
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 29, '76687054', 'Yosmary Ortiz Fajardo', '04/08/2001', '18/05/2024', '01:02:00', '22/05/2024', '16:02:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 49, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.', 'Síndrome HELLP', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50007 : 60007
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 28, '23630300', 'Raquel Pérez Flores', '19/05/2001', '29/04/2024', '08:43:00', '01/05/2024', '07:58:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 70, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'dolor abdominal súbito, sangrado vaginal, pérdida de tono uterino, sufrimiento fetal.', 'Ruptura uterina', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50008 : 60008
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 27, '97229314', 'Verónica Navia Arcila', '09/11/1994', '12/08/2025', '08:01:00', '15/08/2025', '13:02:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 78, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50009 : 60009
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 26, '94865144', 'Patricia Guerrero Palacios', '21/11/1986', '13/03/2024', '07:41:00', '18/03/2024', '02:52:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 79, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50010 : 60010
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 25, '45851214', 'Yusbely González Restrepo', '18/07/1985', '06/08/2024', '19:35:00', '08/08/2024', '19:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 100, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'sangrado vaginal, dolor pélvico, fiebre, secreción vaginal fétida.', 'Aborto inseguro', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50011 : 60011
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 24, '50915711', 'Claudia Causado Colina', '27/11/1988', '07/10/2025', '22:25:00', '12/10/2025', '06:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 6, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50012 : 60012
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 23, '75039193', 'Gabriela Maldonado Consalvi', '02/08/1989', '10/08/2024', '22:14:00', '11/08/2024', '04:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 13, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50013 : 60013
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 22, '42546259', 'Adriana Carrillo Fernández', '05/06/2000', '27/07/2024', '11:41:00', '01/08/2024', '14:31:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 81, Sector El Casco, cerca del CDI. (Miranda)' LIMIT 1), 'hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.', 'Síndrome HELLP', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50014 : 60014
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 21, '92395278', 'Noelia Castillo Fuentes', '08/11/1993', '17/11/2024', '03:10:00', '18/11/2024', '09:15:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 97, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50015 : 60015
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 20, '22327902', 'Elisa Cárdenas Quintana', '19/11/1994', '02/07/2024', '21:15:00', '02/07/2024', '22:55:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 46, Sector Casco Central, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50016 : 60016
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 19, '92505115', 'Noelia Zapata Arévalo', '16/07/1997', '16/06/2025', '23:16:00', '19/06/2025', '21:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 62, Sector Km 55, cerca del CDI. (Independencia)' LIMIT 1), 'dolor abdominal súbito, sangrado vaginal, pérdida de tono uterino, sufrimiento fetal.', 'Ruptura uterina', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50017 : 60017
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 18, '12301416', 'Teresa Guevara Cardona', '11/11/1988', '25/06/2025', '06:17:00', '26/06/2025', '17:27:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 18, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50018 : 60018
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 17, '22035992', 'Xiomara Cárdenas González', '11/10/1999', '05/07/2024', '15:32:00', '08/07/2024', '11:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 42, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50019 : 60019
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 16, '72822990', 'Yusmary Acosta Sierra', '19/09/2002', '14/05/2024', '20:41:00', '14/05/2024', '15:06:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 63, Sector Casco Central, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'ausencia de control, detección tardía de complicaciones.', 'Falta de atención prenatal', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50020 : 60020
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 15, '55814847', 'Edith Calderón Casas', '30/08/1986', '13/08/2024', '15:36:00', '14/08/2024', '10:15:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 65, Sector El Centro, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'ausencia de control, detección tardía de complicaciones.', 'Falta de atención prenatal', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50021 : 60021
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 14, '17118123', 'Ana Zambrano Valenzuela', '14/11/1990', '09/12/2024', '08:26:00', '14/12/2024', '10:09:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 85, Sector Campo Alegre, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50022 : 60022
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 13, '77853044', 'Emma Benitez González', '07/04/2002', '04/03/2024', '10:25:00', '05/03/2024', '01:05:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 9, Sector La Esperanza, cerca del CDI. (Independencia)' LIMIT 1), 'hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.', 'Síndrome HELLP', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50023 : 60023
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 12, '41976881', 'Yusmary Azocar Arteaga', '11/10/2006', '09/05/2025', '00:28:00', '09/05/2025', '10:03:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 30, Sector El Centro, cerca del CDI. (Independencia)' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50024 : 60024
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 11, '71807469', 'Pilar Moreno Cruz', '14/08/2004', '30/03/2025', '01:31:00', '30/03/2025', '15:54:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 12, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50025 : 60025
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 10, '98018191', 'Mercedes Blanco Zambrano', '20/08/1998', '23/09/2025', '00:27:00', '26/09/2025', '09:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 22, Sector Las Malvinas, cerca del CDI. (Miranda)' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50026 : 60026
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 9, '99407517', 'Marta Quintero Peraza', '05/08/1999', '23/09/2025', '04:46:00', '23/09/2025', '05:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 7, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50027 : 60027
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 8, '18837000', 'Nora Caballero Cabrera', '28/05/2001', '07/02/2024', '19:56:00', '10/02/2024', '05:41:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 64, Sector Las Malvinas, cerca del CDI. (Miranda)' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50028 : 60028
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 7, '71928003', 'Jimena López Vega', '21/04/1988', '25/06/2024', '18:57:00', '25/06/2024', '19:57:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 37, Sector Pueblo Nuevo Sur, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50029 : 60029
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 6, '42842697', 'Inés Zambrano Campo', '07/09/2000', '30/10/2024', '20:58:00', '02/11/2024', '19:29:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 79, Sector Barrio Simón Bolívar, cerca del CDI. (Guanipa)' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50030 : 60030
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 5, '45345961', 'Beatriz Valdez Arjona', '07/03/2006', '27/10/2024', '05:45:00', '31/10/2024', '05:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 1, Sector Punta de Mata, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50031 : 60031
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 4, '11629357', 'Pilar Carvajal Salinas', '12/10/2000', '31/08/2025', '00:32:00', '04/09/2025', '11:31:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 10, Sector Centro, cerca del CDI. (Guanipa)' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50032 : 60032
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 3, '61555902', 'Adriana Barboza Márquez', '08/07/1994', '07/01/2025', '00:22:00', '09/01/2025', '08:39:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 8, Sector Casco Central, cerca del CDI. (Simón Rodríguez)' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50033 : 60033
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 2, '55374753', 'Mariángel Valera Ruiz', '14/03/1999', '12/07/2025', '15:29:00', '12/07/2025', '17:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 8, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50034 : 60034
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 1, '30530660', 'Petra Gómez Herrera', '18/08/1990', '12/09/2025', '18:10:00', '14/09/2025', '21:07:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 85, Sector Los Olivos, cerca del CDI. (Guanipa)' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50035 : 60035
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 0, '47957177', 'Antonieta Miranda Guevara', '08/06/1989', '22/11/2025', '19:27:00', '27/11/2025', '14:13:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 79, Sector Sector Las Vegas, cerca del CDI. (José Gregorio Monagas)' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2025-12-16');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50036 : 60036
COMMIT;

-- TOTAL DE REGISTROS DE MORTALIDAD MATERNA GENERADOS: 37
-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.
