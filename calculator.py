import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

class AdvancedCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Calculator")
        self.window.geometry("450x600")  # Increased height for new row
        self.window.minsize(400, 550)
        
        # Hide console (Windows only)
        if os.name == 'nt':
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except:
                pass
        
        # Default settings
        self.settings = {
            "language": "russian",
            "theme": "dark",
            "precision": 10
        }
        
        # Load settings
        self.load_settings()
        
        # Localizations
        self.languages = {
            "russian": {
                "title": "Продвинутый калькулятор",
                "power_prompt": "ⁿ (введите степень)",
                "operations": ["C", "⌫", "±", "%", "7", "8", "9", "/", "4", "5", "6", "*", 
                             "1", "2", "3", "-", "xⁿ", "0", ".", "+", "="],
                "settings_title": "Настройки",
                "language_label": "Язык:",
                "theme_label": "Тема:",
                "precision_label": "Цифры после точки:",
                "save_btn": "Сохранить",
                "error_division": "Деление на ноль!",
                "error_input": "Некорректный ввод!"
            },
            "english": {
                "title": "Advanced Calculator",
                "power_prompt": "ⁿ (enter power)",
                "operations": ["C", "⌫", "±", "%", "7", "8", "9", "/", "4", "5", "6", "*", 
                             "1", "2", "3", "-", "xⁿ", "0", ".", "+", "="],
                "settings_title": "Settings",
                "language_label": "Language:",
                "theme_label": "Theme:",
                "precision_label": "Digits after point:",
                "save_btn": "Save",
                "error_division": "Division by zero!",
                "error_input": "Invalid input!"
            }
        }
        
        # Themes
        self.themes = {
            "dark": {
                "bg": "#2C2C2C",
                "display_bg": "#1A1A1A",
                "display_fg": "white",
                "label_fg": "#888888",
                "numbers_bg": "#404040",
                "numbers_fg": "white",
                "operations_bg": "#FF9500",
                "operations_fg": "white",
                "special_bg": "#A6A6A6",
                "special_fg": "black"
            },
            "light": {
                "bg": "#F0F0F0",
                "display_bg": "white",
                "display_fg": "black",
                "label_fg": "#666666",
                "numbers_bg": "#E0E0E0",
                "numbers_fg": "black",
                "operations_bg": "#FF9500",
                "operations_fg": "white",
                "special_bg": "#C0C0C0",
                "special_fg": "black"
            },
            "blue": {
                "bg": "#1E3A5F",
                "display_bg": "#0A1F3A",
                "display_fg": "white",
                "label_fg": "#88AAFF",
                "numbers_bg": "#2A4A7F",
                "numbers_fg": "white",
                "operations_bg": "#FF6B35",
                "operations_fg": "white",
                "special_bg": "#4A76B4",
                "special_fg": "white"
            }
        }
        
        self.current_lang = self.languages[self.settings["language"]]
        self.current_theme = self.themes[self.settings["theme"]]
        
        # Calculator variables
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.power_mode = False
        self.power_base = None
        self.power_count = ""
        self.new_input = True  # Flag for new input
        
        self.setup_ui()
        
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("calculator_settings.json"):
                with open("calculator_settings.json", "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except:
            pass  # Use default settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open("calculator_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def setup_ui(self):
        """Create interface"""
        self.window.configure(bg=self.current_theme["bg"])
        self.window.title(self.current_lang["title"])
        
        self.create_display()
        self.create_buttons()
        self.create_settings_button()
        
    def create_display(self):
        """Create input field"""
        # Main display
        self.display = tk.Entry(self.window, font=('Arial', 24), 
                               justify='right', bd=10, relief='flat',
                               bg=self.current_theme["display_bg"], 
                               fg=self.current_theme["display_fg"])
        self.display.grid(row=0, column=0, columnspan=4, sticky='we', padx=10, pady=10)
        
        # Operation label
        self.operation_label = tk.Label(self.window, font=('Arial', 12), 
                                       bg=self.current_theme["bg"], 
                                       fg=self.current_theme["label_fg"])
        self.operation_label.grid(row=1, column=0, columnspan=4, sticky='w', padx=15)
        
    def create_settings_button(self):
        """Settings button in top-left corner"""
        settings_btn = tk.Button(self.window, text="⚙", font=('Arial', 14),
                                bg=self.current_theme["special_bg"],
                                fg=self.current_theme["special_fg"],
                                width=3, height=1,
                                command=self.open_settings)
        settings_btn.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
    
    def create_buttons(self):
        """Create calculator buttons"""
        buttons = [
            ['C', '⌫', '±', '%'],    # Percent button is back!
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['xⁿ', '0', '.', '+'],
            ['', '', '', '=']        # Equal button on separate row
        ]
        
        for row, row_buttons in enumerate(buttons):
            for col, text in enumerate(row_buttons):
                if text:  # Skip empty buttons
                    btn = self.create_button(text, row, col)
        
        # Make equal button span 4 columns and be larger
        equal_btn = tk.Button(self.window, text="=", font=('Arial', 18),
                             bg=self.current_theme["operations_bg"],
                             fg=self.current_theme["operations_fg"], bd=0, relief='flat',
                             command=lambda: self.button_click('='))
        equal_btn.grid(row=7, column=0, columnspan=4, sticky='news', padx=2, pady=2)
        
        # Responsive sizing
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)
        for i in range(2, 8):  # Increased row range
            self.window.grid_rowconfigure(i, weight=1)
    
    def create_button(self, text, row, col):
        """Create single button"""
        if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            bg = self.current_theme["numbers_bg"]
            fg = self.current_theme["numbers_fg"]
        elif text in ['/', '*', '-', '+', '=', 'xⁿ']:
            bg = self.current_theme["operations_bg"]
            fg = self.current_theme["operations_fg"]
        else:
            bg = self.current_theme["special_bg"]
            fg = self.current_theme["special_fg"]
        
        btn = tk.Button(self.window, text=text, font=('Arial', 18),
                       bg=bg, fg=fg, bd=0, relief='flat',
                       command=lambda t=text: self.button_click(t))
        btn.grid(row=row+2, column=col, sticky='news', padx=2, pady=2)
        return btn
    
    def open_settings(self):
        """Settings window"""
        settings_window = tk.Toplevel(self.window)
        settings_window.title(self.current_lang["settings_title"])
        settings_window.geometry("300x250")
        settings_window.configure(bg=self.current_theme["bg"])
        settings_window.resizable(False, False)
        
        # Center settings window
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Language
        tk.Label(settings_window, text=self.current_lang["language_label"],
                bg=self.current_theme["bg"], fg=self.current_theme["display_fg"]).pack(pady=5)
        lang_var = tk.StringVar(value=self.settings["language"])
        lang_combo = ttk.Combobox(settings_window, textvariable=lang_var,
                                 values=["russian", "english"], state="readonly")
        lang_combo.pack(pady=5)
        
        # Theme
        tk.Label(settings_window, text=self.current_lang["theme_label"],
                bg=self.current_theme["bg"], fg=self.current_theme["display_fg"]).pack(pady=5)
        theme_var = tk.StringVar(value=self.settings["theme"])
        theme_combo = ttk.Combobox(settings_window, textvariable=theme_var,
                                  values=["dark", "light", "blue"], state="readonly")
        theme_combo.pack(pady=5)
        
        # Digits after point
        tk.Label(settings_window, text=self.current_lang["precision_label"],
                bg=self.current_theme["bg"], fg=self.current_theme["display_fg"]).pack(pady=5)
        precision_var = tk.StringVar(value=str(self.settings["precision"]))
        precision_combo = ttk.Combobox(settings_window, textvariable=precision_var,
                                      values=["2", "5", "10", "15"], state="readonly")
        precision_combo.pack(pady=5)
        
        def save_and_close():
            self.settings.update({
                "language": lang_var.get(),
                "theme": theme_var.get(),
                "precision": int(precision_var.get())
            })
            self.save_settings()
            settings_window.destroy()
            self.apply_settings()
        
        tk.Button(settings_window, text=self.current_lang["save_btn"],
                 command=save_and_close, bg=self.current_theme["operations_bg"],
                 fg="white", font=('Arial', 12)).pack(pady=20)
    
    def apply_settings(self):
        """Apply new settings"""
        self.current_lang = self.languages[self.settings["language"]]
        self.current_theme = self.themes[self.settings["theme"]]
        
        # Update entire interface
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.setup_ui()
    
    def button_click(self, text):
        """Handle button clicks"""
        if text in '0123456789':
            self.input_number(text)
        elif text in ['+', '-', '*', '/']:
            self.input_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':  # Backspace button
            self.backspace()
        elif text == '±':
            self.plus_minus()
        elif text == '%':  # Percentage button - now it's back!
            self.percentage()
        elif text == 'xⁿ':
            self.power_function()
        elif text == '.':
            self.input_decimal()
    
    def backspace(self):
        """Delete last character"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display()
    
    def input_number(self, num):
        """Input number"""
        if self.power_mode:
            if self.power_base is not None:
                self.power_count += num
                self.operation_label.config(text=f"{self.power_base}ⁿ = {self.power_base}" + 
                                           f" × {self.power_base}" * (int(self.power_count or 0) - 1))
            return
            
        # If it's new input (after operation), clear field
        if self.new_input:
            self.current_input = ""
            self.new_input = False
            
        if self.current_input == "0":
            self.current_input = num
        else:
            self.current_input += num
        self.update_display()
    
    def power_function(self):
        """Activate power mode"""
        if self.current_input:
            self.power_mode = True
            self.power_base = float(self.current_input)
            self.power_count = ""
            self.operation_label.config(text=f"{self.current_input}{self.current_lang['power_prompt']}")
            self.current_input = ""
            self.new_input = True
            self.update_display()
        elif self.power_mode and self.power_count:
            self.calculate_power()
    
    def calculate_power(self):
        """Calculate power"""
        if self.power_base is not None and self.power_count:
            try:
                exponent = int(self.power_count)
                if exponent >= 0:
                    result = self.power_base ** exponent
                    # Beautiful operation display
                    operation_text = f"{self.power_base}ⁿ = {self.power_base}"
                    if exponent > 1:
                        operation_text += " × " + " × ".join([str(self.power_base)] * (exponent - 1))
                    operation_text += f" = {result}"
                    self.operation_label.config(text=operation_text)
                    
                    # Round result according to settings
                    result_str = str(round(result, self.settings["precision"]))
                    # Remove trailing zeros after point
                    if '.' in result_str:
                        result_str = result_str.rstrip('0').rstrip('.')
                    
                    self.current_input = result_str
                    self.update_display()
                
                self.power_mode = False
                self.power_base = None
                self.power_count = ""
                self.new_input = True
                
            except ValueError:
                self.show_error(self.current_lang["error_input"])
    
    def calculate(self):
        """Main calculations"""
        if self.power_mode and self.power_count:
            self.calculate_power()
            return
            
        if self.previous_input and self.current_input and self.operation:
            try:
                prev = float(self.previous_input)
                curr = float(self.current_input)
                
                operations = {
                    '+': prev + curr,
                    '-': prev - curr,
                    '*': prev * curr,
                    '/': prev / curr if curr != 0 else None
                }
                
                if self.operation == '/' and curr == 0:
                    self.show_error(self.current_lang["error_division"])
                    return
                
                result = operations[self.operation]
                
                # Round and remove trailing zeros
                result_str = str(round(result, self.settings["precision"]))
                if '.' in result_str:
                    result_str = result_str.rstrip('0').rstrip('.')
                
                self.current_input = result_str
                self.previous_input = ""
                self.operation = None
                self.new_input = True
                self.update_display()
                self.operation_label.config(text="")
                
            except ValueError:
                self.show_error(self.current_lang["error_input"])
        elif self.operation and not self.current_input:
            # If "=" pressed without second number, use previous result
            self.current_input = self.previous_input
            self.calculate()
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.clear()
    
    def clear(self):
        """Clear calculator"""
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.power_mode = False
        self.power_base = None
        self.power_count = ""
        self.new_input = True
        self.update_display()
        self.operation_label.config(text="")
    
    def plus_minus(self):
        """Change sign"""
        if self.current_input and self.current_input != "0":
            self.current_input = str(-float(self.current_input))
            self.update_display()
    
    def percentage(self):
        """Percentage calculation"""
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                # Remove trailing zeros
                value_str = str(value).rstrip('0').rstrip('.') if '.' in str(value) else str(value)
                self.current_input = value_str
                self.update_display()
            except ValueError:
                self.show_error(self.current_lang["error_input"])
    
    def input_decimal(self):
        """Input decimal point"""
        if '.' not in self.current_input:
            self.current_input += '.' if self.current_input else "0."
            self.update_display()
    
    def input_operation(self, op):
        """Input operation"""
        if self.power_mode and self.power_count:
            self.calculate_power()
            return
            
        if self.current_input:
            # If operation already exists, calculate first
            if self.previous_input and self.operation:
                self.calculate()
            
            self.operation = op
            self.previous_input = self.current_input
            self.current_input = ""
            self.new_input = True
            self.operation_label.config(text=f"{self.previous_input} {self.operation}")
        elif self.previous_input and not self.current_input:
            # Change operation if second number not entered
            self.operation = op
            self.operation_label.config(text=f"{self.previous_input} {self.operation}")
    
    def update_display(self):
        """Update display"""
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input or "0")
    
    def run(self):
        """Run application"""
        self.window.mainloop()

# Launch
if __name__ == "__main__":
    calc = AdvancedCalculator()
    calc.run()