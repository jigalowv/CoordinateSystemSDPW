import math
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon


def generate_polygon(num_points: int, radius: float = 10.0, irregularity: float = 0.35) -> Polygon:
    """
    Генерує випадковий полігон без самоперетинів.

    Алгоритм:
    1. Генеруються випадкові кути (від 0 до 2pi).
    2. Кути сортуються.
    3. Для кожного кута генерується випадковий радіус.
    4. Полярні координати перетворюються в Декартові (x, y).

    Args:
        num_points (int): Кількість вершин.
        radius (float): Середній радіус описуючого кола.
        irregularity (float): Коефіцієнт "випадковості" радіуса (0.0 - ідеальне коло, 1.0 - сильний розкид).

    Returns:
        Polygon: Об'єкт полігону Shapely.
    """
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(num_points)])

    points = []
    for angle in angles:
        r = radius * (1 - irregularity * random.random())
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))

    poly = Polygon(points)

    if not poly.is_valid:
        return poly.buffer(0)

    return poly


def visualize_polygon(polygon: Polygon, filename: str = None, title: str = None):
    """
    Візуалізує полігон. Якщо вказано filename, зберігає у файл.
    """
    x, y = polygon.exterior.xy

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0f0f1a')
    ax.set_facecolor('#0f0f1a')

    ax.plot(x, y, color='#00e5ff', linewidth=2, zorder=1)
    ax.fill(x, y, color='#00e5ff', alpha=0.15)
    ax.scatter(x, y, color='#ff4081', s=25, zorder=2)

    n_vertices = len(polygon.exterior.coords) - 1
    ax.set_title(
        title or f"Polygon  ·  N = {n_vertices} вершин",
        color='white', fontsize=13, pad=12
    )
    ax.grid(True, linestyle='--', alpha=0.25, color='white')
    ax.axis('equal')
    ax.tick_params(colors='#aaaaaa')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"  Збережено: {filename}")
        plt.close()
    else:
        plt.show()


# --- Тестовий запуск ---
if __name__ == "__main__":
    random.seed(42)
    try:
        my_poly = generate_polygon(num_points=15, radius=50)
        print(f"Test Polygon Area (Shapely): {my_poly.area}")
        visualize_polygon(my_poly)
    except Exception as e:
        print(f"Error: {e}")
