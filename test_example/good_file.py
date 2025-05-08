from typing import List


def add_numbers(numbers: List[int]) -> int:
    """Add a list of numbers and return the sum."""
    return sum(numbers)


def main() -> None:
    """Main function to demonstrate typing."""
    result = add_numbers([1, 2, 3, 4, 5])
    print(f"Sum: {result}")


if __name__ == "__main__":
    main() 