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


def shoelace_formula(vertices: list[tuple[int, int]]) -> float:
    """
    Calculates the area of a polygon using the shoelace formula.

    """
    if len(vertices) < 3:
        return 0.0
    
    if vertices[0] != vertices[-1]:
        vertices = vertices + [vertices[0]]
    
    area = 0.0
    for i in range(len(vertices) - 1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        area += x1 * y2 - x2 * y1
    
    return abs(area) / 2.0


def polygon_area_with_boundary(vertices: list[tuple[int, int]], boundary_points: int) -> int:
    """
    Calculates the total area of a polygon including its interior and boundary using Pick's theorem.
    
    Pick's theorem: A = I + B/2 - 1, where:
    - A is the area calculated by shoelace formula
    - I is the number of interior points
    - B is the number of boundary points
    
    Rearranging: I = A - B/2 + 1
    Total points = I + B = A - B/2 + 1 + B = A + B/2 + 1
    """
    area = shoelace_formula(vertices)
    return int(area + boundary_points // 2 + 1)