"""
GPS Емулятор — Бекенд обчислювального API
Лабораторно-практичне заняття №3

Архітектура (Варіант 4):
  Фронтенд → WebSocket емулятора (дані супутників)
  Фронтенд → POST /calculate (координати + відстані)
  Бекенд   → scipy.optimize.minimize → повертає результат
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np
from scipy.optimize import minimize

app = FastAPI(title="GPS Обчислювальний API", version="1.0.0")

# Дозволяємо CORS для фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- Моделі даних -----

class Satellite(BaseModel):
    id: str
    x: float
    y: float
    distance: float  # розрахована відстань до об'єкта (км)


class CalculateRequest(BaseModel):
    satellites: List[Satellite]


class CalculateResponse(BaseModel):
    analytical: dict | None   # {"x": ..., "y": ...} або None якщо не вдалось
    numerical: dict            # {"x": ..., "y": ...}
    error: str | None = None


# ----- Аналітичний метод -----

def analytical_trilateration(sats: List[Satellite]) -> dict | None:
    """
    Аналітичне розв'язання системи рівнянь трилатерації.
    Використовуємо три супутники: віднімаємо рівняння кіл попарно,
    отримуємо систему лінійних рівнянь, яку розв'язуємо методом Крамера.

    Рівняння кола для супутника i:
        (x - xi)^2 + (y - yi)^2 = ri^2

    Відніманням першого від другого та третього отримуємо лінійну систему:
        2*(x2-x1)*x + 2*(y2-y1)*y = r1^2 - r2^2 + x2^2 - x1^2 + y2^2 - y1^2
        2*(x3-x1)*x + 2*(y3-y1)*y = r1^2 - r3^2 + x3^2 - x1^2 + y3^2 - y1^2
    """
    if len(sats) < 3:
        return None

    # Беремо перші три супутники
    s1, s2, s3 = sats[0], sats[1], sats[2]
    x1, y1, r1 = s1.x, s1.y, s1.distance
    x2, y2, r2 = s2.x, s2.y, s2.distance
    x3, y3, r3 = s3.x, s3.y, s3.distance

    # Коефіцієнти лінійної системи Ax = b
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1)],
        [2 * (x3 - x1), 2 * (y3 - y1)]
    ])
    b = np.array([
        r1**2 - r2**2 + x2**2 - x1**2 + y2**2 - y1**2,
        r1**2 - r3**2 + x3**2 - x1**2 + y3**2 - y1**2
    ])

    det = np.linalg.det(A)
    if abs(det) < 1e-10:
        # Система виродженя (супутники на одній прямій)
        return None

    solution = np.linalg.solve(A, b)
    return {"x": float(solution[0]), "y": float(solution[1])}


# ----- Чисельний метод (scipy) -----

def numerical_trilateration(sats: List[Satellite]) -> dict:
    """
    Чисельна мінімізація функції втрат за допомогою scipy.optimize.minimize.

    Функція втрат — сума квадратів різниць між виміряною відстанню
    до кожного супутника та обчисленою евклідовою відстанню:

        L(x, y) = Σ ( sqrt((x - xi)^2 + (y - yi)^2) - ri )^2

    Початкове наближення — центроїд позицій супутників.
    Метод оптимізації: L-BFGS-B (квазі-ньютонівський, підходить для гладких функцій).
    """
    def loss(pos):
        x, y = pos
        total = 0.0
        for s in sats:
            dist_calc = np.sqrt((x - s.x)**2 + (y - s.y)**2)
            total += (dist_calc - s.distance) ** 2
        return total

    # Початкове наближення — середнє положення супутників
    x0 = np.mean([s.x for s in sats])
    y0 = np.mean([s.y for s in sats])

    result = minimize(
        loss,
        x0=[x0, y0],
        method="L-BFGS-B",
        options={"ftol": 1e-12, "gtol": 1e-10, "maxiter": 1000}
    )

    return {"x": float(result.x[0]), "y": float(result.x[1])}


# ----- Розрахунок відстані за часом -----

def compute_distances(sats_raw: List[Satellite]) -> List[Satellite]:
    """
    Відстань розраховується через різницю часів:
        відстань = (receivedAt - sentAt) * швидкість_світла
    Але у цьому варіанті фронтенд передає вже готові distance,
    тому ця функція лише повертає вхідні дані.
    """
    return sats_raw


# ----- Ендпоінти -----

@app.get("/")
def root():
    return {"status": "ok", "message": "GPS Обчислювальний API працює"}


@app.post("/calculate", response_model=CalculateResponse)
def calculate(req: CalculateRequest):
    """
    Приймає список супутників з координатами та відстанями,
    виконує аналітичний та чисельний розрахунок,
    повертає обидва результати.
    """
    sats = req.satellites

    if len(sats) < 3:
        return CalculateResponse(
            analytical=None,
            numerical={"x": 0, "y": 0},
            error="Потрібно щонайменше 3 супутники"
        )

    analytical = analytical_trilateration(sats)
    numerical = numerical_trilateration(sats)

    return CalculateResponse(
        analytical=analytical,
        numerical=numerical
    )


@app.get("/health")
def health():
    return {"status": "healthy"}
