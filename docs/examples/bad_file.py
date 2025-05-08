def add_numbers(numbers: list[int]) -> int:
    return sum(numbers)


def main() -> None:
    # Type error: passing a string instead of a list of numbers
    result = add_numbers("not a list")  # This will cause a mypy error
    print(f"Sum: {result}")
