def add_numbers(numbers):
    """Add a list of numbers and return the sum."""
    return sum(numbers)


def main():
    """Main function demonstrating typing errors."""
    # Type error: passing a string instead of a list of numbers
    result = add_numbers("not a list")
    print(f"Sum: {result}")


if __name__ == "__main__":
    main() 