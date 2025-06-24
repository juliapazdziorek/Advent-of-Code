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


def transpose_2d_array(matrix: list[list[str]]) -> list[list[str]]:
    """
    Transpose a 2D matrix (list of lists).
    Returns a new matrix where rows and columns are swapped.
    """
    if not matrix or not matrix[0]:
        return []
    
    return [list(row) for row in zip(*matrix)]


def count_manhattan_distance(pair: tuple[tuple[int, ...], tuple[int, ...]]) -> int:
    """
    Calculates the Manhattan distance between two points of any dimension.
    Each point is a tuple of coordinates.
    Example: count_manhattan_distance(((x1, y1, ...), (x2, y2, ...))) -> sum(|xi - yi| for all i)
    """
    v1, v2 = pair
    if len(v1) != len(v2):
        raise ValueError("Both vectors must have the same number of dimensions.")
    return sum(abs(a - b) for a, b in zip(v1, v2))