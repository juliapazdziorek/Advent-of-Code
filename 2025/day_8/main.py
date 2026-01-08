from utils import files
from utils import maths

# Day 8: Playground
# https://adventofcode.com/2025/day/8


class BoxesCollection:
    boxes: list[tuple[int, ...]]
    edges: list[tuple[int, int]]
    parents: list[int]


    def __init__(self, boxes: list[tuple[int, ...]]) -> None:
        self.boxes = boxes
        self.edges = [(i, j) for i in range(len(boxes)) for j in range(i + 1, len(boxes))]
        self.edges.sort(key=lambda edge: maths.count_euclidean_distance((boxes[edge[0]], boxes[edge[1]])))
        self.parents = list(range(len(boxes)))


    def find_root(self, circuit_id: int) -> int:
        if self.parents[circuit_id] == circuit_id:
            return circuit_id

        self.parents[circuit_id] = self.find_root(self.parents[circuit_id])
        return self.parents[circuit_id]


    def connect_circuits(self, circuit1_id, circuit2_id) -> None:
        self.parents[self.find_root(circuit1_id)] = self.find_root(circuit2_id)


    def count_multiplied_largest_circuits(self) -> int:
        for edge in self.edges[:1000]:
            self.connect_circuits(*edge)

        sizes = [0] * len(self.boxes)
        for i in range(len(self.boxes)):
            sizes[self.find_root(i)] += 1

        largest_three = sorted([size for size in sizes], reverse=True)[:3]
        return largest_three[0] * largest_three[1] * largest_three[2]


    def count_multiplied_last_circuits(self) -> int | None:
        circuits = len(self.boxes)
        for edge in self.edges:
            if self.find_root(edge[0]) == self.find_root(edge[1]):
                continue

            self.connect_circuits(*edge)
            circuits -= 1

            if circuits == 1:
                return self.boxes[edge[0]][0] * self.boxes[edge[1]][0]

        return None


def parse_boxes(lines: list[str]) -> list[tuple[int, ...]]:
    return [tuple(map(int, line.split(','))) for line in lines]


def count_multiplied_largest_circuits(boxes: list[tuple[int, ...]]) -> int:
    boxes_collection = BoxesCollection(boxes)
    return boxes_collection.count_multiplied_largest_circuits()


def count_multiplied_last_circuits(boxes: list[tuple[int, ...]]) -> int:
    boxes_collection = BoxesCollection(boxes)
    return boxes_collection.count_multiplied_last_circuits()


def main() -> None:
    lines = files.read_file('data.txt')
    boxes = parse_boxes(lines)
    multiplied_largest_circuits = count_multiplied_largest_circuits(boxes)
    multiplied_last_circuits = count_multiplied_last_circuits(boxes)

    print(f"1. The number got from multiplying three largest circuits after 1000 connections is equal to: {multiplied_largest_circuits}")
    print(f"2. The number got from multiplying x coordinates of two last boxes is equal to: {multiplied_last_circuits}")


if __name__ == "__main__":
    main()