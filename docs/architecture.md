# Doctor Cañamo - Arquitectura técnica

Este documento describe la arquitectura propuesta para el proyecto **Doctor Cañamo**, organizado en tres estructuras principales: adquisición de datos, diagnóstico inteligente y automatización correctiva.

## 1. Adquisición de datos (Estructura 1)

| Fuente | Métricas previstas | Método de ingesta | Frecuencia | Notas |
| --- | --- | --- | --- | --- |
| Growee Dashboard | Temperatura de agua, EC, pH | API/HTML scraping con autenticación de usuario | 5-15 min | Sincronizar con zona horaria del cultivo |
| SmartLife (Tuya) | Temperatura y humedad ambiente | API de Tuya Smart/SmartLife con credenciales | 5-15 min | Mapear ubicación del dispositivo en el cuarto |
| Google Drive | Fotografías de raíces y hojas | API de Drive, carpeta dedicada | 1-2 h o bajo demanda | Normalizar nombre y metadatos (timestamp, planta, ciclo) |

### Pipeline sugerido
1. **Conectores** por fuente que manejen autenticación y limitación de tasa.
2. **Normalización** a un esquema común (`timestamp`, `sensor_id`, `métrica`, `valor`, `unidad`, `origen`).
3. **Almacenamiento** en base tabular (CSV/Parquet) y carga incremental a un libro de Excel de control.
4. **Validación**: rangos permitidos, detección de valores faltantes y alertas.

### Esquema de datos inicial (tabular)
- `timestamp` (UTC o zona local explícita)
- `source` (growee | smartlife | drive)
- `device_id`
- `metric` (water_temp, ec, ph, air_temp, humidity, image_ref, etc.)
- `value` (numérico o ruta de imagen)
- `unit`
- `plant_id` (opcional para relacionar fotos)

## 2. Diagnóstico con IA (Estructura 2)

### Objetivo
Evaluar salud y necesidades del cultivo combinando sensores y análisis visual, generando recomendaciones accionables y un histórico que mejore con el tiempo.

### Componentes
- **Motor de features**: calcula promedios móviles, deltas (p.ej. variación de pH) y correlaciones clima–nutrientes.
- **Modelo de visión**: clasificación de carencias (NPK, Ca/Mg), estrés hídrico o térmico a partir de fotos de hojas/raíces.
- **Modelo de decisión**: fusiona señales de sensores y visión (reglas + modelo supervisado). Puede iniciar con reglas expertas y transicionar a un modelo de ML.
- **Bucles de retroalimentación**: registrar acciones aplicadas y medir respuesta del cultivo para reentrenar modelos.

### Flujo de diagnóstico
1. Ingesta consolidada → validación → features agregadas por hora/día.
2. Procesamiento de imágenes → etiquetas de salud/confianza.
3. Motor de decisión genera **diagnóstico** (estado, causa probable) y **recomendación** (acción, intensidad, duración).
4. Registro del diagnóstico en el libro de control con trazabilidad de datos de entrada.

### Métricas de calidad
- Precisión de diagnóstico (validada manualmente al inicio).
- Tiempo de respuesta desde captura de datos hasta recomendación.
- Efecto de la acción (mejora de métricas objetivo en 24-48h).

## 3. Automatización correctiva (Estructura 3)

### Acciones previstas
- Ajuste de clima vía SmartLife (A/C, deshumidificador, ventiladores).
- Ajuste de nutrientes vía Growee (EC, pH, temperatura de agua).

### Orquestación
- **Controlador de acciones** con colas y verificación de estado antes y después de ejecutar.
- **Políticas de seguridad**: límites máximos/mínimos, bloqueos de frecuencia, confirmación manual opcional.
- **Observabilidad**: log de comandos enviados, resultado, y relectura de sensores para cerrar el ciclo.

## 4. Seguridad y cumplimiento
- Almacenar credenciales en vault/variables de entorno, nunca en código plano.
- Manejo de PII mínimo; anonimizar datos si se comparte el libro de control.
- Asegurar HTTPS para cualquier API expuesta.

## 5. Roadmap sugerido

| Fase | Entregable | Alcance |
| --- | --- | --- |
| 0 | Prototipo de ingesta | Scripts que extraigan Growee, SmartLife y fotos de Drive a CSV/Excel. Validación básica. |
| 1 | Diagnóstico inicial | Reglas expertas + checklist; clasificador ligero de imágenes pre-entrenado. |
| 2 | Automatización controlada | Integración con SmartLife/Growee con límites de seguridad y modo «dry run». |
| 3 | Mejora continua | Reentrenamiento periódico, dashboards y alertas. |

## 6. Próximos pasos inmediatos
1. Obtener claves API de Growee y Tuya/SmartLife; definir estructura de carpeta en Drive.
2. Definir esquema del libro de Excel (pestañas por fuente + resumen).
3. Implementar ingesta mínima (lectura y volcado a CSV) y pruebas con datos reales.
4. Establecer umbrales iniciales de alerta (pH, EC, temperatura, humedad).
