---
titulo: "Yankuilotl: empresa estatal de innovación"
tipo: analisis
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-009, F-018, F-019, F-020, F-040, F-041, F-042, F-043]
tags: [femeci, semiconductores, yankuilotl, actores, fase-3]
aliases: ["Yankuilotl", "Yankuilot"]
---

# Yankuilotl: empresa estatal de innovación

> [!summary] En corto
> Empresa paraestatal de Puebla creada en julio de 2025 y sectorizada a la SECIHTI. Desde abril de 2026 opera una **casa de ensamble de tarjetas electrónicas** (líneas SMT y through-hole, cuarto limpio clase 1000), tiene una **fábrica de software** y opera el **sistema de bicicleta pública**. En septiembre de 2026 el gobernador anunció que en 2027 también **fabricará tarjetas PCB**. Es el actor del ecosistema "semiconductores" más cercano a un proceso de manufactura real en Puebla, y la UTP aparece como universidad participante. (La forma correcta del nombre es *Yankuilotl*.)

## 1. Datos institucionales

| Dato | Valor | Fuente | Tipo |
|---|---|---|---|
| Creación | Decreto publicado el 15 jul 2025; paraestatal con mayoría estatal | F-018 | Prensa |
| Sectorización | SECIHTI Puebla; "brazo ejecutor" de la política de innovación | F-009, F-018 | Oficial / prensa |
| Presupuesto inicial | 67 millones de pesos el primer año | F-018 | Prensa |
| Objeto | "Impulsar el desarrollo tecnológico, fomentar la formación de talento especializado y la transferencia de conocimiento, así como propiciar la elaboración de patentes" | F-018 | Prensa |
| Director general | Lagtzú López Miro Castorena | F-040 | Oficial |
| Director de Tecnología | Daniel Antonio Gutiérrez | F-042 | Prensa |
| Laboratorio de Electrónica y Prototipos | A cargo de Argel Vega Alonzo | F-042 | Prensa |
| Apoyo federal | Subsecretaría de Desarrollo Tecnológico, Vinculación e Innovación | F-040 | Oficial |
| Universidades | "Reúne, por primera vez, a universidades públicas y privadas" (SECIHTI); en prensa se mencionan BUAP, UTP, UPAEP y Tecnológico de Monterrey; también se menciona a la Universidad Rosario Castellanos | F-042, F-019, F-043 | Prensa |

## 2. Casa de ensamble de tarjetas electrónicas

| Dato | Valor | Fuente | Tipo |
|---|---|---|---|
| Inicio de operación | "Hace tres meses" al 13 jul 2026 (≈ abril 2026) | F-040 | Oficial |
| Infraestructura | "Cuarto Limpio Clase 1000" | F-040 | Oficial |
| Capacidad | Hasta 200,000 componentes por hora con SMT y 40,000 con through-hole | F-041, F-042 | Sitio del gobernador / prensa |
| Proceso descrito | "Diseño del plano constructivo de la tarjeta electrónica", "distribución física de los componentes", "etapa de validación"; después "empastado, colocación de componentes y soldadura" | F-041 | Sitio del gobernador |
| Validación antes de producir en serie | Proceso "para verificar interconexiones y garantizar el funcionamiento antes de iniciar la producción en serie" | F-020 | Prensa |
| Programación por proyecto | "Cada proyecto requiere una programación específica para configurar las máquinas de ensamblaje" (Director de Tecnología) | F-042 | Prensa |
| Productos | Tarjetas para televisores, celulares, tabletas, electrodomésticos, equipo ferroviario, drones, tractores y sembradoras de precisión | F-041, F-042 | Sitio del gobernador / prensa |
| Relación con Kutsari | Ensambla tarjetas y "participa en su diseño en coordinación con el proyecto federal Kutsari, responsable del diseño de los chips" | F-042 | Prensa |
| Demanda | "Ya están saturados por la demanda" (gobernador, 28 sep 2026) | F-043 | Prensa |
| Siguiente paso | Primera fábrica estatal de **tarjetas PCB** (tarjeta desnuda) en 2027, con presupuesto ya previsto | F-043 | Prensa |
| Ubicación | Instalaciones en la "Capital de la Tecnología y Sustentabilidad"; fábrica de bicicletas junto a Kutsari Puebla; planta de mantenimiento en Cuautlancingo | F-041, F-043 | Por confirmar |

> [!warning] Cifra que hay que leer con cuidado
> En un discurso se habló de "200 mil tarjetas electrónicas PCB por hora" [F-043]. La descripción técnica habla de **200 mil componentes por hora** [F-041, F-042], que es la velocidad nominal de colocación de las máquinas SMT, no tarjetas terminadas. Usar la cifra técnica.

## 3. Fábrica de software y movilidad

- `#hecho` 30 especialistas previstos, 20 contratados al 13 jul 2026; soluciones para servicios públicos y transformación digital [F-040].
- `#hecho` Desarrolla aplicaciones, plataformas y sitios web (incluido el de la Feria de Puebla), y la modernización del catastro y del Registro Público de la Propiedad [F-042].
- `#hecho` Plataforma de la bicicleta pública al 90 %, con acceso por celular, tarjeta o código QR integrado con el transporte por cable, las ciclovías y la RUTA [F-040, F-042].

## 4. Lecturas (`#inferencia`)

1. **Planta nueva, mezcla alta y demanda saturada**: programación específica por proyecto, muchos tipos de producto y validación previa sugieren producción de **alta mezcla y bajo volumen**, donde la preparación de cada producto y la inspección suelen ser cuellos de botella. Es una hipótesis que hay que confirmar en la entrevista.
2. **Inspección no descrita**: ninguna fuente menciona inspección óptica automatizada, rayos X ni pruebas eléctricas. No sabemos si inspeccionan a mano, con máquina o con ambos.
3. **Through-hole**: las uniones through-hole se sueldan del lado inferior y suelen requerir inspección distinta a la de SMT; si Yankuilotl usa soldadura manual u ola, podría haber un hueco de inspección. Hipótesis por verificar.
4. **Cuarto limpio clase 1000** para ensamble de tarjetas es poco común; puede reflejar planes de manejo de chips desnudos o requisitos de clientes. Preguntar.
5. **Acceso**: la presencia de universidades (incluida la UTP) y el objetivo de retener talento hacen plausible una colaboración estudiantil.

## 5. Preguntas abiertas

Ver [[guia-contacto-yankuilotl]] y Q-028 y Q-034 a Q-037 en [[preguntas-pendientes]].
