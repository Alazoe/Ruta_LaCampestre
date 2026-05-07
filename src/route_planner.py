#!/usr/bin/env python3
"""Planificador base de rutas semanales para entrega/retiro.

Este ejemplo no usa APIs pagas: aplica una heurística simple de vecino más cercano
sobre coordenadas geográficas (distancia Haversine).
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Point:
    name: str
    lat: float
    lng: float
    service_type: str
    weekly_pickups: int


def haversine_km(a: Point, b: Point) -> float:
    r = 6371.0
    lat1 = math.radians(a.lat)
    lon1 = math.radians(a.lng)
    lat2 = math.radians(b.lat)
    lon2 = math.radians(b.lng)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def read_points(path: str) -> list[Point]:
    points: list[Point] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            points.append(
                Point(
                    name=row["name"],
                    lat=float(row["lat"]),
                    lng=float(row["lng"]),
                    service_type=row["service_type"].strip().lower(),
                    weekly_pickups=int(row["weekly_pickups"]),
                )
            )
    return points


def nearest_neighbor_route(depot: Point, stops: Iterable[Point]) -> list[Point]:
    pending = list(stops)
    route: list[Point] = []
    current = depot
    while pending:
        nxt = min(pending, key=lambda p: haversine_km(current, p))
        route.append(nxt)
        pending.remove(nxt)
        current = nxt
    return route


def route_distance_km(depot: Point, route: list[Point]) -> float:
    if not route:
        return 0.0
    total = haversine_km(depot, route[0])
    for i in range(len(route) - 1):
        total += haversine_km(route[i], route[i + 1])
    total += haversine_km(route[-1], depot)
    return total


def build_week_plan(points: list[Point], depot_name: str) -> dict[str, list[Point]]:
    depot = next((p for p in points if p.name == depot_name), None)
    if depot is None:
        raise ValueError(f"No se encontró depósito '{depot_name}' en el CSV")

    clients = [p for p in points if p.name != depot_name and p.service_type != "depot"]

    twice = [p for p in clients if p.weekly_pickups >= 2]
    once = [p for p in clients if p.weekly_pickups == 1]

    # Distribución simple:
    # - Lunes y Jueves atienden los de 2 retiros/semana.
    # - Miércoles atiende una parte de 1 retiro/semana.
    # - Viernes atiende el resto de 1 retiro/semana.
    half = len(once) // 2
    plan = {
        "Lunes": twice[:],
        "Miércoles": once[:half],
        "Jueves": twice[:],
        "Viernes": once[half:],
    }

    return plan


def print_plan(points: list[Point], depot_name: str) -> None:
    depot = next(p for p in points if p.name == depot_name)
    plan = build_week_plan(points, depot_name)

    print("=== Plan semanal propuesto ===")
    for day, stops in plan.items():
        route = nearest_neighbor_route(depot, stops)
        km = route_distance_km(depot, route)
        names = " -> ".join(p.name for p in route) if route else "(sin paradas)"
        print(f"\n{day}:")
        print(f"  Ruta: {depot.name} -> {names} -> {depot.name}")
        print(f"  Distancia estimada: {km:.2f} km")


def main() -> None:
    parser = argparse.ArgumentParser(description="Planificador semanal de rutas")
    parser.add_argument("--input", required=True, help="CSV de puntos")
    parser.add_argument("--depot", required=True, help="Nombre del depósito/base")
    args = parser.parse_args()

    points = read_points(args.input)
    print_plan(points, args.depot)


if __name__ == "__main__":
    main()
