import random
from shapely.geometry import Point, Polygon


def gauss_area(polygon: Polygon) -> float:
    """
    Обчислення площі полігону за формулою Гауса (Shoelace formula).

    Формула:
        S = 0.5 * |Σ (x_i * y_{i+1} - x_{i+1} * y_i)|

    Args:
        polygon (Polygon): Об'єкт полігону Shapely.

    Returns:
        float: Площа полігону.
    """
    coords = list(polygon.exterior.coords[:-1])  # остання точка == перша
    n = len(coords)
    area = 0.0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += (x1 * y2) - (x2 * y1)
    return abs(area) / 2.0


def monte_carlo_area(polygon: Polygon, num_points: int = 10_000) -> float:
    """
    Обчислення площі полігону методом Монте-Карло.

    Алгоритм:
        1. Визначаємо Bounding Box полігону.
        2. Генеруємо num_points випадкових точок всередині BB.
        3. Рахуємо частку точок, що потрапили в полігон.
        4. Площа ≈ S_bb * (inside / num_points)

    Args:
        polygon (Polygon): Об'єкт полігону Shapely.
        num_points (int): Кількість випадкових точок.

    Returns:
        float: Наближена площа полігону.
    """
    min_x, min_y, max_x, max_y = polygon.bounds
    bbox_area = (max_x - min_x) * (max_y - min_y)

    inside_count = 0
    for _ in range(num_points):
        rx = random.uniform(min_x, max_x)
        ry = random.uniform(min_y, max_y)
        if polygon.contains(Point(rx, ry)):
            inside_count += 1

    return bbox_area * (inside_count / num_points)
