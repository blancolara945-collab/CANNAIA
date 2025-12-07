# Referencias de proyectos similares

Este documento resume proyectos y comunidades que ya han trabajado en automatización de cultivos y control ambiental. La idea es extraer prácticas que aceleren a Doctor Cañamo y evitar errores comunes.

## Panorama rápido

| Proyecto/comunidad | Qué resuelve | Lecciones para Doctor Cañamo |
| --- | --- | --- |
| **Home Assistant + Tuya/SmartLife** | Orquestación de dispositivos de clima e iluminación doméstica con automatizaciones declarativas (YAML) y plantillas. | Modelo de integraciones modulares y repositorio de "blueprints" reutilizables; validaciones de seguridad por dispositivo; modo manual/automático con overrides. |
| **FarmBot (open-source)** | Robot CNC para siembra y riego de huertos. Telemetría, control remoto y planeación de riegos. | Telemetría detallada de cada acción, simulación previa a ejecutar, límites físicos para evitar daños; UI web con historial de comandos y estado de actuadores. |
| **Controladores hidropónicos comerciales (p. ej., unidades todo-en-uno de nutrientes/clima)** | Dosificación automática de nutrientes, control de pH/EC y clima en armarios cerrados. | Bucles cerrados con límites duros de seguridad, alarmas redundantes (app + email), calibración frecuente de sondas y mantenimiento guiado. |
| **OpenAg / Personal Food Computer (MIT)** | Cámaras de cultivo cerradas con recetas climáticas reproducibles y dataset abierto. | Concepto de "receta" de ambiente versionada; compartición de datos para mejorar modelos; importancia de la mantenibilidad (el proyecto falló por costos/operación). |
| **Comunidades DIY (r/AutomatedHydroponics, foros ESPHome)** | Sensado barato (EC, pH, T/H), dashboards caseros y riegos programados. | Kits de calibración baratos, redundancia de sensores, almacenamiento local (SD/SQLite) cuando no hay nube, guías paso a paso para montaje. |

## Ideas accionables para el roadmap

1. **Recetas versionadas de cultivo**: definir perfiles (germinación, crecimiento, floración) con rangos objetivo de pH/EC/T/H y tasas de cambio aceptables. Almacenar versiones y variaciones por cultivar.
2. **Blueprints de automatización**: inspirarse en Home Assistant para publicar plantillas YAML/JSON de reglas (p. ej., "si humedad < 45% y luz encendida → activar humidificador 5 min") que los usuarios puedan copiar y ajustar.
3. **Telemetría y replay de acciones**: registrar cada comando enviado (Growee/SmartLife), el estado previo y posterior, y permitir reproducir secuencias en modo simulación antes de aplicar.
4. **Gestión de seguridad**: límites duros y suaves, ventanas de mantenimiento para evitar dosificar mientras se calibra, y notificaciones redundantes. Bloqueo automático si un sensor queda sin calibrar por más de N días.
5. **Calibración guiada y tracking de sondas**: checklist interactivo para calibrar pH/EC, registro de fecha de calibración, drifts observados y alerta cuando toca recalibrar o reemplazar sondas.
6. **Etiquetado de imágenes con asistencia**: flujo de etiquetado semiautomático (modelo ligero + confirmación humana) para clasificar carencias y generar dataset propio. Versionar los sets de entrenamiento.
7. **Fallback offline**: buffer local de datos y reglas mínimas cuando no hay conectividad; sincronización diferida al recuperar red.
8. **Dashboards compartibles**: exportar vistas web ligeras con últimos diagnósticos/acciones para consultores o cultivadores externos sin exponer credenciales.

## Próximos pasos recomendados

- Priorizar dos "recetas" iniciales (crecimiento y floración) y mapearlas a los umbrales actuales de las reglas en `diagnostics/rules.py`.
- Definir el formato de blueprint (YAML/JSON) para automatizaciones y agregar validadores en el CLI antes de ejecutar acciones.
- Ampliar la telemetría del pipeline para registrar comandos simulados/ejecutados y su estado, guardándolos en el Excel y en logs estructurados.
- Diseñar un flujo de calibración en la CLI con recordatorio por fecha y pruebas de saneamiento de sensores.
