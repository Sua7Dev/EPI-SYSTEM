BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 06: INSERCIÓN EN MORTALIDAD INFANTIL (3 Tablas en Cascada)
-- --------------------------------------------------------------------------------------

-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('2 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('5 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('4 Años');
INSERT INTO persona_paciente (edad) VALUES ('3 Años');

-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 50, Sector Barrio Blanco.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 38, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 68, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 34, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 39, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 51, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 10, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 50, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 19, Sector Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 26, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 16, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 71, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 28, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 85, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 37, Sector Las Malvinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 12, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 10, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 32, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 22, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 83, Sector Colinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 29, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 32, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 94, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 67, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 39, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 69, Sector Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 5, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 10, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 67, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 98, Sector Valmore Rodríguez.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 35, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 71, Sector Barrio Blanco.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 84, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 33, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 63, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 92, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 12, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 82, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 80, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 33, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 25, Sector Paraíso 1.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 32, Sector Colinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 33, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 13, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 90, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 76, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 32, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 10, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 45, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 58, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 86, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 61, Sector Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 71, Sector Las Malvinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 58, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 80, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 94, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 99, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 86, Sector Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 20, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 25, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 90, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 92, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 65, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 97, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 80, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));

-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_INFANTIL (Detalle)
DELETE FROM mortalidad_infantil;
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 64, '56110135', 'Pablo Castillo Quintana', '17/06/2019', '06/05/2024', '16:10:00', '07/05/2024', '16:10:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 50, Sector Barrio Blanco.' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ángela Reyes Varela');
-- IDx Infantil: 30000 : 40000
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 63, '60970973', 'Baltazar Chávez Morales', '31/03/2019', '24/02/2024', '08:22:00', '24/02/2024', '08:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 38, Sector Pedro Camejo.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Consuelo Zambrano Restrepo');
-- IDx Infantil: 30001 : 40001
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 62, '26558654', 'Victoria Peña Cicero', '15/11/2018', '26/01/2024', '21:34:00', '26/01/2024', '21:34:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 68, Sector Paraíso 2.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Catalina Contreras Blanco');
-- IDx Infantil: 30002 : 40002
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 61, '83854993', 'Felipe Trejo Paredes', '08/12/2020', '10/09/2024', '09:50:00', '10/09/2024', '09:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 34, Sector Campo Oficina.' LIMIT 1), 'deposiciones líquidas frecuentes, deshidratación, ojos hundidos, boca seca, letargo.', 'Diarrea aguda', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Jimena Rosales Granados');
-- IDx Infantil: 30003 : 40003
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 60, '71303970', 'Emma Baron Redondo', '19/08/2019', '27/06/2025', '10:49:00', '28/06/2025', '10:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 39, Sector Casco Central.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Oriana Herrera Marques');
-- IDx Infantil: 30004 : 40004
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 59, '96624546', 'Fermín Cisneros Gómez', '28/01/2020', '31/01/2025', '07:04:00', '31/01/2025', '07:04:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 51, Sector Campo Oficina.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yusmary Parra Mejía');
-- IDx Infantil: 30005 : 40005
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 58, '66373402', 'Luisana Duarte Valdez', '19/11/2022', '25/11/2024', '00:47:00', '25/11/2024', '00:47:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 10, Sector Simón Bolívar.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Alicia Cadenas Gómez');
-- IDx Infantil: 30006 : 40006
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 57, '80230547', 'René Valenzuela Fuentes', '18/09/2018', '25/01/2024', '16:13:00', '26/01/2024', '16:13:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 50, Sector Pueblo Nuevo Sur.' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Emma Briceño Ramos');
-- IDx Infantil: 30007 : 40007
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 56, '64063418', 'Agustín Véliz Pérez', '23/12/2019', '17/09/2025', '09:26:00', '18/09/2025', '09:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 19, Sector Central.' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Natalia Peraza Mejía');
-- IDx Infantil: 30008 : 40008
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 55, '62326612', 'Paula Peraza Arismendi', '03/05/2020', '04/12/2025', '20:38:00', '04/12/2025', '20:38:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 26, Sector Campo Oficina.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Fernanda Yépez Flores');
-- IDx Infantil: 30009 : 40009
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 54, '12398431', 'Yolanda Correa Salazar', '03/04/2023', '14/12/2025', '18:41:00', '14/12/2025', '18:41:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 16, Sector Casco Central.' LIMIT 1), 'fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.', 'Dengue grave', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Diana Arias Cárdenas');
-- IDx Infantil: 30010 : 40010
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 53, '46058784', 'Valentina Zambrano Granados', '16/06/2020', '26/03/2024', '11:22:00', '27/03/2024', '11:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 71, Sector Casco Central.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Juana Arismendi Acosta');
-- IDx Infantil: 30011 : 40011
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 52, '36148602', 'Emanuel Rivera Yépez', '05/05/2021', '18/09/2025', '08:55:00', '19/09/2025', '08:55:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 28, Sector Las Villas.' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Manuela Aular Carreño');
-- IDx Infantil: 30012 : 40012
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 51, '31143529', 'Irma Cadenas Quiñones', '14/03/2020', '27/02/2024', '21:50:00', '27/02/2024', '21:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 85, Sector Las Villas.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Xiomara Márquez Valenzuela');
-- IDx Infantil: 30013 : 40013
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 50, '70731183', 'Soledad Zapata Carvajal', '13/10/2021', '29/11/2024', '09:57:00', '29/11/2024', '09:57:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 37, Sector Las Malvinas.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Wilmer Acosta Vega');
-- IDx Infantil: 30014 : 40014
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 49, '38860109', 'Alba Contreras Jiménez', '19/09/2021', '06/07/2024', '17:30:00', '06/07/2024', '17:30:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 12, Sector Los Ángeles.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Catalina Navarro Barreto');
-- IDx Infantil: 30015 : 40015
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 48, '72115691', 'Raúl Salinas Borjas', '01/06/2019', '12/10/2024', '06:55:00', '12/10/2024', '06:55:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 10, Sector Paraíso 2.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Antonieta Del Castillo Arrate');
-- IDx Infantil: 30016 : 40016
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 47, '97716477', 'Fidel Cisneros Santana', '01/06/2020', '20/02/2025', '01:44:00', '21/02/2025', '01:44:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 32, Sector La Floresta.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Josefina Paz Chávez');
-- IDx Infantil: 30017 : 40017
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 46, '96479607', 'Patricio Gallegos Briceño', '28/12/2021', '03/04/2024', '01:45:00', '04/04/2024', '01:45:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 22, Sector Pueblo Nuevo Sur.' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Julia Marín Murillo');
-- IDx Infantil: 30018 : 40018
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 45, '97246821', 'Alberto Vargas Rojas', '02/01/2023', '04/06/2025', '22:16:00', '05/06/2025', '22:16:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 83, Sector Colinas.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Wilmer Casas Báez');
-- IDx Infantil: 30019 : 40019
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 44, '68643541', 'Walter Ortiz Gómez', '30/04/2021', '16/01/2025', '11:16:00', '16/01/2025', '11:16:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 29, Sector Pueblo Nuevo Sur.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Carmen Trejo Gutiérrez');
-- IDx Infantil: 30020 : 40020
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 43, '89684602', 'Carmen Álvarez Bandres', '28/10/2018', '21/06/2024', '14:46:00', '21/06/2024', '14:46:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 32, Sector Paraíso 1.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lilian Brito Sánchez');
-- IDx Infantil: 30021 : 40021
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 42, '79086693', 'Andrea Arias Restrepo', '09/10/2019', '17/02/2025', '22:48:00', '17/02/2025', '22:48:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 94, Sector Paraíso 2.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Camila Arias Romero');
-- IDx Infantil: 30022 : 40022
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 41, '68281574', 'Natalia Cedeno León', '04/10/2018', '28/06/2024', '08:04:00', '28/06/2024', '08:04:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 67, Sector Pueblo Nuevo Sur.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Xiomara Rivas Estrada');
-- IDx Infantil: 30023 : 40023
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 40, '60850267', 'Baltazar Mendoza Barreto', '11/02/2020', '08/05/2025', '17:37:00', '08/05/2025', '17:37:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 39, Sector Simón Bolívar.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Valentina Estrada Rojas');
-- IDx Infantil: 30024 : 40024
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 39, '19001323', 'Daniel Lozano Cordero', '08/08/2020', '29/12/2025', '14:47:00', '30/12/2025', '14:47:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 69, Sector Central.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Natalia Lozano Guerra');
-- IDx Infantil: 30025 : 40025
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 38, '91951616', 'Gabriela Núñez Zambrano', '28/01/2019', '01/04/2024', '01:18:00', '01/04/2024', '01:18:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 5, Sector Las Villas.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Valeria Pérez Yépez');
-- IDx Infantil: 30026 : 40026
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 37, '27587125', 'Isabel Castañeda Torres', '17/01/2022', '01/09/2024', '01:02:00', '01/09/2024', '01:02:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 10, Sector Paraíso 1.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Luisa Betancourt López');
-- IDx Infantil: 30027 : 40027
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 36, '21634260', 'Nora Carvajal Rojas', '19/03/2021', '24/05/2024', '04:13:00', '25/05/2024', '04:13:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 67, Sector Casco Central.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Rosa Trujillo Valencia');
-- IDx Infantil: 30028 : 40028
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 35, '77295540', 'Francisco Carreño Duarte', '02/05/2020', '21/12/2025', '21:19:00', '22/12/2025', '21:19:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 98, Sector Valmore Rodríguez.' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lourdes Maldonado Aguilar');
-- IDx Infantil: 30029 : 40029
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 34, '94695817', 'Juana Núñez Lozano', '20/01/2019', '18/08/2024', '03:41:00', '18/08/2024', '03:41:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 35, Sector Campo Oficina.' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ángela Salcedo Carreño');
-- IDx Infantil: 30030 : 40030
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 33, '53343983', 'Antonio Montes Aranda', '11/04/2019', '22/09/2024', '20:35:00', '23/09/2024', '20:35:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 71, Sector Barrio Blanco.' LIMIT 1), 'politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.', 'Accidentes de tránsito', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Clara Jaimes Castro');
-- IDx Infantil: 30031 : 40031
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 32, '31690024', 'Joaquín Olivo Bustamante', '17/02/2019', '15/08/2024', '17:53:00', '16/08/2024', '17:53:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 84, Sector La Floresta.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Inés Carreño Ramos');
-- IDx Infantil: 30032 : 40032
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 31, '24364914', 'Valeria Quintana Silva', '23/10/2018', '04/01/2024', '14:17:00', '04/01/2024', '14:17:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 33, Sector Campo Oficina.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mariángel Arévalo Vera');
-- IDx Infantil: 30033 : 40033
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 30, '36052892', 'René Murillo Casas', '08/11/2021', '13/12/2024', '09:49:00', '13/12/2024', '09:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 63, Sector Cementerio.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Zulimar Campo Casas');
-- IDx Infantil: 30034 : 40034
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 29, '69849450', 'Josefina Barros Contreras', '07/01/2020', '02/05/2024', '11:22:00', '03/05/2024', '11:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 92, Sector Pedro Camejo.' LIMIT 1), 'fiebre, tos, dificultad respiratoria, aleteo nasal, retracciones intercostales, cianosis.', 'Neumonía', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Olga Maldonado Arévalo');
-- IDx Infantil: 30035 : 40035
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 28, '60544701', 'Andrés Yánez Quintero', '03/07/2018', '21/02/2024', '05:16:00', '22/02/2024', '05:16:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 12, Sector Paraíso 2.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Rita Consalvi Miranda');
-- IDx Infantil: 30036 : 40036
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 27, '55583654', 'Samuel Bello Salas', '08/01/2021', '15/10/2024', '07:50:00', '16/10/2024', '07:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 82, Sector Campo Alegre.' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mariángel Soto Briceño');
-- IDx Infantil: 30037 : 40037
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 26, '31782716', 'María Maldonado Borjas', '09/10/2022', '02/12/2024', '11:26:00', '02/12/2024', '11:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 80, Sector San José.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Claudia Márquez Cordero');
-- IDx Infantil: 30038 : 40038
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 25, '42110128', 'Olivia Arcila Arguello', '26/06/2020', '17/02/2024', '10:39:00', '17/02/2024', '10:39:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 33, Sector Campo Oficina.' LIMIT 1), 'fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.', 'Dengue grave', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Génesis Cedeno Soto');
-- IDx Infantil: 30039 : 40039
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 24, '62599679', 'Lourdes Galindo Pinto', '25/06/2021', '18/09/2025', '17:35:00', '19/09/2025', '17:35:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 25, Sector Paraíso 1.' LIMIT 1), 'fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.', 'Dengue grave', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Olivia Toro Guevara');
-- IDx Infantil: 30040 : 40040
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 23, '96969298', 'Noé Bohorquez Colina', '20/01/2019', '22/12/2024', '20:43:00', '22/12/2024', '20:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 32, Sector Colinas.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gabriela Flores Trujillo');
-- IDx Infantil: 30041 : 40041
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 22, '71776669', 'Marco Arrate Salcedo', '25/11/2019', '22/06/2025', '21:40:00', '22/06/2025', '21:40:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 33, Sector 19 de Marzo.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Irma Vidal Bernal');
-- IDx Infantil: 30042 : 40042
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 21, '47818490', 'Xiomara Núñez Yépez', '13/05/2021', '03/08/2025', '03:01:00', '03/08/2025', '03:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 13, Sector Simón Bolívar.' LIMIT 1), 'fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.', 'Dengue grave', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ana Azocar Bermúdez');
-- IDx Infantil: 30043 : 40043
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 20, '93806064', 'Andrés Restrepo Chávez', '03/05/2020', '05/03/2025', '06:06:00', '06/03/2025', '06:06:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 90, Sector Pedro Camejo.' LIMIT 1), 'lesiones inexplicables, miedo a adultos, retraso en el desarrollo, retraimiento.', 'Abuso infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Marta Brito Vargas');
-- IDx Infantil: 30044 : 40044
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 19, '74112251', 'Clara Ibarra Zambrano', '25/05/2019', '14/09/2024', '13:37:00', '14/09/2024', '13:37:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 76, Sector Bicentenario.' LIMIT 1), 'fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.', 'Dengue grave', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Fernanda Salinas Guevara');
-- IDx Infantil: 30045 : 40045
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 18, '28940377', 'Oriana Ospina Soto', '27/03/2022', '29/06/2024', '09:33:00', '29/06/2024', '09:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 32, Sector Cementerio.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Julia Díaz Pinto');
-- IDx Infantil: 30046 : 40046
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 17, '61472986', 'Esperanza Castañeda Acosta', '10/01/2021', '01/01/2024', '22:29:00', '01/01/2024', '22:29:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 10, Sector 19 de Marzo.' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Julia Cicero Aguilar');
-- IDx Infantil: 30047 : 40047
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 16, '67027146', 'Saúl Naranjo Ortega', '13/11/2022', '25/06/2025', '05:33:00', '25/06/2025', '05:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 45, Sector La Floresta.' LIMIT 1), 'politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.', 'Accidentes de tránsito', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mariángel Serrano Castillo');
-- IDx Infantil: 30048 : 40048
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 15, '89149745', 'Walter Aguilar Borjas', '09/03/2022', '31/07/2024', '11:53:00', '31/07/2024', '11:53:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 58, Sector San José.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Irene Ortega Cisneros');
-- IDx Infantil: 30049 : 40049
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 14, '48946450', 'Julia Rosales Aguilar', '24/12/2018', '27/01/2024', '22:12:00', '27/01/2024', '22:12:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 86, Sector 19 de Marzo.' LIMIT 1), 'lesiones inexplicables, miedo a adultos, retraso en el desarrollo, retraimiento.', 'Abuso infantil', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Natalia Trejo Cabrera');
-- IDx Infantil: 30050 : 40050
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 13, '78432370', 'Juan Miranda Bernal', '07/05/2022', '28/08/2024', '19:10:00', '29/08/2024', '19:10:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 61, Sector Central.' LIMIT 1), 'desnutrición, falta de higiene, infecciones frecuentes, retraso en el crecimiento.', 'Negligencia', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elvira Paredes Moreno');
-- IDx Infantil: 30051 : 40051
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 12, '35846712', 'Yulimar Duarte Paredes', '30/03/2022', '10/12/2025', '19:57:00', '11/12/2025', '19:57:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 71, Sector Las Malvinas.' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gabriela Del Castillo Cadenas');
-- IDx Infantil: 30052 : 40052
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 11, '75363381', 'Jacobo Aular Rincón', '09/02/2022', '18/10/2024', '01:37:00', '19/10/2024', '01:37:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 58, Sector Campo Alegre.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Consuelo Casas Estrada');
-- IDx Infantil: 30053 : 40053
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 10, '32591903', 'Rodrigo Colina Castillo', '19/01/2023', '10/12/2025', '08:42:00', '11/12/2025', '08:42:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 80, Sector Pueblo Nuevo Sur.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Noelia Castro Mendoza');
-- IDx Infantil: 30054 : 40054
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 9, '49278232', 'Rocío Carrillo Colina', '30/10/2020', '30/01/2024', '21:01:00', '30/01/2024', '21:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 94, Sector Campo Alegre.' LIMIT 1), 'fiebre alta, rigidez de nuca, vómitos, irritabilidad, fontanela abombada, convulsiones.', 'Meningitis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mayerling Núñez Briceño');
-- IDx Infantil: 30055 : 40055
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 8, '87564005', 'Alba Varela Rincón', '17/04/2020', '06/06/2024', '23:50:00', '07/06/2024', '23:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 99, Sector Casco Central.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Noelia Villegas Contreras');
-- IDx Infantil: 30056 : 40056
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 7, '53015060', 'Consuelo Casas Ortiz', '10/01/2021', '16/02/2025', '01:03:00', '16/02/2025', '01:03:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 86, Sector Central.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mercedes Burgos Peraza');
-- IDx Infantil: 30057 : 40057
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 6, '13035502', 'Esteban Arcila Reyes', '17/11/2020', '06/08/2025', '01:45:00', '06/08/2025', '01:45:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 20, Sector Los Ángeles.' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yosmary Correa Rosales');
-- IDx Infantil: 30058 : 40058
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 5, '62552568', 'Gloria Gil Márquez', '09/07/2022', '20/08/2024', '18:10:00', '20/08/2024', '18:10:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 25, Sector Las Villas.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gloria Sierra Asuaje');
-- IDx Infantil: 30059 : 40059
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 4, '80781354', 'Soledad Gil López', '22/05/2020', '05/11/2025', '13:14:00', '06/11/2025', '13:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 90, Sector Las Villas.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Olga Núñez Rodríguez');
-- IDx Infantil: 30060 : 40060
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 3, '85751598', 'Daniela Carrillo Rivas', '26/11/2018', '04/04/2024', '13:42:00', '05/04/2024', '13:42:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 92, Sector Los Ángeles.' LIMIT 1), 'deposiciones líquidas frecuentes, deshidratación, ojos hundidos, boca seca, letargo.', 'Diarrea aguda', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Jimena Blanco Ruiz');
-- IDx Infantil: 30061 : 40061
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 2, '22335560', 'Luisana Bautista Mora', '15/01/2020', '16/10/2024', '06:47:00', '16/10/2024', '06:47:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 65, Sector Los Ángeles.' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Josefina Salinas Carrillo');
-- IDx Infantil: 30062 : 40062
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 1, '78241925', 'Luis Caballero Olivo', '11/03/2020', '09/05/2024', '11:14:00', '10/05/2024', '11:14:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 97, Sector Campo Oficina.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Rosa María Trujillo León');
-- IDx Infantil: 30063 : 40063
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 0, '85181915', 'Armando Abreu Álvarez', '26/12/2021', '21/01/2025', '13:52:00', '22/01/2025', '13:52:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 80, Sector Paraíso 2.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-03-29');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ana Quintana Cardona');
-- IDx Infantil: 30064 : 40064
COMMIT;

-- TOTAL DE REGISTROS DE MORTALIDAD INFANTIL GENERADOS: 65
-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.
