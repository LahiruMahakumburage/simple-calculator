import tkinter as tk
from tkinter import font

# --- Main Application Class (Inherits from tk.Tk) ---
# This class represents the main calculator window


class CalculatorApp(tk.Tk):

    def __init__(self):
        """
        Constructor for the main application window.
        """
        # Call the parent class (tk.Tk) constructor
        super().__init__()

        # --- Window Setup ---
        self.title("Calculator")
        self.geometry('400x500')
        self.configure(bg="black")  # Set a background color

        # --- State Variable ---
        # This will hold the string to be evaluated, e.g., "12+5"
        self.expression = ""

        # --- Define Fonts ---
        self.display_font = font.Font(family="Helvetica", size=32)

        # --- Create Widgets ---

        # 1. Create the Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")  # Start with "0"

        # The display is an Entry widget, but set to 'readonly'
        self.display_entry = tk.Entry(
            self,
            textvariable=self.display_var,
            font=self.display_font,
            # --- THIS IS THE UPDATED LINE ---
            fg="#000000",  # Changed from "white" to a light green
            # --- END OF UPDATE ---
            bg="black",
            bd=0,  # No border
            justify='right',  # Align text to the right
            state='readonly'  # Disables typing directly into the display
        )
        # Use pack for the display, making it fill the width
        self.display_entry.pack(fill='x', padx=10, pady=20)

        # 2. Create the Frame for Buttons
        self.button_frame = ButtonFrame(self)
        self.button_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 3. (Optional) Bind keyboard
        self.bind("<Key>", self.on_key_press)

    # --- Logic Methods ---

    def on_button_click(self, char):
        """
        Called when a number or operator button is pressed.
        Appends the character to the 'expression' string.
        """
        current_display = self.display_var.get()
        char_str = str(char)

        if current_display.startswith("Error"):
            self.expression = char_str
        elif self.expression == "0" and char_str not in "0.":
            self.expression = char_str
        elif self.expression == "0" and char_str == "0":
            return
        else:
            self.expression += char_str

        self.display_var.set(self.expression)

    def on_clear(self):
        """
        Called when the 'AC' (All Clear) button is pressed.
        """
        self.expression = ""
        self.display_var.set("0")

    def on_equals(self):
        """
        Called when the '=' button is pressed.
        Evaluates the 'expression' string and handles errors.
        """
        if not self.expression:
            return

        try:
            safe_expression = self.expression.replace(
                '×', '*').replace('÷', '/')
            result = str(eval(safe_expression))
            self.display_var.set(result)
            self.expression = result

        except ZeroDivisionError:
            self.display_var.set("Error: Div by zero")
            # --- ADD THIS LINE ---
            self.display_entry.config(fg="red")
            self.expression = ""
        except SyntaxError:
            self.display_var.set("Error: Invalid Syntax")
            # --- ADD THIS LINE ---
            self.display_entry.config(fg="red")
            self.expression = ""
        except Exception as e:
            self.display_var.set("Error")
            # --- ADD THIS LINE ---
            self.display_entry.config(fg="red")
            self.expression = ""

    def on_key_press(self, event):
        """
        Handles keyboard input for better usability.
        """
        key = event.char
        keysym = event.keysym

        if key in '0123456789.':
            self.on_button_click(key)
        elif key == '+':
            self.on_button_click('+')
        elif key == '-':
            self.on_button_click('-')
        elif key == '*':
            self.on_button_click('×')
        elif key == '/':
            self.on_button_click('÷')
        elif keysym == 'Return' or key == '\r' or key == '=':
            self.on_equals()
        elif keysym == 'Escape' or keysym == 'Delete':
            self.on_clear()
        elif keysym == 'BackSpace':
            self.expression = self.expression[:-1]
            if not self.expression:
                self.display_var.set("0")
            else:
                self.display_var.set(self.expression)


# --- Button Frame Class (Inherits from tk.Frame) ---
class ButtonFrame(tk.Frame):

    def __init__(self, parent):
        """
        Constructor for the button frame.
        'parent' here is the main CalculatorApp instance.
        """
        super().__init__(parent, bg="black")

        self.app = parent

        # --- Define Fonts and Colors ---
        button_font = font.Font(family="Helvetica", size=18)
        num_bg = "#505050"
        op_bg = "#FF9500"
        special_bg = "#D4D4D2"
        text_color = "white"
        special_text_color = "Black"

        # --- Define Button Layout ---
        buttons = [
            ('AC', 1, 0, 3, self.app.on_clear, special_bg, special_text_color),
            ('÷',  1, 3, 1, lambda: self.app.on_button_click('÷'), op_bg, text_color),

            ('7',  2, 0, 1, lambda: self.app.on_button_click(7), num_bg, text_color),
            ('8',  2, 1, 1, lambda: self.app.on_button_click(8), num_bg, text_color),
            ('9',  2, 2, 1, lambda: self.app.on_button_click(9), num_bg, text_color),
            ('×',  2, 3, 1, lambda: self.app.on_button_click('×'), op_bg, text_color),

            ('4',  3, 0, 1, lambda: self.app.on_button_click(4), num_bg, text_color),
            ('5',  3, 1, 1, lambda: self.app.on_button_click(5), num_bg, text_color),
            ('6',  3, 2, 1, lambda: self.app.on_button_click(6), num_bg, text_color),
            ('-',  3, 3, 1, lambda: self.app.on_button_click('-'), op_bg, text_color),

            ('1',  4, 0, 1, lambda: self.app.on_button_click(1), num_bg, text_color),
            ('2',  4, 1, 1, lambda: self.app.on_button_click(2), num_bg, text_color),
            ('3',  4, 2, 1, lambda: self.app.on_button_click(3), num_bg, text_color),
            ('+',  4, 3, 1, lambda: self.app.on_button_click('+'), op_bg, text_color),

            ('0',  5, 0, 2, lambda: self.app.on_button_click(0), num_bg, text_color),
            ('.',  5, 2, 1, lambda: self.app.on_button_click('.'), num_bg, text_color),
            ('=',  5, 3, 1, self.app.on_equals, op_bg, text_color),
        ]

        # --- Create and Place Buttons ---
        for (text, row, col, col_span, cmd, bg, fg) in buttons:
            btn = tk.Button(
                self,
                text=text,
                font=button_font,
                command=cmd,
                bg=bg,
                fg=fg,
                bd=0,
                padx=20,
                pady=20
            )
            btn.grid(row=row, column=col, columnspan=col_span,
                     sticky="nsew", padx=2, pady=2)

        # --- Configure Grid to be Responsive ---
        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)


# --- Main execution ---
if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
