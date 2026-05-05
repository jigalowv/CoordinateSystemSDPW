"""
main.py — Головний скрипт лабораторної роботи №6
Запускає всі три завдання:
  1. Генерація та візуалізація полігонів (N = 10, 50, 100)
  2. Аналіз точності Монте-Карло (N = 50, різні K)
  3. Бенчмарк продуктивності (N = 10, 50, 100, 1000)
"""

import os
import sys
import random
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Додаємо поточну директорію до шляху пошуку модулів
sys.path.insert(0, os.path.dirname(__file__))

from generators import generate_polygon, visualize_polygon
from algorithms import gauss_area, monte_carlo_area

# ─── Константи ────────────────────────────────────────────────────────────────
SEED = 42
MC_BENCHMARK_POINTS = 10_000
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

DARK_BG   = '#0f0f1a'
CYAN      = '#00e5ff'
PINK      = '#ff4081'
YELLOW    = '#ffd600'
GREEN     = '#69ff47'
TEXT_CLR  = '#e0e0e0'


def img(name: str) -> str:
    """Повертає повний шлях до файлу в папці images/."""
    return os.path.join(IMAGES_DIR, name)


# ─── 1. Генерація полігонів ───────────────────────────────────────────────────
def task1_generate_polygons():
    print("\n" + "=" * 55)
    print("  ЗАВДАННЯ 1 — Генерація та візуалізація полігонів")
    print("=" * 55)

    random.seed(SEED)
    vertex_counts = [10, 50, 100]
    polys = {}

    for n in vertex_counts:
        poly = generate_polygon(num_points=n)
        polys[n] = poly
        fname = img(f"polygon_n{n}.png")
        visualize_polygon(poly, filename=fname)
        print(f"  N={n:>3}: Shapely area = {poly.area:.6f}")

    return polys


# ─── 2. Аналіз точності Монте-Карло ──────────────────────────────────────────
def task2_monte_carlo_accuracy(poly50):
    print("\n" + "=" * 55)
    print("  ЗАВДАННЯ 2 — Збіжність Монте-Карло (N=50)")
    print("=" * 55)

    random.seed(SEED)
    true_area = poly50.area

    iterations_list = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]
    errors = []

    print(f"  {'K':>8}  {'MC Area':>12}  {'Error %':>10}")
    print(f"  {'-'*8}  {'-'*12}  {'-'*10}")

    for k in iterations_list:
        mc_area = monte_carlo_area(poly50, num_points=k)
        error = abs(mc_area - true_area) / true_area * 100
        errors.append(error)
        print(f"  {k:>8,}  {mc_area:>12.4f}  {error:>9.4f}%")

    # ── Графік збіжності
    fig, ax = plt.subplots(figsize=(9, 5), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)

    ax.plot(iterations_list, errors, marker='o', color=PINK,
            linewidth=2.5, markersize=7, markerfacecolor=YELLOW, zorder=3)

    ax.axhline(y=1.0, color=CYAN, linestyle='--', linewidth=1.2,
               alpha=0.7, label='Поріг 1%')
    ax.axhline(y=0.5, color=GREEN, linestyle=':', linewidth=1.2,
               alpha=0.7, label='Поріг 0.5%')

    ax.set_xscale('log')
    ax.set_xlabel('Кількість точок K  (log-шкала)', color=TEXT_CLR, fontsize=11)
    ax.set_ylabel('Відносна похибка (%)', color=TEXT_CLR, fontsize=11)
    ax.set_title('Збіжність методу Монте-Карло  ·  N = 50 вершин',
                 color='white', fontsize=13, pad=12)

    ax.tick_params(colors=TEXT_CLR)
    ax.grid(True, linestyle='--', alpha=0.25, color='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')

    legend = ax.legend(facecolor='#1a1a2e', edgecolor='#333355',
                       labelcolor=TEXT_CLR, fontsize=10)

    plt.tight_layout()
    plt.savefig(img('error_plot.png'), dpi=130,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n  Графік збережено: images/error_plot.png")

    return iterations_list, errors


# ─── 3. Бенчмарк продуктивності ──────────────────────────────────────────────
def task3_benchmark():
    print("\n" + "=" * 55)
    print(f"  ЗАВДАННЯ 3 — Бенчмарк  (MC K={MC_BENCHMARK_POINTS:,})")
    print("=" * 55)

    vertex_counts = [10, 50, 100, 1000]
    REPEATS = 5
    results = []

    header = f"  {'N':>5}  {'Shapely (мс)':>14}  {'Гаус (мс)':>12}  {'MC (мс)':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    for n in vertex_counts:
        random.seed(SEED)
        poly = generate_polygon(num_points=n)

        # Shapely
        t0 = time.perf_counter()
        for _ in range(REPEATS):
            _ = poly.area
        t_shapely = (time.perf_counter() - t0) / REPEATS * 1000

        # Гаус
        t0 = time.perf_counter()
        for _ in range(REPEATS):
            _ = gauss_area(poly)
        t_gauss = (time.perf_counter() - t0) / REPEATS * 1000

        # Монте-Карло
        t0 = time.perf_counter()
        for _ in range(REPEATS):
            _ = monte_carlo_area(poly, num_points=MC_BENCHMARK_POINTS)
        t_mc = (time.perf_counter() - t0) / REPEATS * 1000

        results.append((n, t_shapely, t_gauss, t_mc))
        print(f"  {n:>5}  {t_shapely:>14.4f}  {t_gauss:>12.4f}  {t_mc:>12.2f}")

    # ── Графік бенчмарку
    labels  = [f"N={r[0]}" for r in results]
    t_s_lst = [r[1] for r in results]
    t_g_lst = [r[2] for r in results]
    t_m_lst = [r[3] for r in results]

    x = list(range(len(labels)))
    w = 0.25

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)

    bars_s = ax.bar([i - w for i in x], t_s_lst, width=w,
                    label='Shapely', color=CYAN,   alpha=0.85)
    bars_g = ax.bar(x,               t_g_lst, width=w,
                    label='Гаус',    color=GREEN,  alpha=0.85)
    bars_m = ax.bar([i + w for i in x], t_m_lst, width=w,
                    label=f'Монте-Карло (K={MC_BENCHMARK_POINTS:,})',
                    color=PINK, alpha=0.85)

    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, color=TEXT_CLR)
    ax.set_ylabel('Час виконання (мс, log-шкала)', color=TEXT_CLR, fontsize=11)
    ax.set_title('Порівняння швидкодії алгоритмів', color='white', fontsize=13, pad=12)
    ax.tick_params(colors=TEXT_CLR)
    ax.grid(True, axis='y', linestyle='--', alpha=0.25, color='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')

    legend = ax.legend(facecolor='#1a1a2e', edgecolor='#333355',
                       labelcolor=TEXT_CLR, fontsize=10)

    plt.tight_layout()
    plt.savefig(img('time_benchmark.png'), dpi=130,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n  Графік збережено: images/time_benchmark.png")

    return results


# ─── Головна точка входу ──────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║   Лабораторна робота №6 — Площа геометричних фігур  ║")
    print("╚══════════════════════════════════════════════════════╝")

    polys   = task1_generate_polygons()
    _, _    = task2_monte_carlo_accuracy(polys[50])
    results = task3_benchmark()

    print("\n✓  Всі завдання виконано. Перевір папку images/\n")
