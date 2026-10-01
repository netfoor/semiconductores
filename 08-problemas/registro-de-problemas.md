---
titulo: "Registro de problemas documentados"
tipo: registro
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-011, F-014, F-019, F-020, F-031, F-032, F-033, F-034, F-035, F-036]
tags: [femeci, problemas, fase-2]
aliases: ["Problemas documentados"]
---

# Registro de problemas documentados

Problemas de Puebla con evidencia pública encontrados en la Fase 2. **Esto no es una selección de proyecto**: es el inventario del que saldrán las hipótesis de la Fase 5. Cada problema indica su nivel de evidencia y qué falta saber. Plantilla de ficha detallada: [[indice-problemas]].

**Nivel de evidencia:** **Alto** = fuente oficial con cifras recientes · **Medio** = fuente oficial sin cifras o prensa que cita a autoridades · **Bajo** = iniciativa documentada, pero problema técnico aún no descrito públicamente.

## Resumen

| ID | Problema | Sector / categoría FEMECI probable | Evidencia | Actualidad |
|---|---|---|---|---|
| P-001 | Descargas contaminantes irregulares al río Atoyac difíciles de detectar | Ambiental / Ciencias Ambientales o Sistemas (IoT) | Media-alta | 2025–2026 |
| P-002 | Inundaciones y deslaves en la Sierra Norte; compromiso de fortalecer pronóstico y alertamiento | Riesgo / Ciencias Ambientales | Alta (daño) · Media (alertamiento) | oct 2025 |
| P-003 | Riesgo por cenizas del Popocatépetl y necesidad de monitoreo | Riesgo / Ciencias Ambientales | Media | 2026 |
| P-004 | Brecha de talento en manufactura 4.0, calidad, automatización y software en la cadena automotriz | Industria / Ingenierías o Sistemas | Media-alta | 2025 |
| P-005 | Construcción de capacidades en electrónica y semiconductores: validación, pruebas y calidad en procesos nuevos | Industria emergente / Sistemas o Ingenierías | Baja (problema técnico no descrito aún) | 2026 |
| P-006 | Informalidad alta y baja digitalización de MIPyMES | Economía / Ciencias Sociales o Sistemas | Media | 2024–2025 |
| P-007 | Capacidades técnicas agrícolas limitadas y residuos agroindustriales (bagazo de mezcal) | Agro / Agroindustria o Ambientales | Media | 2025–2026 |

## P-001 · Descargas irregulares al río Atoyac

- `#hecho` Según datos de CONAGUA difundidos por la Presidencia, hay 1,095 descargas irregulares identificadas y un aumento de 160 % entre marzo y diciembre de 2025; 2,850 descargas ilegales detectadas en el Atoyac y el Zahuapan frente a 572 permisos; 250 plantas de tratamiento, 87 fuera de operación [F-032].
- `#hecho` Industria textil y de mezclilla predominan en zonas críticas (entre ellas San Martín Texmelucan y San Miguel Xoxtla en Puebla; Tepetitla de Lardizábal y Nativitas en Tlaxcala) [F-032].
- `#hecho` Limitación técnica reconocida: las empresas "le dan vuelta a la autoridad" y suspenden la descarga cuando detectan inspectores; "la Conagua está adquiriendo los equipos para empezar los monitoreos de la calidad"; la vigilancia es por brigadas, sin mención de monitoreo continuo [F-032].
- `#hecho` (pendiente de leer) Otras notas de 2026 reportan 4,900 descargas en la cuenca, señalamientos presidenciales a textileras y multas por 56 millones de pesos (ver fuentes pendientes en [[registro-de-fuentes]]).
- **Qué falta saber:** qué parámetros se miden, con qué frecuencia, qué tecnología usa o planea usar CONAGUA, quién es el usuario de un posible sistema.
- **Implicación (`#inferencia`):** problema real, actual y con un hueco técnico explícito (detección de eventos intermitentes). La evidencia proviene de prensa que cita a autoridades; hay que llegar al documento oficial.

## P-002 · Inundaciones y deslaves en la Sierra Norte

- `#hecho` Cifras oficiales al 28 oct 2025: 22 personas fallecidas, más de 64 mil afectadas, 11 mil viviendas censadas [F-033].
- `#hecho` Al 20 oct 2025, el gobernador reportó 23 municipios afectados, 404 deslaves, 11 puentes destruidos y 134.8 km de caminos dañados, y enumeró entre los ejes de respuesta el "fortalecimiento del sistema de pronóstico y alertamiento para prevenir futuros riesgos" [F-034, cita del gobernador en prensa].
- **Qué falta saber:** qué sistema de pronóstico y alertamiento existe, qué se planea fortalecer y quién lo opera.
- **Implicación (`#inferencia`):** el problema es grave y reconocido por el gobierno. Un proyecto aquí tendría que mostrar claramente qué aporta frente a lo que ya existe y si hay continuidad con trabajos previos de los integrantes (reglas de originalidad, FE-07).

## P-003 · Cenizas del Popocatépetl

- `#hecho` El nanosatélite Gxiba-1 (UPAEP, con la agencia espacial japonesa) busca "generar información científica útil para la gestión de riesgos y la protección de la población" monitoreando cenizas volcánicas [F-036].
- **Qué falta saber:** qué monitoreo existe en tierra y qué necesidades no cubre.
- **Implicación (`#inferencia`):** el tema ya tiene un proyecto estudiantil de alto perfil reconocido por el estado; la originalidad sería un reto.

## P-004 · Talento para manufactura 4.0 en la cadena automotriz

- `#hecho` Gobierno, BID y Clúster Automotriz Zona Centro acordaron 107 paquetes de formación en "manufactura 4.0, tecnología y desarrollo; calidad y procesos; sostenibilidad y seguridad; logística, software y automatización" para alinear "las capacidades del talento humano con demandas del sector"; el sector emplea a más de 55 mil personas [F-031].
- **Qué falta saber:** qué problemas operativos concretos (calidad, inspección, trazabilidad) motivan esa formación y si un proveedor aceptaría compartir datos.
- **Implicación (`#inferencia`):** el problema documentado es de talento, no de una tecnología específica; un proyecto técnico aquí necesitaría evidencia adicional de un proveedor.

## P-005 · Capacidades en electrónica y semiconductores

- `#hecho` Hay iniciativas activas: laboratorios de caracterización y validación de circuitos integrados (Kutsari, mayo 2026) [F-011]; planta de ensamble de tarjetas de Yankuilotl con validación de diseño "para verificar interconexiones y garantizar el funcionamiento antes de iniciar la producción en serie" (julio 2026) [F-019, F-020].
- `#hecho` El objetivo declarado incluye retener talento especializado y "evitar la fuga de cerebros" [F-020].
- **Qué falta saber (Fase 3):** qué problemas técnicos tienen hoy estas operaciones (defectos, inspección, pruebas, trazabilidad, rendimiento), cómo se resuelven y qué datos existen.
- **Implicación (`#inferencia`):** alta alineación con la política del organizador, pero **todavía no hay un problema técnico documentado**: la hipótesis de semiconductores sigue abierta.

## P-006 · Informalidad y digitalización de MIPyMES

- `#hecho` 70.7 % de la población ocupada en la informalidad (ENOE 2024); el plan propone "transformación digital para MIPyMES" [F-014, lectura automatizada].
- **Implicación (`#inferencia`):** problema amplio y estructural; difícil de convertir en un prototipo con experimento cuantitativo en 29 días.

## P-007 · Capacidades agrícolas y residuos agroindustriales

- `#hecho` El plan reconoce "escaso desarrollo de capacidades técnicas en procesos productivos" del campo [F-014]; SECIHTI trabaja con 11 cooperativas un diagnóstico para una bioplanta que transforme residuos de mezcal en bioplásticos y biocombustibles [F-035].
- **Implicación (`#inferencia`):** alineado con el enfoque territorial del organizador; requiere competencias químicas o biológicas que no son el núcleo del equipo.

## Próximos pasos

- Fase 3: profundizar P-005 (eslabones, empresas, procesos, problemas técnicos documentados).
- Fase 5: llevar a la matriz de comparación los problemas con evidencia media o alta y crear fichas `P-###` completas para los finalistas.
