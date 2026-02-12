BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 07: INSERCIÓN EN MORTALIDAD MATERNA (3 Tablas en Cascada)
-- --------------------------------------------------------------------------------------

-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)
INSERT INTO persona_paciente (edad) VALUES (36);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (26);
INSERT INTO persona_paciente (edad) VALUES (33);
INSERT INTO persona_paciente (edad) VALUES (19);
INSERT INTO persona_paciente (edad) VALUES (36);
INSERT INTO persona_paciente (edad) VALUES (21);
INSERT INTO persona_paciente (edad) VALUES (23);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (35);
INSERT INTO persona_paciente (edad) VALUES (19);
INSERT INTO persona_paciente (edad) VALUES (34);
INSERT INTO persona_paciente (edad) VALUES (25);
INSERT INTO persona_paciente (edad) VALUES (29);
INSERT INTO persona_paciente (edad) VALUES (29);
INSERT INTO persona_paciente (edad) VALUES (31);
INSERT INTO persona_paciente (edad) VALUES (36);
INSERT INTO persona_paciente (edad) VALUES (25);
INSERT INTO persona_paciente (edad) VALUES (24);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (21);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (29);
INSERT INTO persona_paciente (edad) VALUES (20);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (26);
INSERT INTO persona_paciente (edad) VALUES (40);
INSERT INTO persona_paciente (edad) VALUES (18);
INSERT INTO persona_paciente (edad) VALUES (26);
INSERT INTO persona_paciente (edad) VALUES (20);
INSERT INTO persona_paciente (edad) VALUES (39);
INSERT INTO persona_paciente (edad) VALUES (22);
INSERT INTO persona_paciente (edad) VALUES (37);
INSERT INTO persona_paciente (edad) VALUES (31);
INSERT INTO persona_paciente (edad) VALUES (18);
INSERT INTO persona_paciente (edad) VALUES (40);
INSERT INTO persona_paciente (edad) VALUES (23);

-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 26, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 39, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 8, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 35, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 55, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 92, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 93, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 81, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 74, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 52, Sector Valmore Rodríguez.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 77, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 73, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 13, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 20, Sector Colinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 16, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 62, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 74, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 80, Sector Valmore Rodríguez.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 76, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 47, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 5, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 72, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 13, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 96, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 97, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 15, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 65, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 20, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 47, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 26, Sector Colinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 36, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 63, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 91, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 51, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 70, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 71, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 46, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));

-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_MATERNA (Detalle)
DELETE FROM mortalidad_materna;
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 36, '96109889', 'Claudia Castillo Ramírez', '27/12/1987', '11/10/2024', '01:14:00', '15/10/2024', '23:44:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 26, Sector Bicentenario.' LIMIT 1), 'sangrado vaginal, dolor pélvico, fiebre, secreción vaginal fétida.', 'Aborto inseguro', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50000 : 60000
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 35, '74570748', 'Edith Maldonado Olivo', '05/08/1987', '09/03/2025', '20:55:00', '09/03/2025', '09:54:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 39, Sector Pedro Camejo.' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50001 : 60001
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 34, '51978431', 'Margarita Figueroa Navarro', '28/08/1998', '16/08/2025', '07:28:00', '18/08/2025', '20:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 8, Sector Simón Bolívar.' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50002 : 60002
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 33, '29613065', 'Rosa María Rivera Chávez', '18/04/1992', '28/06/2025', '10:52:00', '30/06/2025', '02:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 35, Sector Bicentenario.' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50003 : 60003
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 32, '48996256', 'Alicia Velásquez Valencia', '26/02/2006', '04/07/2025', '08:16:00', '06/07/2025', '20:57:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 55, Sector Paraíso 2.' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50004 : 60004
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 31, '22552683', 'Julia Mendoza Barros', '07/09/1988', '18/07/2025', '09:49:00', '21/07/2025', '20:44:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 92, Sector Paraíso 2.' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50005 : 60005
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 30, '88014378', 'Valentina Barrios Consalvi', '10/02/2003', '03/03/2024', '06:03:00', '07/03/2024', '13:06:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 93, Sector Paraíso 1.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50006 : 60006
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 29, '75872570', 'Olivia Bermúdez Silva', '15/08/2002', '29/10/2025', '02:21:00', '02/11/2025', '03:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 81, Sector Las Villas.' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50007 : 60007
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 28, '89886448', 'Inés Marques Fajardo', '17/02/1988', '30/05/2025', '05:31:00', '30/05/2025', '14:57:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 74, Sector Paraíso 1.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50008 : 60008
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 27, '64441246', 'Alba Varela Briceño', '03/12/1988', '17/05/2024', '18:08:00', '21/05/2024', '13:42:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 52, Sector Valmore Rodríguez.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50009 : 60009
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 26, '33938606', 'Esperanza Barreto Baron', '23/11/2005', '07/06/2025', '14:04:00', '10/06/2025', '18:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 77, Sector Las Villas.' LIMIT 1), 'hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.', 'Preeclampsia', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50010 : 60010
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 25, '70256777', 'Diana Aranda León', '17/10/1990', '05/07/2025', '09:12:00', '06/07/2025', '10:34:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 73, Sector Bicentenario.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50011 : 60011
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 24, '80229471', 'Wilmer Castro Yépez', '20/09/1999', '17/02/2025', '09:33:00', '21/02/2025', '20:41:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 13, Sector Campo Oficina.' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50012 : 60012
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 23, '73768257', 'Nora Ramírez Vargas', '03/07/1996', '25/07/2025', '06:20:00', '28/07/2025', '12:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 20, Sector Colinas.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50013 : 60013
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 22, '79695598', 'Dolores Medina Calles', '19/05/1994', '05/03/2024', '05:59:00', '10/03/2024', '01:36:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 16, Sector Los Ángeles.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50014 : 60014
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 21, '52087162', 'Ángela Sandoval Sánchez', '06/05/1994', '04/05/2025', '02:41:00', '08/05/2025', '17:28:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 62, Sector Casco Central.' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50015 : 60015
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 20, '87469974', 'Elena Estrada Arismendi', '11/01/1988', '28/06/2024', '17:57:00', '01/07/2024', '04:25:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 74, Sector San José.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50016 : 60016
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 19, '22056930', 'María Torres Guerrero', '28/04/1999', '27/11/2024', '09:45:00', '28/11/2024', '07:24:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 80, Sector Valmore Rodríguez.' LIMIT 1), 'sangrado vaginal, dolor pélvico, fiebre, secreción vaginal fétida.', 'Aborto inseguro', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50017 : 60017
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 18, '73493025', 'Olivia Castañeda Arcila', '12/03/2000', '07/07/2024', '07:09:00', '11/07/2024', '13:04:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 76, Sector San José.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50018 : 60018
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 17, '93742515', 'Berta Contreras Cedeno', '02/06/1987', '08/01/2025', '17:20:00', '11/01/2025', '12:32:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 47, Sector Los Ángeles.' LIMIT 1), 'progresión de síntomas sin intervención, complicaciones evitables.', 'Retraso en la atención obstétrica', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50019 : 60019
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 16, '70826331', 'Fernanda Betancourt García', '18/06/2003', '14/02/2025', '15:19:00', '19/02/2025', '17:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 5, Sector La Floresta.' LIMIT 1), 'disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.', 'Embolia de líquido amniótico', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50020 : 60020
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 15, '96543263', 'Lilian Sierra Medina', '04/08/1988', '01/09/2025', '18:12:00', '06/09/2025', '07:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 72, Sector Bicentenario.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50021 : 60021
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 14, '36305075', 'Nora Granados Martínez', '07/10/1995', '21/06/2025', '12:19:00', '21/06/2025', '11:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 13, Sector Paraíso 2.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50022 : 60022
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 13, '27684188', 'Lismar Salas Cordero', '15/02/2005', '22/11/2025', '17:50:00', '27/11/2025', '06:42:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 96, Sector 19 de Marzo.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50023 : 60023
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 12, '84255521', 'Nelly Contreras Acosta', '19/05/1988', '05/10/2025', '06:57:00', '07/10/2025', '17:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 97, Sector Cementerio.' LIMIT 1), 'fiebre alta, hipotensión, confusión, taquicardia, escalofríos.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50024 : 60024
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 11, '91116897', 'Ruth Molina Flores', '01/06/1999', '11/09/2025', '19:57:00', '16/09/2025', '21:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 15, Sector La Floresta.' LIMIT 1), 'dolor abdominal agudo, sangrado vaginal, mareo, síncope.', 'Embarazo ectópico roto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50025 : 60025
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 10, '39519808', 'Miriam Urdaneta Rosales', '12/01/1984', '06/12/2024', '23:27:00', '07/12/2024', '22:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 65, Sector Paraíso 1.' LIMIT 1), 'dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.', 'Desprendimiento prematuro de placenta', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50026 : 60026
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 9, '30731976', 'Josefina Suárez Silva', '01/08/2006', '10/08/2024', '22:25:00', '13/08/2024', '08:29:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 20, Sector San José.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50027 : 60027
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 8, '90817960', 'Nora Azocar Bautista', '04/08/1998', '06/06/2025', '03:38:00', '06/06/2025', '02:05:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 47, Sector Bicentenario.' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50028 : 60028
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 7, '81043666', 'Xiomara Cisneros Serrano', '06/12/2004', '08/12/2024', '19:22:00', '13/12/2024', '11:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 26, Sector Colinas.' LIMIT 1), 'fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.', 'Infección puerperal', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50029 : 60029
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 6, '78587050', 'Pilar Velásquez Bermúdez', '31/12/1984', '25/01/2024', '19:00:00', '28/01/2024', '02:13:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 36, Sector Pueblo Nuevo Sur.' LIMIT 1), 'sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.', 'Hemorragia posparto', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50030 : 60030
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 5, '47169154', 'Milagros Zambrano Ramos', '21/08/2002', '29/10/2024', '17:34:00', '29/10/2024', '06:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 63, Sector Las Villas.' LIMIT 1), 'disnea súbita, dolor torácico, taquicardia, hemoptisis.', 'Embolia pulmonar', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50031 : 60031
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 4, '64591741', 'Soledad Mejía Campos', '09/11/1988', '10/12/2025', '22:10:00', '11/12/2025', '20:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 91, Sector Pedro Camejo.' LIMIT 1), 'presión elevada, proteinuria, edema, visión borrosa.', 'Trastornos hipertensivos del embarazo', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50032 : 60032
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 3, '70652057', 'Dolores Villegas Hernández', '25/05/1992', '20/01/2024', '02:31:00', '22/01/2024', '14:13:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 51, Sector Simón Bolívar.' LIMIT 1), 'hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.', 'Síndrome HELLP', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50033 : 60033
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 2, '39730457', 'Consuelo Barrios Quintana', '11/02/2006', '24/02/2024', '17:04:00', '28/02/2024', '12:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 70, Sector Campo Alegre.' LIMIT 1), 'convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.', 'Eclampsia', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50034 : 60034
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 1, '18981215', 'Esperanza Trejo Téllez', '10/09/1984', '31/08/2024', '08:50:00', '04/09/2024', '05:32:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 71, Sector Pueblo Nuevo Sur.' LIMIT 1), 'disnea súbita, dolor torácico, taquicardia, hemoptisis.', 'Embolia pulmonar', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50035 : 60035
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 0, '80622265', 'Rocío Quiñones Paz', '21/02/2000', '28/01/2024', '11:34:00', '01/02/2024', '20:44:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 46, Sector Las Villas.' LIMIT 1), 'disnea, fatiga, palpitaciones, edema periférico.', 'Cardiopatía preexistente agravada', '2026-02-11');
INSERT INTO mortalidad_materna (id_m) VALUES (LAST_INSERT_ROWID());
-- IDx Materna: 50036 : 60036
COMMIT;

-- TOTAL DE REGISTROS DE MORTALIDAD MATERNA GENERADOS: 37
-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.
