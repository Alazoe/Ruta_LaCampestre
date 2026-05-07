diff --git a/readme.md b/readme.md
index 5979cf730ff68439e739757e6808a0be7496a0b8..ca505af1ba1761a4dcbbd83403e5959fa008c355 100644
--- a/readme.md
+++ b/readme.md
@@ -1,33 +1,92 @@
 # Ruta La Campestre
 
-Este proyecto contiene una base inicial para planificar rutas de:
+Planificador base de rutas semanales para **entrega de alimento** y **retiro de huevos**, con soporte para clientes que requieren **1 o 2 retiros por semana**.
 
-- **Entrega de alimento**
-- **Retiro de huevos**
+El proyecto usa una heurística simple (vecino más cercano + distancia Haversine) para construir un plan inicial por día sin depender de APIs pagas.
 
-considerando el nuevo requisito operativo de pasar de **1 retiro semanal** a **2 retiros semanales**.
+## ¿Qué hace este proyecto?
 
-## Enfoque recomendado
+- Lee un archivo CSV con puntos geográficos (depósito y clientes).
+- Separa clientes por frecuencia de retiro semanal.
+- Genera un plan semanal base:
+  - **Lunes** y **Jueves** para clientes con `weekly_pickups >= 2`.
+  - **Miércoles** y **Viernes** para dividir clientes con `weekly_pickups == 1`.
+- Ordena cada ruta diaria con vecino más cercano.
+- Estima la distancia total de cada día en kilómetros.
 
-1. Exportar los puntos desde Google Maps (o mantener una tabla maestra de ubicaciones).
-2. Clasificar cada punto por:
-   - tipo de visita (`entrega`, `retiro` o `mixto`)
-   - frecuencia semanal (`1` o `2`)
-   - prioridad/ventana horaria (opcional)
-3. Construir dos rutas semanales:
-   - **Ruta A**: por ejemplo lunes/jueves
-   - **Ruta B**: por ejemplo martes/viernes
-4. Validar distancia, tiempo total y capacidad del vehículo.
+## Estructura del repositorio
 
-## Estructura
+- `src/route_planner.py`: lógica del planificador y ejecución por CLI.
+- `data/puntos_ejemplo.csv`: dataset de ejemplo para pruebas rápidas.
 
-- `src/route_planner.py`: script inicial para dividir puntos por frecuencia y generar rutas simples por día.
-- `data/puntos_ejemplo.csv`: datos de ejemplo.
+## Requisitos
 
-## Ejecutar ejemplo
+- Python **3.10+** (recomendado 3.11 o 3.12).
+- No requiere dependencias externas (solo librería estándar).
+
+Verifica tu versión:
+
+```bash
+python3 --version
+```
+
+## Formato del CSV de entrada
+
+El archivo debe incluir encabezados exactamente así:
+
+- `name`
+- `lat`
+- `lng`
+- `service_type`
+- `weekly_pickups`
+
+### Ejemplo
+
+```csv
+name,lat,lng,service_type,weekly_pickups
+Granja Central,-31.4201,-64.1888,depot,0
+Cliente A,-31.4010,-64.1905,retiro,2
+Cliente B,-31.4330,-64.1750,mixto,1
+```
+
+> Importante: el valor que pases en `--depot` debe coincidir exactamente con el `name` del depósito en el CSV.
+
+## Cómo ejecutar el proyecto
+
+Desde la raíz del repo:
 
 ```bash
 python3 src/route_planner.py --input data/puntos_ejemplo.csv --depot "Granja Central"
 ```
 
-El script imprime un plan semanal base con dos retiros para clientes que lo requieren.
+### Salida esperada
+
+El script imprime algo como:
+
+- `=== Plan semanal propuesto ===`
+- Ruta por día (`Lunes`, `Miércoles`, `Jueves`, `Viernes`)
+- Distancia estimada por día
+
+## Flujo recomendado para usarlo en operación
+
+1. Mantén una tabla maestra de clientes con coordenadas actualizadas.
+2. Exporta/actualiza el CSV en el formato requerido.
+3. Ejecuta el script al inicio de semana.
+4. Revisa distancias y ajusta manualmente ventanas horarias o prioridades.
+5. Itera según capacidad de vehículo y tiempos reales de campo.
+
+## Problemas comunes
+
+- **Error: No se encontró depósito ... en el CSV**
+  - Verifica que `--depot` coincida con el campo `name` del depósito.
+- **Error al convertir lat/lng**
+  - Asegúrate de usar números decimales válidos (`-31.42`, `-64.18`).
+- **Rutas poco óptimas**
+  - El algoritmo actual es heurístico y base; sirve para planificación inicial.
+
+## Próximas mejoras sugeridas
+
+- Soporte para ventanas horarias y prioridad por cliente.
+- Balance de carga por día (capacidad de vehículo).
+- Exportación de rutas a formatos visuales (mapas).
+- Integración opcional con APIs de ruteo para tiempos reales.
