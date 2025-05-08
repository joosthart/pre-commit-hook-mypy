def add_numbers(numbers: list[int]) -> int:
    return sum(numbers)


def main() -> None:
    result = add_numbers([1, 2, 3, 4, 5])
    print(f"Sum: {result}")
