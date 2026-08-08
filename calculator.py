"""Simple calculator logic for the Smart Calculator app.

This file keeps the math separate from the user interface so the code is
easier to read and maintain.
"""

from __future__ import annotations

import re


def add(first_number: float, second_number: float) -> float:
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    if second_number == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return first_number / second_number


def format_number(value: float) -> str:
    """Convert a number to a clean string for the display."""
    if value == int(value):
        return str(int(value))
    text = f"{value:.10f}".rstrip("0").rstrip(".")
    return text if text else "0"


def _is_number(token: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(\.\d+)?", token))


def _tokenize(expression: str) -> list[str]:
    """Split the expression into numbers and operators.

    The calculator only supports simple arithmetic, so this tokenizer is kept
    small and beginner-friendly.
    """
    tokens: list[str] = []
    number_buffer = ""
    previous_token = ""

    for character in expression.replace(" ", ""):
        if character.isdigit() or character == ".":
            number_buffer += character
            continue

        if character in "+-*/":
            if number_buffer:
                tokens.append(number_buffer)
                previous_token = number_buffer
                number_buffer = ""

            # Support unary minus at the start of the expression or after
            # another operator, for example: -5 or 10 + -3.
            if character == "-" and (not tokens or previous_token in "+-*/"):
                number_buffer = "-"
                continue

            tokens.append(character)
            previous_token = character
            continue

        raise ValueError("Invalid expression.")

    if number_buffer:
        tokens.append(number_buffer)

    return tokens


def _apply_operator(first_number: float, operator: str, second_number: float) -> float:
    if operator == "+":
        return add(first_number, second_number)
    if operator == "-":
        return subtract(first_number, second_number)
    if operator == "*":
        return multiply(first_number, second_number)
    if operator == "/":
        return divide(first_number, second_number)
    raise ValueError("Invalid expression.")


def calculate(expression: str) -> str:
    """Safely calculate a simple arithmetic expression.

    The calculator supports only numbers and +, -, *, / operators.
    Operator precedence is respected: multiplication and division happen
    before addition and subtraction.
    """
    if not expression.strip():
        raise ValueError("Please enter a number.")

    tokens = _tokenize(expression)
    if not tokens:
        raise ValueError("Invalid expression.")

    if len(tokens) == 1 and _is_number(tokens[0]):
        return format_number(float(tokens[0]))

    # First pass: handle * and /.
    high_priority_tokens: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token in "*/":
            if not high_priority_tokens or index + 1 >= len(tokens):
                raise ValueError("Invalid expression.")

            left_number = float(high_priority_tokens.pop())
            right_number = float(tokens[index + 1])
            result = _apply_operator(left_number, token, right_number)
            high_priority_tokens.append(format_number(result))
            index += 2
            continue

        high_priority_tokens.append(token)
        index += 1

    # Second pass: handle + and - from left to right.
    result = float(high_priority_tokens[0])
    index = 1
    while index < len(high_priority_tokens):
        operator = high_priority_tokens[index]
        if index + 1 >= len(high_priority_tokens):
            raise ValueError("Invalid expression.")

        next_number = float(high_priority_tokens[index + 1])
        result = _apply_operator(result, operator, next_number)
        index += 2

    return format_number(result)


def to_percentage(number_text: str) -> str:
    """Convert the current number to percentage form.

    Example: 50 -> 0.5
    """
    if not number_text or number_text in "+-*/":
        raise ValueError("Please enter a number.")
    return format_number(float(number_text) / 100)


def toggle_sign(number_text: str) -> str:
    """Switch a number between positive and negative."""
    if not number_text or number_text in "+-*/":
        raise ValueError("Please enter a number.")

    number_value = float(number_text)
    return format_number(-number_value)
