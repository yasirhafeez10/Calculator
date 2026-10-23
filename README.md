# Smart Calculator

## Description

Smart Calculator is a beginner-friendly desktop calculator made with Python 3 and CustomTkinter. It works offline and provides a clean modern interface for basic arithmetic.

## Features

- Addition, subtraction, multiplication, and division
- Percentage support
- Decimal numbers
- Positive and negative toggle
- Clear and backspace buttons
- Keyboard support
- Safe calculation without unrestricted `eval()`
- Modern dark-mode UI

## Technologies Used

- Python 3
- CustomTkinter

## Project Structure

```text
SmartCalculator/
├── main.py
├── calculator.py
├── ui.py
├── requirements.txt
├── README.md
└── assets/
    └── icons/
```

## Installation

Install the required package:

```bash
pip install -r requirements.txt
```

## How to Run

Start the application with:

```bash
python main.py
```

## Keyboard Shortcuts

- `0` to `9` for numbers
- `+`, `-`, `*`, `/` for operators
- `%` for percentage
- `.` for decimals
- `Enter` to calculate
- `Backspace` to delete the last character
- `Escape` to clear the calculator

## Future Improvements

- Add calculation history
- Add scientific functions
- Add light mode toggle
- Add sound feedback for button clicks

## How the Calculator Works

The UI in `ui.py` sends the entered expression to `calculator.py`. The calculator logic uses a small safe parser that supports numbers and the `+`, `-`, `*`, and `/` operators. It does not use unrestricted Python `eval()`, which keeps the app safer and easier to understand.
