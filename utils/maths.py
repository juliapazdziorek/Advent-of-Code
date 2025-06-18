import math

def solve_quadratic_equation(a: float, b: float, c: float) -> tuple[float, ...]:
    """
    Solves the quadratic equation ax^2 + bx + c = 0.
    Returns a tuple of real solutions (can be empty, one, or two values).
    """
    if a == 0:
        raise ValueError("Coefficient 'a' must not be zero for a quadratic equation.")

    delta = b ** 2 - 4 * a * c
    solutions = []

    if delta > 0:
        sqrt_delta = math.sqrt(delta)
        solutions.append((-b - sqrt_delta) / (2 * a))
        solutions.append((-b + sqrt_delta) / (2 * a))
    elif delta == 0:
        solutions.append(-b / (2 * a))
    # If delta < 0, no real solutions

    return tuple(solutions)