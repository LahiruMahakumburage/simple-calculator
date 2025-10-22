

#
import tkinter as tk
from tkinter import messagebox


class SimpleCalculator:
    def __init__(self):
        # STEP 1: Create the main window
        self.window = tk.Tk()
        self.window.title("Begiber Calculator")
        self.window.geometry("300x450")

        # STEP 2: Create variables to store numbers
        self.display_text = tk.StringVar()  # What shows on screen
        self.display_text.set("0")          # Start with "0"

        self. first_number = ""              # First number in calculation
        self.operation = ""                 # +, -, ×, ÷
        self.current_number = "0"           # Number being typed now

        # STEP 3: Create the calculator interface
        self.make_display()
        self.make_buttons()

    def make_display(self):

        screen = tk.Entry(
            self.window,
            textvariable=self.display_text,
            font=("Arial", 20),
            justify="right",
            state="readonly"
        )
        screen.pack(pady=10, padx=10, fill="x")

    def make_buttons(self):

        # Create a frame to hold all buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        # ROW 1: Clear, +/-, %, ÷
        self.create_button("C", 0, 0, button_frame, "lightcoral")
        self.create_button("±", 0, 1, button_frame, "lightgray")
        self.create_button("%", 0, 2, button_frame, "lightgray")
        self.create_button("÷", 0, 3, button_frame, "orange")

        # ROW 2: 7, 8, 9, ×
        self.create_button("7", 1, 0, button_frame)
        self.create_button("8", 1, 1, button_frame)
        self.create_button("9", 1, 2, button_frame)
        self.create_button("×", 1, 3, button_frame, "orange")

        # ROW 3: 4, 5, 6, -
        self.create_button("4", 2, 0, button_frame)
        self.create_button("5", 2, 1, button_frame)
        self.create_button("6", 2, 2, button_frame)
        self.create_button("-", 2, 3, button_frame, "orange")

        # ROW 4: 1, 2, 3, +
        self.create_button("1", 3, 0, button_frame)
        self.create_button("2", 3, 1, button_frame)
        self.create_button("3", 3, 2, button_frame)
        self.create_button("+", 3, 3, button_frame, "orange")

        # ROW 5: 0 (wide), ., =
        zero_btn = tk.Button(
            button_frame,
            text="0",
            font=("Arial", 16),
            width=8,
            height=2,
            command=lambda: self.button_pressed("0")
        )
        zero_btn.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

        self.create_button(".", 4, 2, button_frame)
        self.create_button("=", 4, 3, button_frame, "lightgreen")

    def create_button(self, text, row, col, parent, color="lightblue"):
        """Helper function to create a single button"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 16),
            width=4,
            height=2,
            bg=color,
            command=lambda: self.button_pressed(text)
        )
        btn.grid(row=row, column=col, padx=2, pady=2)

    def button_pressed(self, button_text):
        """This function runs when ANY button is clicked"""

        # Check button pressed
        if button_text.isdigit():           # Numbers 0-9
            self.add_digit(button_text)

        elif button_text == ".":            # Decimal point
            self.add_decimal()

        elif button_text in "+-×÷":        # Operation buttons
            self.set_operation(button_text)

        elif button_text == "=":           # Equals button
            self.calculate_result()

        elif button_text == "C":           # Clear button
            self.clear_all()

        elif button_text == "±":           # Plus/minus button
            self.change_sign()

        elif button_text == "%":           # Percentage button
            self.make_percentage()

    def add_digit(self, digit):
        """Adds a number digit to the display"""
        if self.current_number == "0":
            self.current_number = digit
        else:
            self.current_number = self.current_number + digit

        self.display_text.set(self.current_number)

    def add_decimal(self):
        """Adds decimal point if not already present"""
        if "." not in self.current_number:
            self.current_number = self.current_number + "."
            self.display_text.set(self.current_number)

    def set_operation(self, op):
        """Stores the operation and first number"""
        # If we already have an operation, calculate first
        if self.operation and self.first_number:
            self.calculate_result()

        # Store the first number and operation
        self.first_number = self.current_number
        self.operation = op
        self.current_number = "0"

    def calculate_result(self):
        """Does the actual math calculation"""
        # Make sure we have everything needed
        if not self.operation or not self.first_number:
            return

        try:
            # Convert text to numbers
            num1 = float(self.first_number)
            num2 = float(self.current_number)

            # Do the math based on operation
            if self.operation == "+":
                answer = num1 + num2
            elif self.operation == "-":
                answer = num1 - num2
            elif self.operation == "×":
                answer = num1 * num2
            elif self.operation == "÷":
                if num2 == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    self.clear_all()
                    return
                answer = num1 / num2

            # Show the result
            self.current_number = str(answer)
            self.display_text.set(self.current_number)

            # Clear operation for next calculation
            self.operation = ""
            self.first_number = ""

        except:
            messagebox.showerror("Error", "Something went wrong!")
            self.clear_all()

    def clear_all(self):
        """Resets calculator to starting state"""
        self.current_number = "0"
        self.first_number = ""
        self.operation = ""
        self.display_text.set("0")

    def change_sign(self):
        """Changes positive to negative or vice versa"""
        if self.current_number != "0":
            if self.current_number.startswith("-"):
                self.current_number = self.current_number[1:]  # Remove minus
            else:
                self.current_number = "-" + self.current_number  # Add minus

            self.display_text.set(self.current_number)

    def make_percentage(self):
        """Converts current number to percentage"""
        try:
            number = float(self.current_number)
            result = number / 100
            self.current_number = str(result)
            self.display_text.set(self.current_number)
        except:
            pass

    def start_calculator(self):
        """Starts the calculator and keeps it running"""
        self.window.mainloop()


# START THE PROGRAM
# =================
if __name__ == "__main__":
    # Create a calculator
    my_calculator = SimpleCalculator()

    # Start it running
    my_calculator.start_calculator()
