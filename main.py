"""Entry point for the Smart Calculator application."""

from ui import CalculatorApp


def main() -> None:
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
