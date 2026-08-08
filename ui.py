"""User interface for the Smart Calculator app."""

from __future__ import annotations

import customtkinter as ctk

from calculator import calculate, toggle_sign, to_percentage


class CalculatorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Smart Calculator")
        self.geometry("420x620")
        self.minsize(360, 560)

        self.current_expression = ""
        self.current_result = "0"
        self.just_calculated = False

        self._create_widgets()
        self._bind_keys()
        self._update_display()

    def _create_widgets(self) -> None:
        self.main_frame = ctk.CTkFrame(self, corner_radius=24)
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=16)
        self.main_frame.grid_columnconfigure(0, weight=1)
        for column_index in range(4):
            self.main_frame.grid_columnconfigure(column_index, weight=1)

        title_label = ctk.CTkLabel(
            self.main_frame,
            text="SMART CALCULATOR",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=(24, 10), sticky="ew")

        self.expression_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=20),
            anchor="e",
            justify="right",
            wraplength=360,
        )
        self.expression_label.grid(row=1, column=0, columnspan=4, padx=20, pady=(16, 4), sticky="ew")

        separator = ctk.CTkFrame(self.main_frame, height=2, corner_radius=0)
        separator.grid(row=2, column=0, columnspan=4, padx=24, pady=(0, 6), sticky="ew")

        self.result_label = ctk.CTkLabel(
            self.main_frame,
            text="0",
            font=ctk.CTkFont(size=36, weight="bold"),
            anchor="e",
            justify="right",
            wraplength=360,
        )
        self.result_label.grid(row=3, column=0, columnspan=4, padx=20, pady=(0, 18), sticky="ew")

        buttons = [
            ("C", self.clear_all, "secondary"),
            ("⌫", self.backspace, "secondary"),
            ("%", self.apply_percentage, "secondary"),
            ("÷", lambda: self.add_operator("/"), "operator"),
            ("7", lambda: self.add_digit("7"), "number"),
            ("8", lambda: self.add_digit("8"), "number"),
            ("9", lambda: self.add_digit("9"), "number"),
            ("×", lambda: self.add_operator("*"), "operator"),
            ("4", lambda: self.add_digit("4"), "number"),
            ("5", lambda: self.add_digit("5"), "number"),
            ("6", lambda: self.add_digit("6"), "number"),
            ("-", lambda: self.add_operator("-"), "operator"),
            ("1", lambda: self.add_digit("1"), "number"),
            ("2", lambda: self.add_digit("2"), "number"),
            ("3", lambda: self.add_digit("3"), "number"),
            ("+", lambda: self.add_operator("+"), "operator"),
            ("+/-", self.toggle_current_sign, "secondary"),
            ("0", lambda: self.add_digit("0"), "number"),
            (".", lambda: self.add_decimal_point(), "number"),
            ("=", self.calculate_result, "equals"),
        ]

        row_index = 4
        column_index = 0
        for text, command, button_type in buttons:
            button = self._create_button(text, command, button_type)
            button.grid(row=row_index, column=column_index, padx=8, pady=8, sticky="nsew")
            column_index += 1
            if column_index == 4:
                column_index = 0
                row_index += 1

        for row_number in range(4, 9):
            self.main_frame.grid_rowconfigure(row_number, weight=1)

    def _create_button(self, text: str, command, button_type: str) -> ctk.CTkButton:
        if button_type == "equals":
            return ctk.CTkButton(
                self.main_frame,
                text=text,
                command=command,
                corner_radius=18,
                height=60,
                font=ctk.CTkFont(size=22, weight="bold"),
                fg_color=("#2F80ED", "#1F6FEB"),
                hover_color=("#2563EB", "#1D4ED8"),
            )

        if button_type == "operator":
            return ctk.CTkButton(
                self.main_frame,
                text=text,
                command=command,
                corner_radius=18,
                height=60,
                font=ctk.CTkFont(size=22, weight="bold"),
                fg_color=("#4B5563", "#374151"),
                hover_color=("#6B7280", "#4B5563"),
            )

        if button_type == "secondary":
            return ctk.CTkButton(
                self.main_frame,
                text=text,
                command=command,
                corner_radius=18,
                height=60,
                font=ctk.CTkFont(size=22, weight="bold"),
                fg_color=("#334155", "#1F2937"),
                hover_color=("#475569", "#374151"),
            )

        return ctk.CTkButton(
            self.main_frame,
            text=text,
            command=command,
            corner_radius=18,
            height=60,
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color=("#1F2937", "#111827"),
            hover_color=("#374151", "#1F2937"),
        )

    def _bind_keys(self) -> None:
        self.bind("<Key>", self.handle_key_press)

    def _update_display(self) -> None:
        self.expression_label.configure(text=self.current_expression)
        self.result_label.configure(text=self.current_result)

    def _show_error(self, message: str) -> None:
        self.current_result = message
        self.just_calculated = False
        self._update_display()

    def _get_current_number_range(self) -> tuple[int, int]:
        """Return the start and end positions of the current number."""
        if not self.current_expression:
            return 0, 0

        end_index = len(self.current_expression)
        start_index = end_index - 1

        while start_index >= 0 and (self.current_expression[start_index].isdigit() or self.current_expression[start_index] == "."):
            start_index -= 1

        # Include a unary minus sign if it belongs to this number.
        if start_index >= 0 and self.current_expression[start_index] == "-":
            if start_index == 0 or self.current_expression[start_index - 1] in "+-*/":
                start_index -= 1

        return start_index + 1, end_index

    def _get_current_number(self) -> str:
        start_index, end_index = self._get_current_number_range()
        return self.current_expression[start_index:end_index]

    def _replace_current_number(self, new_number: str) -> None:
        if not self.current_expression:
            self.current_expression = new_number
            return

        start_index, end_index = self._get_current_number_range()
        self.current_expression = self.current_expression[:start_index] + new_number + self.current_expression[end_index:]

    def add_digit(self, digit: str) -> None:
        if self.current_result in {"Invalid expression.", "Cannot divide by zero.", "Please enter a number."}:
            self.clear_all()

        if self.just_calculated:
            self.current_expression = ""
            self.current_result = "0"
            self.just_calculated = False

        if self.current_expression and self.current_expression[-1] == "0":
            current_number = self._get_current_number()
            if current_number == "0":
                self.current_expression = self.current_expression[:-1] + digit
            else:
                self.current_expression += digit
        else:
            self.current_expression += digit

        self._preview_result()

    def add_decimal_point(self) -> None:
        if self.current_result in {"Invalid expression.", "Cannot divide by zero.", "Please enter a number."}:
            self.clear_all()

        if self.just_calculated:
            self.current_expression = ""
            self.current_result = "0"
            self.just_calculated = False

        current_number = self._get_current_number()
        if "." in current_number:
            return

        if not current_number or current_number in "+-*/":
            self.current_expression += "0."
        else:
            self.current_expression += "."

        self._preview_result()

    def add_operator(self, operator: str) -> None:
        if self.current_result in {"Invalid expression.", "Cannot divide by zero.", "Please enter a number."}:
            self.clear_all()

        if self.just_calculated:
            self.current_expression = self.current_result if self.current_result not in {"0", ""} else self.current_expression
            self.just_calculated = False

        if not self.current_expression:
            if operator == "-":
                self.current_expression = "-"
            return

        if self.current_expression[-1] in "+-*/":
            self.current_expression = self.current_expression[:-1] + operator
        else:
            self.current_expression += operator

        self._preview_result()

    def clear_all(self) -> None:
        self.current_expression = ""
        self.current_result = "0"
        self.just_calculated = False
        self._update_display()

    def backspace(self) -> None:
        if self.current_result in {"Invalid expression.", "Cannot divide by zero.", "Please enter a number."}:
            self.current_result = "0"
        self.just_calculated = False

        self.current_expression = self.current_expression[:-1]
        self._preview_result()

    def apply_percentage(self) -> None:
        current_number = self._get_current_number()
        if not current_number:
            self._show_error("Please enter a number.")
            return

        try:
            converted_number = to_percentage(current_number)
        except ValueError as error:
            self._show_error(str(error))
            return

        self._replace_current_number(converted_number)
        self._preview_result()

    def toggle_current_sign(self) -> None:
        current_number = self._get_current_number()
        if not current_number:
            self._show_error("Please enter a number.")
            return

        try:
            changed_number = toggle_sign(current_number)
        except ValueError as error:
            self._show_error(str(error))
            return

        self._replace_current_number(changed_number)
        self._preview_result()

    def calculate_result(self) -> None:
        try:
            self.current_result = calculate(self.current_expression)
        except ZeroDivisionError as error:
            self.current_result = str(error)
        except ValueError as error:
            self.current_result = str(error)

        self.just_calculated = self.current_result not in {"Invalid expression.", "Cannot divide by zero.", "Please enter a number."}
        self._update_display()

    def _preview_result(self) -> None:
        if not self.current_expression:
            self.current_result = "0"
            self.just_calculated = False
        else:
            try:
                self.current_result = calculate(self.current_expression)
                self.just_calculated = False
            except (ValueError, ZeroDivisionError):
                # If the expression is incomplete, we simply keep the last
                # valid result or show a neutral 0.
                if self.current_result not in {"Invalid expression.", "Cannot divide by zero.", "Please enter a number."}:
                    self.current_result = "0"

        self._update_display()

    def handle_key_press(self, event) -> None:
        key = event.keysym
        char = event.char

        if char.isdigit():
            self.add_digit(char)
            return

        if char in "+-*/":
            self.add_operator(char)
            return

        if char == ".":
            self.add_decimal_point()
            return

        if char == "%":
            self.apply_percentage()
            return

        if key == "Return":
            self.calculate_result()
            return

        if key == "BackSpace":
            self.backspace()
            return

        if key == "Escape":
            self.clear_all()
