# Ruta La Campestre

Este proyecto contiene una base inicial para planificar rutas de:

- **Entrega de alimento**
- **Retiro de huevos**

considerando el nuevo requisito operativo de pasar de **1 retiro semanal** a **2 retiros semanales**.

## Enfoque recomendado

1. Exportar los puntos desde Google Maps (o mantener una tabla maestra de ubicaciones).
2. Clasificar cada punto por:
   - tipo de visita (`entrega`, `retiro` o `mixto`)
   - frecuencia semanal (`1` o `2`)
   - prioridad/ventana horaria (opcional)
3. Construir dos rutas semanales:
   - **Ruta A**: por ejemplo lunes/jueves
   - **Ruta B**: por ejemplo martes/viernes
4. Validar distancia, tiempo total y capacidad del vehículo.

## Estructura

- `src/route_planner.py`: script inicial para dividir puntos por frecuencia y generar rutas simples por día.
- `data/puntos_ejemplo.csv`: datos de ejemplo.

## Ejecutar ejemplo

```bash
python3 src/route_planner.py --input data/puntos_ejemplo.csv --depot "Granja Central"
```

El script imprime un plan semanal base con dos retiros para clientes que lo requieren.
