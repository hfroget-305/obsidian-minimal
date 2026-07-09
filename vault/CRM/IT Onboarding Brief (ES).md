---
type: brief
audience: Especialista de TI (nueva incorporación, sin contexto del negocio)
status: documento vivo
tags:
  - crm
  - onboarding
---

# Guía de Incorporación de TI — El Sistema de Experiencia del Cliente

Bienvenido/a. Este documento explica, desde cero, el negocio que vas a apoyar,
el sistema que hemos construido, cómo se ve el producto "terminado" y dónde
entras tú. Léelo completo una vez; después te servirá como referencia.

---

## 1. El negocio en un párrafo

Vendemos a clientes que normalmente empiezan como **leads** (alguien que podría
comprar), se convierten en **clientes** (alguien que compró) y — cuando los hemos
atendido bien — se convierten en **referidores** (clientes que nos traen nuevos
leads). Ese último paso importa más que cualquier otro: un lead referido cuesta
menos ganarlo y es más leal que cualquier lead que podamos comprar con
publicidad. Así que todo el sistema que estás a punto de conocer existe para
responder una sola pregunta, continuamente: **"¿En qué punto del recorrido está
cada persona, y qué es lo próximo que le debemos?"**

## 2. La filosofía: archivos, no un CRM SaaS

Deliberadamente **no** usamos software tipo Salesforce/HubSpot. El sistema es
una carpeta de archivos de texto plano:

- Cada lead, cliente, referido e interacción es un **archivo Markdown** (`.md`)
  — un archivo de texto que puedes abrir en el Bloc de notas, buscar con grep,
  respaldar y versionar.
- Los datos estructurados (estado, fechas, montos) viven en un pequeño bloque de
  **frontmatter YAML** al inicio de cada archivo — pares clave: valor legibles
  por máquina.
- Las relaciones ("este referido vino de aquel cliente") son **wikilinks** —
  `[[Globex]]` en un archivo apunta al archivo llamado `Globex.md`.
- Vemos y editamos estos archivos en **[Obsidian](https://obsidian.md)** — una
  aplicación de escritorio gratuita que trata una carpeta ("bóveda" o *vault*)
  de archivos Markdown como una base de conocimiento enlazada, y añade tres
  superpoderes de los que dependemos:
  - **Bases** (archivos `.base`): vistas de base de datos en vivo sobre los
    archivos — piensa en "consultas SQL guardadas renderizadas como tablas",
    definidas en YAML.
  - **Canvas** (archivos `.canvas`): pizarras visuales, guardadas como JSON plano.
  - **Backlinks**: abre el archivo de cualquier cliente y ve todos los archivos
    que lo enlazan — el historial completo de la relación sin configurar nada.

**Por qué te importa como persona de TI:** no hay servidor de base de datos, no
hay dependencia de un proveedor, no hay claves de API que cuidar para el sistema
central. La "base de datos" es un repositorio Git de archivos de texto. Todo lo
que sabes de archivos, Git y CI aplica directamente.

## 3. La arquitectura de tres capas

```text
┌────────────────────────────────────────────────────────────┐
│ Capa 3 · LOS DATOS (vault/CRM/)                            │
│ Registros de Lead, Cliente, Referido, Interacción + vistas │  ← aquí vive el negocio
├────────────────────────────────────────────────────────────┤
│ Capa 2 · LAS HABILIDADES DE IA (skills/, .claude-plugin/)  │
│ Enseñan a los agentes de IA a leer/escribir nuestros       │
│ formatos de archivo                                        │  ← aquí vive el apalancamiento
├────────────────────────────────────────────────────────────┤
│ Capa 1 · LA FONTANERÍA (.github/workflows/)                │
│ Repo Git, CI, sincronización semanal, bots de revisión     │  ← esto es tuyo
└────────────────────────────────────────────────────────────┘
```

### Capa 1 — Fontanería (tu terreno)

- **El repo de GitHub** `hfroget-305/obsidian-minimal` contiene todo.
- **`sync-obsidian-skills.yml`**: una GitHub Action que corre cada lunes,
  revisa las definiciones de habilidades de código abierto
  ([kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)) y abre
  un pull request cuando cambian. Tiene timeout de 10 minutos, no persiste
  credenciales y falla ruidosamente si su paso de reescritura deja de coincidir.
- **CodeRabbit** revisa cada PR automáticamente. Nada llega a `master` sin
  pasar revisión.

### Capa 2 — Habilidades de IA (el apalancamiento)

`skills/` contiene cinco conjuntos de instrucciones ("Agent Skills") que enseñan
a los agentes de IA (Claude Code y herramientas compatibles) a trabajar
correctamente con nuestros formatos: Markdown de Obsidian, sintaxis de Bases,
JSON Canvas, la CLI de Obsidian y una herramienta de captura web (Defuddle).
Gracias a ellas, un agente de IA puede crear un archivo de lead correctamente
estructurado, actualizar una vista del panel o redibujar el canvas del recorrido
a petición — todo este CRM se construyó así. Trata las habilidades como
dependencias vendorizadas: la sincronización del lunes las mantiene al día; tú
revisas el PR.

### Capa 3 — Los datos (el negocio)

`vault/CRM/` es el producto. Cuatro **tipos de registro**, cada uno con plantilla:

| Registro | Un archivo por… | Campos clave | Ciclo de vida (`status`) |
|---|---|---|---|
| **Lead** | cliente potencial | `source`, `referrer`, `value`, `last_contact`, `next_action`, `next_action_date` | new → contacted → qualified → proposal → won/lost |
| **Cliente** | cliente que paga | `health` (green/yellow/red), `nps` (0–10), `last_contact`, `referrals_given` | onboarding → active ⇄ at-risk → churned |
| **Referido** | evento de referencia | `referrer` → archivo del cliente, `referred` → archivo del lead, `reward` | invited → contacted → converted/lost |
| **Interacción** (Touchpoint) | interacción | `about` → con quién, `channel`, `sentiment`, `follow_up` | — (registro solo-añadir) |

Más dos instrumentos sobre esos registros:

- **`Dashboards/CRM Dashboard.base`** — seis vistas en vivo: Pipeline de Leads
  (agrupado por etapa, valor del pipeline sumado), **Seguimientos Vencidos**
  (todo lo atrasado), Clientes (promedio de NPS), **En Riesgo** (salud roja o
  amarilla *o* más de 30 días de silencio — nuestra alerta temprana de fuga),
  Referidos, Interacciones Recientes.
- **`Customer Experience Flow.canvas`** — el mapa visual del recorrido:
  Atraer → Convertir → Entregar → Deleitar y Referir, con el **volante de
  referidos** (los promotores alimentan nuevos leads) y un **ciclo de mejora
  continua** (recuperación de detractores, análisis de razones de pérdida,
  revisión semanal).

El ritmo operativo es una **revisión semanal de 20 minutos** documentada en
`CRM Home.md`: poner a cero los seguimientos vencidos → una acción por cada
cliente en riesgo → dar seguimiento a los referidos → detectar patrones en las
razones de pérdida → implementar una mejora pequeña.

## 4. El producto terminado — cómo se ve "listo"

La meta final es un sistema donde **los humanos solo hacen el trabajo de
criterio** (hablar con la gente, evaluar la salud, decidir acciones) y **todo lo
mecánico está automatizado**. En concreto, el producto terminado tiene cinco
propiedades:

1. **Fontanería que se mantiene sola.** Las dependencias se actualizan solas
   mediante PRs revisados (✅ ya en marcha: la sincronización del lunes). Los
   respaldos son automáticos (historial de Git + una copia externa). Nada se
   pudre en silencio — todo trabajo automatizado falla ruidosamente.

2. **Captura de registros sin tocar nada.** Un lead nuevo nunca se escribe a
   mano (🔶 primeras vías en marcha: formulario de issue, ejecución manual y
   despacho por API → PR con el archivo del lead vía `crm-lead-intake.yml`;
   falta el vigilante de correo):
   - Formulario web / correo entrante → aparece un archivo de lead con el
     formato correcto en `CRM/Leads/` con `status: new` y la fecha de hoy,
     mediante una pequeña automatización (GitHub Action, flujo de n8n o un
     script que vigile un buzón — tú decides).
   - Las interacciones de correo/calendario se registran como archivos de
     Interacción de la misma manera.

3. **El sistema nos avisa; nosotros nunca lo consultamos.** Hoy el panel
   muestra los seguimientos vencidos cuando lo abrimos; terminado significa que
   **empuja**: un resumen los lunes (correo o mensaje de chat) generado desde
   los mismos datos — acciones vencidas, clientes en riesgo, recompensas de
   referidos pendientes. Un trabajo programado lee el frontmatter (es solo
   YAML — trivial de parsear) y da formato al resumen.

4. **Métricas de experiencia con historial, no solo una foto del momento.** Un
   trabajo mensual de instantáneas añade las cifras clave (valor del pipeline
   por canal, promedio de NPS, tasa de conversión de referidos, días promedio
   hasta el primer contacto) a una nota de métricas, para que las tendencias se
   vuelvan visibles. Eso es lo que significa "mejorar constantemente la
   experiencia" de forma medible: tiempos de respuesta bajando, NPS subiendo,
   el volante girando.

5. **Operación asistida por IA.** Gracias a la Capa 2, el trabajo rutinario se
   delega en lenguaje natural: "registra una interacción de la llamada de hoy
   con Globex, sentimiento positivo, seguimiento el próximo martes" o "redacta
   la revisión semanal". Las habilidades garantizan que el resultado llegue con
   el formato correcto, a la carpeta correcta.

## 5. Tus primeros 90 días (hoja de ruta propuesta)

| Fase | Entregable | Notas |
|---|---|---|
| **Semanas 1–2 · Aprender y endurecer** | Ejecuta tú mismo/a la revisión semanal una vez; configura el respaldo externo del repo; verifica el flujo del PR de sincronización del lunes | No puedes automatizar un proceso que no has hecho a mano |
| **Semanas 3–6 · Automatizar la captura** | Pipeline formulario/correo → archivo de lead; interacción → archivo de touchpoint | El punto de mayor apalancamiento; elimina la mayor parte de la escritura manual |
| **Semanas 7–10 · Notificaciones push** | Trabajo del resumen del lunes (vencidos / en riesgo / recompensas pendientes) | Leer frontmatter, dar formato, enviar — que sea aburrido y confiable |
| **Semanas 11–13 · Historial de métricas** | Trabajo mensual de instantáneas + nota de tendencias | Permite juzgar el ciclo de mejora con números |
| **Continuo** | Revisar los PRs de sincronización; mantener las automatizaciones en verde; proponer una mejora de proceso al mes | Eres participante del ciclo de mejora, no solo su fontanero/a |

## 6. Reglas de juego

- **El texto plano es sagrado.** Cualquier automatización que construyas lee y
  escribe Markdown + frontmatter YAML en este repo. Nada de bases de datos en
  la sombra, nada de datos que existan solo dentro de una herramienta de terceros.
- **Todo pasa por PRs.** Las automatizaciones hacen commit a ramas y abren PRs,
  igual que los humanos y el bot de sincronización. La revisión es la red de
  seguridad.
- **Fallar ruidosamente.** Una automatización rota en silencio es peor que no
  tener automatización — sigue el patrón de `sync-obsidian-skills.yml`
  (timeouts, verificaciones explícitas).
- **El cliente nunca nota el sistema.** Solo experimenta respuestas rápidas,
  contexto recordado y agradecimientos que llegan a tiempo. Ese es el producto.

## 7. Dónde vive cada cosa

| Qué | Dónde |
|---|---|
| Esta guía (inglés) | `vault/CRM/IT Onboarding Brief.md` |
| Esta guía (español) | `vault/CRM/IT Onboarding Brief (ES).md` |
| Hub del sistema + ritual semanal | `vault/CRM/CRM Home.md` |
| Mapa visual del recorrido | `vault/CRM/Customer Experience Flow.canvas` |
| Panel en vivo (6 vistas) | `vault/CRM/Dashboards/CRM Dashboard.base` |
| Plantillas de registros | `vault/CRM/Templates/` |
| Registros de ejemplo | `vault/CRM/{Leads,Customers,Referrals,Touchpoints}/` |
| Definiciones de habilidades de IA | `skills/` + `.claude-plugin/` |
| Sincronización semanal de dependencias | `.github/workflows/sync-obsidian-skills.yml` |
| Fuente original de las habilidades | https://github.com/kepano/obsidian-skills |

Las preguntas que este documento no respondió son errores de este documento —
corrígelo mediante un PR.
