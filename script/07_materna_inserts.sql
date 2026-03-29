BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 07: INSERCIÓN EN MORTALIDAD MATERNA (3 Tablas en Cascada)
-- --------------------------------------------------------------------------------------

-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)
INSERT INTO persona_paciente (edad) VALUES ('40 Años');
INSERT INTO persona_paciente (edad) VALUES ('37 Años');
INSERT INTO persona_paciente (edad) VALUES ('30 Años');
INSERT INTO persona_paciente (edad) VALUES ('39 Años');
INSERT INTO persona_paciente (edad) VALUES ('24 Años');
INSERT INTO persona_paciente (edad) VALUES ('35 Años');
INSERT INTO persona_paciente (edad) VALUES ('18 Años');
INSERT INTO persona_paciente (edad) VALUES ('34 Años');
INSERT INTO persona_paciente (edad) VALUES ('30 Años');
INSERT INTO persona_paciente (edad) VALUES ('18 Años');
INSERT INTO persona_paciente (edad) VALUES ('36 Años');
INSERT INTO persona_paciente (edad) VALUES ('40 Años');
INSERT INTO persona_paciente (edad) VALUES ('39 Años');
INSERT INTO persona_paciente (edad) VALUES ('39 Años');
INSERT INTO persona_paciente (edad) VALUES ('29 Años');
INSERT INTO persona_paciente (edad) VALUES ('28 Años');
INSERT INTO persona_paciente (edad) VALUES ('24 Años');
INSERT INTO persona_paciente (edad) VALUES ('39 Años');
INSERT INTO persona_paciente (edad) VALUES ('29 Años');
INSERT INTO persona_paciente (edad) VALUES ('21 Años');
INSERT INTO persona_paciente (edad) VALUES ('35 Años');
INSERT INTO persona_paciente (edad) VALUES ('38 Años');
INSERT INTO persona_paciente (edad) VALUES ('26 Años');
INSERT INTO persona_paciente (edad) VALUES ('23 Años');
INSERT INTO persona_paciente (edad) VALUES ('30 Años');
INSERT INTO persona_paciente (edad) VALUES ('39 Años');
INSERT INTO persona_paciente (edad) VALUES ('22 Años');
INSERT INTO persona_paciente (edad) VALUES ('28 Años');
INSERT INTO persona_paciente (edad) VALUES ('19 Años');
INSERT INTO persona_paciente (edad) VALUES ('29 Años');
INSERT INTO persona_paciente (edad) VALUES ('21 Años');
INSERT INTO persona_paciente (edad) VALUES ('23 Años');
INSERT INTO persona_paciente (edad) VALUES ('23 Años');
INSERT INTO persona_paciente (edad) VALUES ('27 Años');
INSERT INTO persona_paciente (edad) VALUES ('40 Años');
INSERT INTO persona_paciente (edad) VALUES ('30 Años');
INSERT INTO persona_paciente (edad) VALUES ('32 Años');

-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 35, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 42, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 57, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 6, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 3, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 88, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 77, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 95, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 53, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 48, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 22, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 50, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 83, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 65, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 40, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 80, Sector Valmore Rodríguez.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 84, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 25, Sector Valmore Rodríguez.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 63, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 26, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 67, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 60, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 18, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 65, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 65, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 59, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 39, Sector Barrio Blanco.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 14, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 76, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 54, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 34, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 31, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 50, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 24, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 77, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 60, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 53, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));

-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_MATERNA (Detalle)
DELETE FROM mortalidad_materna;
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 36, '38003086', 'Xiomara Granados Bravo', '14/09/1984', '09/03/2025', '18:48:00', '09/03/2025', '01:53:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 35, Sector Paraíso 1.' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50000 : 60000
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 35, '32857185', 'Valeria Ortega Valenzuela', '14/11/1986', '20/04/2024', '12:19:00', '22/04/2024', '08:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 42, Sector Paraíso 2.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50001 : 60001
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 34, '37421988', 'Yolanda Villegas Calles', '10/08/1994', '10/09/2024', '06:30:00', '13/09/2024', '20:06:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 57, Sector Campo Oficina.' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50002 : 60002
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 33, '32997251', 'Irene Rangel Aguilar', '26/01/1986', '16/12/2025', '06:20:00', '18/12/2025', '20:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 6, Sector San José.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50003 : 60003
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 32, '57596481', 'Oriana Calles Silva', '02/01/2001', '27/07/2025', '09:09:00', '01/08/2025', '10:24:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 3, Sector Paraíso 1.' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50004 : 60004
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 31, '59523453', 'Gabriela Campo Aular', '24/03/1989', '29/11/2024', '12:16:00', '04/12/2024', '00:39:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 88, Sector Paraíso 2.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50005 : 60005
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 30, '34809431', 'Elvira Valenzuela Henríquez', '08/09/2007', '20/09/2025', '20:26:00', '21/09/2025', '01:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 77, Sector Las Villas.' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50006 : 60006
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 29, '32311427', 'Zulay Gallegos Salcedo', '20/04/1989', '20/03/2024', '15:20:00', '21/03/2024', '03:30:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 95, Sector Bicentenario.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50007 : 60007
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 28, '66247827', 'Isabel Navia Casas', '21/07/1995', '10/11/2025', '17:37:00', '14/11/2025', '09:52:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 53, Sector San José.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50008 : 60008
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 27, '63389651', 'Nelly Colina Méndez', '15/07/2006', '13/07/2024', '10:53:00', '14/07/2024', '19:36:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 48, Sector Casco Central.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50009 : 60009
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 26, '63597355', 'Olivia Escobar Rincón', '15/05/1989', '29/05/2025', '10:50:00', '31/05/2025', '06:38:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 22, Sector La Floresta.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50010 : 60010
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 25, '29923522', 'Soledad Sandoval Cedeno', '21/02/1984', '26/12/2024', '00:51:00', '30/12/2024', '17:46:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 50, Sector Los Ángeles.' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50011 : 60011
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 24, '91122311', 'Olivia Marín Acosta', '12/10/1984', '17/07/2024', '06:52:00', '22/07/2024', '11:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 83, Sector Casco Central.' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50012 : 60012
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 23, '73045876', 'Ángela Márquez Naranjo', '12/12/1985', '15/05/2025', '04:55:00', '20/05/2025', '11:03:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 65, Sector Paraíso 2.' LIMIT 1), 'hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.', 'Síndrome HELLP', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50013 : 60013
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 22, '55628608', 'Alicia García Arteaga', '24/03/1996', '24/04/2025', '12:08:00', '25/04/2025', '02:51:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 40, Sector Las Villas.' LIMIT 1), 'ausencia de control, detección tardía de complicaciones.', 'Falta de atención prenatal', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50014 : 60014
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 21, '19690930', 'Olga Barros Miranda', '31/07/1997', '30/09/2025', '17:19:00', '02/10/2025', '17:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 80, Sector Valmore Rodríguez.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50015 : 60015
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 20, '76650089', 'Pilar Ospina Zambrano', '01/01/2000', '07/04/2024', '14:30:00', '07/04/2024', '21:27:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 84, Sector Paraíso 1.' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50016 : 60016
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 19, '92178047', 'Josefina Valenzuela Ospina', '03/07/1984', '16/05/2024', '04:41:00', '17/05/2024', '05:46:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 25, Sector Valmore Rodríguez.' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50017 : 60017
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 18, '25410890', 'Alicia Velásquez Paredes', '17/12/1994', '24/01/2024', '18:41:00', '28/01/2024', '07:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 63, Sector Simón Bolívar.' LIMIT 1), 'hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.', 'Síndrome HELLP', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50018 : 60018
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 17, '79404806', 'Jimena Pereira Guerrero', '03/02/2004', '24/03/2025', '08:08:00', '29/03/2025', '04:00:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 26, Sector Paraíso 1.' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50019 : 60019
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 16, '28458796', 'Zulimar González Olivo', '29/03/1988', '14/01/2024', '12:53:00', '14/01/2024', '04:24:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 67, Sector San José.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50020 : 60020
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 15, '93560916', 'Ángela Salinas Arias', '14/10/1987', '13/12/2025', '08:05:00', '14/12/2025', '01:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 60, Sector Paraíso 2.' LIMIT 1), 'presión elevada, proteinuria, edema, visión borrosa.', 'Trastornos hipertensivos del embarazo', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50021 : 60021
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 14, '57536555', 'Alicia Amaya Casas', '11/04/1998', '24/10/2024', '09:08:00', '29/10/2024', '14:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 18, Sector Paraíso 1.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50022 : 60022
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 13, '91417195', 'Silvia Arias Paz', '11/12/2001', '05/07/2025', '07:40:00', '05/07/2025', '02:29:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 65, Sector Campo Alegre.' LIMIT 1), 'presión elevada, proteinuria, edema, visión borrosa.', 'Trastornos hipertensivos del embarazo', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50023 : 60023
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 12, '73649864', 'Emma Fuentes Vera', '18/07/1993', '24/01/2024', '02:38:00', '25/01/2024', '19:42:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 65, Sector Pedro Camejo.' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50024 : 60024
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 11, '37108827', 'Verónica Hernández Barreto', '03/12/1984', '02/11/2024', '23:49:00', '04/11/2024', '03:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 59, Sector Pueblo Nuevo Sur.' LIMIT 1), 'dolor abdominal súbito, sangrado vaginal, pérdida de tono uterino, sufrimiento fetal.', 'Ruptura uterina', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50025 : 60025
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 10, '31473761', 'Carolina Acosta Escobar', '28/04/2002', '24/01/2025', '20:29:00', '25/01/2025', '00:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 39, Sector Barrio Blanco.' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50026 : 60026
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 9, '28606717', 'Pilar Pulido Granados', '25/05/1995', '22/03/2024', '17:55:00', '22/03/2024', '23:28:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 14, Sector Las Villas.' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50027 : 60027
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 8, '93987168', 'Francisca Fajardo Mejía', '15/11/2004', '03/05/2024', '17:21:00', '07/05/2024', '11:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 76, Sector Pedro Camejo.' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50028 : 60028
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 7, '63082126', 'Margarita Báez Paz', '18/12/1994', '24/09/2024', '14:42:00', '29/09/2024', '19:16:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 54, Sector Los Ángeles.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50029 : 60029
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 6, '76254060', 'Lismar Márquez Vidal', '21/11/2003', '22/02/2025', '21:05:00', '27/02/2025', '16:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 34, Sector Pueblo Nuevo Sur.' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50030 : 60030
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 5, '13488702', 'Teresa Ibarra Arévalo', '23/02/2001', '24/09/2024', '00:59:00', '27/09/2024', '14:16:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 31, Sector Pedro Camejo.' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50031 : 60031
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 4, '17224714', 'Zulimar Abreu Urdaneta', '13/03/2001', '29/05/2024', '07:15:00', '30/05/2024', '18:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 50, Sector Cementerio.' LIMIT 1), 'ausencia de control, detección tardía de complicaciones.', 'Falta de atención prenatal', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50032 : 60032
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 3, '89468849', 'Luisana Burgos Benitez', '11/04/1997', '27/07/2024', '21:23:00', '27/07/2024', '21:19:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 24, Sector Pueblo Nuevo Sur.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50033 : 60033
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 2, '29000894', 'Nelly Zambrano Molina', '23/01/1984', '06/01/2025', '14:44:00', '08/01/2025', '21:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 77, Sector Pueblo Nuevo Sur.' LIMIT 1), 'ausencia de control, detección tardía de complicaciones.', 'Falta de atención prenatal', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50034 : 60034
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 1, '95065302', 'Antonieta Cruz Díaz', '30/01/1994', '14/12/2024', '09:35:00', '19/12/2024', '22:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 60, Sector 19 de Marzo.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50035 : 60035
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 0, '91509318', 'Rosa María Campos Salazar', '29/10/1991', '09/04/2024', '22:49:00', '09/04/2024', '15:48:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 53, Sector Los Ángeles.' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2026-03-29');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50036 : 60036
COMMIT;

-- TOTAL DE REGISTROS DE MORTALIDAD MATERNA GENERADOS: 37
-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.
