BEGIN TRANSACTION;
-- --------------------------------------------------------------------------------------
-- SCRIPT 06: INSERCIÓN EN MORTALIDAD INFANTIL (3 Tablas en Cascada)
-- --------------------------------------------------------------------------------------

-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (5);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (3);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (4);
INSERT INTO persona_paciente (edad) VALUES (2);
INSERT INTO persona_paciente (edad) VALUES (4);

-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 22, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 90, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 52, Sector Colinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 20, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 92, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 39, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 95, Sector Barrio Blanco.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 52, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 22, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 98, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 81, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 82, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 70, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 53, Sector Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 26, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 33, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 67, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 1, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 13, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 78, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 9, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 44, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 89, Sector Valmore Rodríguez.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 6, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 59, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 9, Sector Los Ángeles.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 29, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 1, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 33, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 9, Sector Bicentenario.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 99, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 45, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 97, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 83, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 9, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 34, Sector Barrio Blanco.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 54, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 46, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 48, Sector Barrio Blanco.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 86, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 74, Sector Las Villas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 50, Sector San José.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 28, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 75, Sector Las Malvinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 20, Sector La Floresta.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 9, Sector Simón Bolívar.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 97, Sector Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 98, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 87, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 86, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 1, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 6, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 12, Sector Las Malvinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 37, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 73, Sector Cementerio.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 35, Sector Paraíso 2.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 67, Sector Campo Alegre.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 95, Sector Pueblo Nuevo Sur.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 57, Sector Casco Central.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 69, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 15, Sector Las Malvinas.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Avenida 54, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Carrera 30, Sector Pedro Camejo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Edmundo Barrios'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 78, Sector 19 de Marzo.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'San José de Guanipa'));
INSERT INTO direccion (descripcion, id_parroquia) VALUES ('Calle 98, Sector Campo Oficina.', (SELECT id_parroquia FROM parroquia WHERE nombre = 'Miguel Otero Silva'));

-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_INFANTIL (Detalle)
DELETE FROM mortalidad_infantil;
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 64, '60497748', 'Susana Burgos Valdez', '10/10/2022', '30/04/2025', '03:59:00', '01/05/2025', '03:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 22, Sector Los Ángeles.' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Daniela Barrios Calderón');
-- IDx Infantil: 30000 : 40000
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 63, '92775607', 'Salvador Campos Valera', '17/09/2022', '07/08/2025', '10:26:00', '08/08/2025', '10:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 90, Sector Paraíso 2.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Teresa Suárez Cortez');
-- IDx Infantil: 30001 : 40001
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 62, '24252841', 'Natalia Briceño Navia', '01/05/2020', '16/10/2024', '04:26:00', '16/10/2024', '04:26:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 52, Sector Colinas.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Cecilia Bautista Correa');
-- IDx Infantil: 30002 : 40002
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 61, '76308842', 'Alejandro Guevara Rosales', '06/08/2022', '30/05/2025', '07:20:00', '31/05/2025', '07:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 20, Sector Campo Oficina.' LIMIT 1), 'signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).', 'Malformaciones congénitas', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yosmary Silva Santana');
-- IDx Infantil: 30003 : 40003
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 60, '38200209', 'Alba Yépez González', '19/07/2021', '15/07/2025', '09:38:00', '16/07/2025', '09:38:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 92, Sector Campo Oficina.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Inés Trejo Asuaje');
-- IDx Infantil: 30004 : 40004
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 59, '63941775', 'Susana Amaya Ospina', '09/05/2021', '18/08/2024', '18:19:00', '18/08/2024', '18:19:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 39, Sector San José.' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Nora Bermúdez Ramírez');
-- IDx Infantil: 30005 : 40005
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 58, '97760442', 'Aarón Cicero Betancourt', '07/01/2021', '12/10/2024', '01:33:00', '12/10/2024', '01:33:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 95, Sector Barrio Blanco.' LIMIT 1), 'deposiciones líquidas frecuentes, deshidratación, ojos hundidos, boca seca, letargo.', 'Diarrea aguda', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gabriela Serrano Cortez');
-- IDx Infantil: 30006 : 40006
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 57, '78252408', 'Teodoro Arévalo Castañeda', '29/08/2019', '05/08/2024', '07:10:00', '05/08/2024', '07:10:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 52, Sector Campo Alegre.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Rosa Barboza Calles');
-- IDx Infantil: 30007 : 40007
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 56, '50268631', 'Valentina Velásquez Uribe', '29/01/2019', '31/10/2024', '17:52:00', '31/10/2024', '17:52:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 22, Sector Campo Alegre.' LIMIT 1), 'fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.', 'Sarampión', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elisa Lozano Montes');
-- IDx Infantil: 30008 : 40008
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 55, '38391700', 'Jesús Granados Aranda', '03/02/2020', '28/07/2025', '04:49:00', '29/07/2025', '04:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 98, Sector Las Villas.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Diana Cortez Redondo');
-- IDx Infantil: 30009 : 40009
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 54, '84590931', 'Leonardo Paz Díaz', '08/08/2018', '19/04/2024', '15:49:00', '19/04/2024', '15:49:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 81, Sector Campo Alegre.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Rita Bohorquez Chávez');
-- IDx Infantil: 30010 : 40010
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 53, '11193886', 'Génesis Prieto Carvajal', '29/12/2021', '19/10/2025', '22:18:00', '20/10/2025', '22:18:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 82, Sector Campo Alegre.' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Concepción Cicero Bustamante');
-- IDx Infantil: 30011 : 40011
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 52, '54509119', 'Victoria Galindo Briceño', '27/04/2023', '12/09/2025', '14:40:00', '12/09/2025', '14:40:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 70, Sector Campo Alegre.' LIMIT 1), 'cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.', 'Cardiopatías congénitas', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Wilmer Varela Sierra');
-- IDx Infantil: 30012 : 40012
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 51, '24757433', 'Raúl Cisneros Gutiérrez', '18/11/2018', '08/02/2024', '16:11:00', '09/02/2024', '16:11:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 53, Sector Central.' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Beatriz Lucena Baron');
-- IDx Infantil: 30013 : 40013
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 50, '58445931', 'Rigoberto Amaya Navarro', '17/10/2022', '24/10/2024', '06:50:00', '25/10/2024', '06:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 26, Sector San José.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Xiomara Fuentes Correa');
-- IDx Infantil: 30014 : 40014
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 49, '73984987', 'Luisana Arroyo García', '03/10/2019', '07/05/2025', '14:04:00', '08/05/2025', '14:04:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 33, Sector Cementerio.' LIMIT 1), 'politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.', 'Accidentes de tránsito', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gabriela Asuaje Cicero');
-- IDx Infantil: 30015 : 40015
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 48, '60741753', 'Alonso Arrate Carvajal', '23/04/2020', '22/09/2025', '14:29:00', '22/09/2025', '14:29:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 67, Sector Paraíso 2.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Valeria Cabrera Toro');
-- IDx Infantil: 30016 : 40016
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 47, '91525525', 'Lourdes Carvajal Duarte', '21/02/2020', '17/06/2024', '17:29:00', '17/06/2024', '17:29:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 1, Sector Paraíso 2.' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yolanda Fernández Guerrero');
-- IDx Infantil: 30017 : 40017
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 46, '56172766', 'Rocío Cicero Rivas', '22/10/2020', '04/09/2025', '02:30:00', '05/09/2025', '02:30:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 13, Sector Las Villas.' LIMIT 1), 'desnutrición, falta de higiene, infecciones frecuentes, retraso en el crecimiento.', 'Negligencia', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Verónica Zambrano Santana');
-- IDx Infantil: 30018 : 40018
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 45, '72843582', 'Enrique Bravo Abreu', '24/11/2021', '28/02/2025', '12:37:00', '28/02/2025', '12:37:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 78, Sector 19 de Marzo.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elisa Cardona Valencia');
-- IDx Infantil: 30019 : 40019
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 44, '66522605', 'Mercedes Caballero Vásquez', '11/04/2021', '23/03/2025', '18:08:00', '24/03/2025', '18:08:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 9, Sector 19 de Marzo.' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lidia Lara Flores');
-- IDx Infantil: 30020 : 40020
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 43, '48709665', 'Adrián Bravo Salas', '16/07/2022', '29/01/2025', '12:10:00', '30/01/2025', '12:10:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 44, Sector Los Ángeles.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Verónica Consalvi Ortiz');
-- IDx Infantil: 30021 : 40021
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 42, '16803049', 'Elisa Reyes Mora', '27/08/2022', '22/08/2025', '18:01:00', '22/08/2025', '18:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 89, Sector Valmore Rodríguez.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Xiomara Briceño Lucena');
-- IDx Infantil: 30022 : 40022
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 41, '66086435', 'Amparo Azocar Valenzuela', '31/01/2022', '10/04/2024', '19:04:00', '11/04/2024', '19:04:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 6, Sector San José.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Ángela Consalvi Colmenares');
-- IDx Infantil: 30023 : 40023
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 40, '32456642', 'Víctor Bermúdez Parra', '26/07/2023', '07/12/2025', '07:43:00', '07/12/2025', '07:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 59, Sector San José.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Oriana Duarte Olivo');
-- IDx Infantil: 30024 : 40024
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 39, '37572615', 'Daniela Izquierdo Peña', '08/06/2019', '06/01/2024', '07:21:00', '06/01/2024', '07:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 9, Sector Los Ángeles.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Rosa María Delgado Arévalo');
-- IDx Infantil: 30025 : 40025
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 38, '33101829', 'Pilar Vargas Quintero', '08/06/2021', '26/08/2024', '05:43:00', '27/08/2024', '05:43:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 29, Sector San José.' LIMIT 1), 'desnutrición, falta de higiene, infecciones frecuentes, retraso en el crecimiento.', 'Negligencia', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Julia Henríquez Zapata');
-- IDx Infantil: 30026 : 40026
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 37, '86632184', 'Sebastián Carvajal Zambrano', '06/04/2023', '23/12/2025', '03:47:00', '24/12/2025', '03:47:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 1, Sector Cementerio.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lourdes Ospina Barrios');
-- IDx Infantil: 30027 : 40027
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 36, '61065114', 'Valentín Herrera Véliz', '03/10/2019', '25/03/2025', '02:45:00', '26/03/2025', '02:45:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 33, Sector La Floresta.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yulimar Marín Ramírez');
-- IDx Infantil: 30028 : 40028
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 35, '14547002', 'Yulimar Medina Sierra', '20/12/2019', '12/11/2024', '02:30:00', '12/11/2024', '02:30:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 9, Sector Bicentenario.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mayerling Arcila Bernal');
-- IDx Infantil: 30029 : 40029
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 34, '86643230', 'René Brito Paz', '28/01/2023', '09/04/2025', '05:01:00', '09/04/2025', '05:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 99, Sector San José.' LIMIT 1), 'dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.', 'Asfixia por alimentos', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lourdes Redondo Vega');
-- IDx Infantil: 30030 : 40030
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 33, '24998417', 'René Salas Casas', '23/06/2022', '25/09/2025', '15:21:00', '26/09/2025', '15:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 45, Sector San José.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Irma Cedeno Roldán');
-- IDx Infantil: 30031 : 40031
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 32, '48354231', 'Emanuel Torres Méndez', '09/09/2019', '09/02/2024', '14:48:00', '09/02/2024', '14:48:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 97, Sector Las Villas.' LIMIT 1), 'politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.', 'Accidentes de tránsito', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Yolanda Padilla Aguilar');
-- IDx Infantil: 30032 : 40032
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 31, '84153296', 'Alonso Moreno Carvajal', '06/11/2020', '08/05/2025', '15:20:00', '08/05/2025', '15:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 83, Sector Simón Bolívar.' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Silvia Bravo Trujillo');
-- IDx Infantil: 30033 : 40033
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 30, '60500153', 'Matilde Rivera Campos', '05/05/2023', '24/05/2025', '16:55:00', '25/05/2025', '16:55:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 9, Sector Casco Central.' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Catalina Brito Causado');
-- IDx Infantil: 30034 : 40034
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 29, '85718383', 'Pedro Azocar Palacios', '02/06/2020', '10/01/2025', '20:07:00', '10/01/2025', '20:07:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 34, Sector Barrio Blanco.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Manuela Galindo Valencia');
-- IDx Infantil: 30035 : 40035
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 28, '91433236', 'Inés Báez Rivera', '10/04/2019', '30/08/2024', '19:23:00', '31/08/2024', '19:23:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 54, Sector Casco Central.' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Petra Soto Rivera');
-- IDx Infantil: 30036 : 40036
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 27, '18088241', 'Héctor Véliz Gómez', '04/02/2023', '01/05/2025', '06:00:00', '02/05/2025', '06:00:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 46, Sector Las Villas.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Gabriela Cano Colmenares');
-- IDx Infantil: 30037 : 40037
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 26, '15603676', 'Consuelo Vásquez Pereira', '29/04/2020', '12/08/2024', '23:19:00', '12/08/2024', '23:19:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 48, Sector Barrio Blanco.' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Patricia Bello Lozano');
-- IDx Infantil: 30038 : 40038
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 25, '69074516', 'Pedro Aular Mendoza', '26/12/2020', '07/08/2025', '21:52:00', '08/08/2025', '21:52:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 86, Sector Campo Oficina.' LIMIT 1), 'cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.', 'Cardiopatías congénitas', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mayerling Valera Caraballo');
-- IDx Infantil: 30039 : 40039
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 24, '76133708', 'Luisana Zambrano Romero', '22/12/2020', '20/04/2024', '14:01:00', '20/04/2024', '14:01:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 74, Sector Las Villas.' LIMIT 1), 'fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.', 'Malaria', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Concepción Trujillo Méndez');
-- IDx Infantil: 30040 : 40040
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 23, '37831344', 'Roberto Gutiérrez Véliz', '10/12/2018', '23/07/2024', '14:11:00', '23/07/2024', '14:11:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 50, Sector San José.' LIMIT 1), 'vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.', 'Intoxicaciones accidentales', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Francisca García Núñez');
-- IDx Infantil: 30041 : 40041
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 22, '23419728', 'Alicia Guerrero Gómez', '04/09/2020', '01/07/2025', '18:53:00', '01/07/2025', '18:53:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 28, Sector Cementerio.' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Elena Barrios Cerrada');
-- IDx Infantil: 30042 : 40042
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 21, '81420543', 'Ninoska Barboza Galindo', '13/11/2018', '17/04/2024', '04:17:00', '17/04/2024', '04:17:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 75, Sector Las Malvinas.' LIMIT 1), 'fiebre, tos, dificultad respiratoria, aleteo nasal, retracciones intercostales, cianosis.', 'Neumonía', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Juana Bello Cordero');
-- IDx Infantil: 30043 : 40043
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 20, '80075610', 'Irma Moreno Moreno', '01/09/2020', '27/02/2025', '15:09:00', '27/02/2025', '15:09:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 20, Sector La Floresta.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Susana López Campo');
-- IDx Infantil: 30044 : 40044
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 19, '30952539', 'Elena Cano Rojas', '02/03/2019', '27/06/2024', '10:52:00', '28/06/2024', '10:52:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 9, Sector Simón Bolívar.' LIMIT 1), 'desnutrición, falta de higiene, infecciones frecuentes, retraso en el crecimiento.', 'Negligencia', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lismar Gil Baron');
-- IDx Infantil: 30045 : 40045
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 18, '24501213', 'David Cisneros Mendoza', '14/08/2019', '10/05/2024', '23:46:00', '10/05/2024', '23:46:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 97, Sector Central.' LIMIT 1), 'hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.', 'Caídas graves', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Francisca Peraza Molina');
-- IDx Infantil: 30046 : 40046
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 17, '85172994', 'Rubén Casas Palma', '14/07/2019', '18/12/2024', '01:21:00', '19/12/2024', '01:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 98, Sector Casco Central.' LIMIT 1), 'desnutrición, falta de higiene, infecciones frecuentes, retraso en el crecimiento.', 'Negligencia', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Antonieta Ortiz Castro');
-- IDx Infantil: 30047 : 40047
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 16, '28573822', 'Lismar Salinas Lozano', '15/09/2018', '16/06/2024', '10:39:00', '16/06/2024', '10:39:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 87, Sector 19 de Marzo.' LIMIT 1), 'palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.', 'Cáncer infantil', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Adriana Ortega Carvajal');
-- IDx Infantil: 30048 : 40048
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 15, '26017510', 'Noelia Navia Pereira', '21/10/2020', '29/07/2024', '14:20:00', '29/07/2024', '14:20:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 86, Sector Casco Central.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Emma Urdaneta Guerra');
-- IDx Infantil: 30049 : 40049
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 14, '16019722', 'Valeria Navia Bohorquez', '14/08/2022', '04/07/2025', '19:22:00', '05/07/2025', '19:22:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 1, Sector Cementerio.' LIMIT 1), 'hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.', 'Violencia doméstica', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Jimena Palacios Prieto');
-- IDx Infantil: 30050 : 40050
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 13, '75209838', 'Yulimar Aguilar Zapata', '06/05/2022', '05/05/2025', '00:56:00', '06/05/2025', '00:56:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 6, Sector Campo Alegre.' LIMIT 1), 'emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.', 'Desnutrición aguda severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Verónica Alvarado Núñez');
-- IDx Infantil: 30051 : 40051
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 12, '84383442', 'Andrés Cano Carvajal', '11/09/2020', '30/07/2024', '02:18:00', '31/07/2024', '02:18:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 12, Sector Las Malvinas.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Laura Flores Hernández');
-- IDx Infantil: 30052 : 40052
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 11, '17590798', 'Leonardo Pinto Briceño', '28/02/2022', '27/12/2024', '14:54:00', '27/12/2024', '14:54:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 37, Sector Campo Oficina.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Juana Bautista Urdaneta');
-- IDx Infantil: 30053 : 40053
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 10, '17656234', 'Juana Cruz Paz', '20/06/2019', '29/09/2024', '09:21:00', '29/09/2024', '09:21:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 73, Sector Cementerio.' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Marta Zambrano Borjas');
-- IDx Infantil: 30054 : 40054
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 9, '82611251', 'Enrique Cruz Montes', '16/02/2023', '31/03/2025', '10:36:00', '31/03/2025', '10:36:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 35, Sector Paraíso 2.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Teresa Marcano Arroyo');
-- IDx Infantil: 30055 : 40055
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 8, '94506087', 'Alonso Soto Blanco', '28/10/2021', '06/08/2024', '14:12:00', '07/08/2024', '14:12:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 67, Sector Campo Alegre.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Mariana Lucena Suárez');
-- IDx Infantil: 30056 : 40056
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 7, '62721418', 'Andrés Mora Montes', '22/03/2021', '28/09/2024', '09:30:00', '29/09/2024', '09:30:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 95, Sector Pueblo Nuevo Sur.' LIMIT 1), 'tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.', 'Tuberculosis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Dolores Delgado Vásquez');
-- IDx Infantil: 30057 : 40057
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 6, '91435945', 'Maximiliano Maldonado Rivas', '20/08/2021', '08/02/2024', '10:05:00', '08/02/2024', '10:05:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 57, Sector Casco Central.' LIMIT 1), 'pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.', 'Ahogamiento', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Isabel Baron Rojas');
-- IDx Infantil: 30058 : 40058
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 5, '55281728', 'Olivia Valera Rivera', '02/11/2020', '10/07/2024', '10:28:00', '11/07/2024', '10:28:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 69, Sector 19 de Marzo.' LIMIT 1), 'pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.', 'VIH/SIDA', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Claudia Cantillo Yánez');
-- IDx Infantil: 30059 : 40059
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 4, '25731668', 'Hugo Brito Cerrada', '06/01/2021', '02/10/2025', '01:38:00', '03/10/2025', '01:38:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 15, Sector Las Malvinas.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Marta Valdez Abreu');
-- IDx Infantil: 30060 : 40060
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 3, '27615743', 'Isaac Bernal Zambrano', '27/05/2020', '17/07/2024', '22:35:00', '18/07/2024', '22:35:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Avenida 54, Sector Pedro Camejo.' LIMIT 1), 'dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.', 'Asma severa', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Valentina Casas Moreno');
-- IDx Infantil: 30061 : 40061
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 2, '38815824', 'Lourdes Zapata Marques', '11/02/2021', '05/04/2025', '20:50:00', '06/04/2025', '20:50:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Carrera 30, Sector Pedro Camejo.' LIMIT 1), 'deposiciones líquidas frecuentes, deshidratación, ojos hundidos, boca seca, letargo.', 'Diarrea aguda', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Silvia Lozano Vega');
-- IDx Infantil: 30062 : 40062
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 1, '53839091', 'Miriam Baron Valencia', '18/12/2022', '20/12/2024', '13:08:00', '20/12/2024', '13:08:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 78, Sector 19 de Marzo.' LIMIT 1), 'fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.', 'Sepsis', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Alicia Ruiz Ibarra');
-- IDx Infantil: 30063 : 40063
INSERT INTO mortalidad (id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, idx_defuncion, fecha_registro_formulario) VALUES ((SELECT MAX(id_paciente) FROM persona_paciente) - 0, '41377578', 'Tomás Peraza Ibarra', '16/07/2020', '22/01/2025', '23:59:00', '22/01/2025', '23:59:00', (SELECT id_direccion FROM direccion WHERE descripcion = 'Calle 98, Sector Campo Oficina.' LIMIT 1), 'dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.', 'Quemaduras', '2026-02-11');
INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (LAST_INSERT_ROWID(), 'Lidia Arismendi Montes');
-- IDx Infantil: 30064 : 40064
COMMIT;

-- TOTAL DE REGISTROS DE MORTALIDAD INFANTIL GENERADOS: 65
-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.
