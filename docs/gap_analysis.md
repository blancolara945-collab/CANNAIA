# Brecha y pendientes para Doctor Cañamo

Este documento resume lo que falta para que el prototipo actual se convierta en un sistema operativo end-to-end.

## Ingesta de datos
- **Integración real con Growee y SmartLife**: los conectores actuales son sintéticos; falta implementar autenticación, manejo de rate limits, y mapeo de dispositivos/zonas del cultivo.
- **Imágenes de Drive**: hoy sólo se registran referencias; falta la descarga/indexado de fotos, normalización de metadatos (planta, ciclo) y redimensionado para visión.
- **Persistencia histórica**: el pipeline escribe un Excel por corrida; falta un almacén incremental (CSV/Parquet/DB) y control de duplicados/staging.
- **Programación y backfill**: no hay scheduler; se necesita orquestar corridas periódicas y reingestas cuando fallen fuentes.

## Diagnóstico con IA
- **Features y agregaciones**: sólo existen reglas por umbral; falta el cálculo de promedios móviles, variaciones y correlaciones clima-nutrientes.
- **Modelo de visión**: no hay clasificación de imágenes; falta elegir un modelo pre-entrenado, etiquetar dataset inicial y exponer un servicio/librería de inferencia.
- **Fusión de señales**: se requiere combinar sensores + visión en un modelo de decisión entrenable y calibrar umbrales con datos reales.
- **Aprendizaje continuo**: no hay ciclo de retroalimentación con validación humana ni mecanismos de retraining.

## Automatización correctiva
- **Controladores de acción reales**: las acciones son stubs; falta invocar APIs de SmartLife/Growee, confirmar estado y manejar reintentos/fallos.
- **Guardrails de seguridad**: definir límites de pH/EC/temperatura, frecuencia máxima de cambios y modos manuales o de «dry run» por entorno.
- **Cierre del loop**: leer métricas post-acción para validar impacto y registrar auditoría completa (quién/qué/cuándo/resultado).

## Seguridad, operaciones y observabilidad
- **Gestión de secretos**: mover credenciales a un vault/secret manager y rotarlas; documentar variables requeridas por entorno.
- **Monitoreo y alertas**: agregar logs estructurados, métricas (p.ej., Prometheus) y alertas (Slack/Email) para fallos de ingesta/diagnóstico/acción.
- **Testing con datos reales**: crear fixtures anonimizados y pruebas de integración contra sandboxes de Growee/SmartLife.
- **Despliegue**: definir empaquetado (Docker) y entornos (dev/staging/prod) con pipelines de CI/CD que corran más allá del modo `--dry-run`.

## Experiencia de usuario y datos
- **Dashboard**: hace falta un panel para visualizar tendencias, diagnósticos y acciones aplicadas.
- **Calidad de datos avanzada**: ampliar validaciones (rangos dinámicos, detección de outliers, sincronización de timestamps, unidades consistentes).
- **Esquema contractual**: formalizar el modelo tabular (campos obligatorios/opcionales) y versionarlo para compatibilidad futura.

## Próximos pasos sugeridos
1. Implementar conectores reales de Growee/SmartLife con pruebas integradas y almacenamiento incremental.
2. Añadir agregaciones y checklist de reglas expertas calibradas con datos reales; instrumentar captura y etiquetado de imágenes.
3. Construir acciones con guardrails y cierre de bucle de verificación; publicar contenedor ejecutable y pipeline agendado.
