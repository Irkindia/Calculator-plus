import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import traceback
from decimal import Decimal, getcontext

# Import localization system
try:
    from lang import en, ru
    HAS_LANGS = True
except ImportError:
    HAS_LANGS = False

def show_error_dialog(message):
    """Show error dialog with details"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Calculator Error", message)
    root.destroy()

try:
    import requests
    from packaging import version
    HAS_DEPENDENCIES = True
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    HAS_DEPENDENCIES = False

class AdvancedCalculator:
    def __init__(self):
        try:
            self.window = tk.Tk()
            self.window.title("Calculator Plus v1.1.0")
            self.window.geometry("450x600")
            self.window.minsize(400, 550)
            
            # Hide console window on Windows
            if os.name == 'nt':
                try:
                    import ctypes
                    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
                except:
                    pass
            
            # Check for updates only if dependencies are available
            if HAS_DEPENDENCIES:
                update_info = self.check_updates()
                if update_info:
                    messagebox.showinfo("Update Available", update_info)
            
            self.setup_calculator()
            
        except Exception as e:
            error_msg = f"Failed to initialize calculator:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            print(error_msg)
            show_error_dialog(error_msg)
            sys.exit(1)
    
    def check_updates(self):
        """Check for updates from GitHub"""
        try:
            GITHUB_URL = "https://api.github.com/repos/Irkindia/calculator-plus/releases/latest"
            response = requests.get(GITHUB_URL, timeout=5)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release['tag_name']
                current_version = "v1.1.0"
                
                if version.parse(latest_version) > version.parse(current_version):
                    return f"🎉 Update available {latest_version}!\n{latest_release['body']}\n\nDownload: https://github.com/Irkindia/calculator-plus"
            return None
        except:
            return None
    
    def setup_calculator(self):
        """Setup calculator components"""
        # Default settings
        self.settings = {
            "language": "russian", 
            "theme": "dark"
        }
        
        # Load settings from file
        self.load_settings()
        
        # Setup localization
        self.setup_localization()
        
        # Themes configuration
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
        
        self.current_theme = self.themes[self.settings["theme"]]
        
        # Calculator state variables
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.power_mode = False
        self.power_base = None
        self.power_count = ""
        self.new_input = True
        
        self.setup_ui()
    
    def setup_localization(self):
        """Setup localization system"""
        if not HAS_LANGS:
            # Minimal fallback translations
            self.languages = {
                "english": {
                    "title": "Calculator Plus",
                    "power_prompt": "ⁿ (enter power)",
                    "settings_title": "Settings",
                    "language_label": "Language:",
                    "theme_label": "Theme:",
                    "save_btn": "Save",
                    "error_division": "Division by zero!",
                    "error_input": "Invalid input!"
                },
                "russian": {
                    "title": "Калькулятор Плюс",
                    "power_prompt": "ⁿ (введите степень)",
                    "settings_title": "Настройки",
                    "language_label": "Язык:",
                    "theme_label": "Тема:",
                    "save_btn": "Сохранить",
                    "error_division": "Деление на ноль!",
                    "error_input": "Некорректный ввод!"
                }
            }
        else:
            # Use external language files
            self.languages = {
                "english": en.translations,
                "russian": ru.translations
            }
        
        self.current_lang = self.languages[self.settings["language"]]
    
    def get_text(self, key):
        """Get localized text by key"""
        return self.current_lang.get(key, key)
    
    def get_localized_themes(self):
        """Get theme names in current language"""
        if HAS_LANGS:
            return [
                self.get_text("theme_dark"),
                self.get_text("theme_light"), 
                self.get_text("theme_blue")
            ]
        else:
            return ["Dark", "Light", "Blue"]
    
    def get_localized_languages(self):
        """Get language names - each in its native form"""
        return ["Русский", "English"]
    
    def get_theme_key(self, localized_name):
        """Convert localized theme name back to key"""
        if HAS_LANGS:
            themes_map = {
                self.get_text("theme_dark"): "dark",
                self.get_text("theme_light"): "light", 
                self.get_text("theme_blue"): "blue"
            }
        else:
            themes_map = {"Dark": "dark", "Light": "light", "Blue": "blue"}
        return themes_map.get(localized_name, "dark")
    
    def get_language_key(self, localized_name):
        """Convert native language name back to key"""
        langs_map = {
            "Русский": "russian",
            "English": "english"
        }
        return langs_map.get(localized_name, "russian")
    
    def get_current_language_display(self):
        """Get current language in its native form"""
        if self.settings["language"] == "russian":
            return "Русский"
        else:
            return "English"
        
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists("calculator_settings.json"):
                with open("calculator_settings.json", "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except:
            pass
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open("calculator_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def setup_ui(self):
        """Initialize user interface"""
        self.window.configure(bg=self.current_theme["bg"])
        self.window.title(self.get_text("title"))
        
        self.create_display()
        self.create_buttons()
        self.create_settings_button()
        
    def create_display(self):
        """Create calculator display area"""
        # Main display entry
        self.display = tk.Entry(self.window, font=('Arial', 24), 
                               justify='right', bd=10, relief='flat',
                               bg=self.current_theme["display_bg"], 
                               fg=self.current_theme["display_fg"])
        self.display.grid(row=0, column=0, columnspan=4, sticky='we', padx=10, pady=10)
        
        # Operation display label
        self.operation_label = tk.Label(self.window, font=('Arial', 12), 
                                       bg=self.current_theme["bg"], 
                                       fg=self.current_theme["label_fg"])
        self.operation_label.grid(row=1, column=0, columnspan=4, sticky='w', padx=15)
        
    def create_settings_button(self):
        """Create settings button in top-left corner"""
        settings_btn = tk.Button(self.window, text="⚙", font=('Arial', 14),
                                bg=self.current_theme["special_bg"],
                                fg=self.current_theme["special_fg"],
                                width=3, height=1,
                                command=self.open_settings)
        settings_btn.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
    
    def create_buttons(self):
        """Create calculator buttons grid"""
        buttons = [
            [self.get_text("btn_clear"), self.get_text("btn_backspace"), self.get_text("btn_plus_minus"), self.get_text("btn_percent")],
            ['7', '8', '9', '÷'],  # Changed / to ÷
            ['4', '5', '6', '×'],  # Changed * to ×
            ['1', '2', '3', '-'],
            [self.get_text("btn_power"), '0', self.get_text("btn_decimal"), '+'],
            ['', '', '', self.get_text("btn_equals")]
        ]
        
        for row, row_buttons in enumerate(buttons):
            for col, text in enumerate(row_buttons):
                if text:  # Skip empty buttons
                    btn = self.create_button(text, row, col)
        
        # Create large equal button
        equal_btn = tk.Button(self.window, text=self.get_text("btn_equals"), font=('Arial', 18),
                             bg=self.current_theme["operations_bg"],
                             fg=self.current_theme["operations_fg"], bd=0, relief='flat',
                             command=lambda: self.button_click('='))
        equal_btn.grid(row=7, column=0, columnspan=4, sticky='news', padx=2, pady=2)
        
        # Configure grid responsiveness
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)
        for i in range(2, 8):
            self.window.grid_rowconfigure(i, weight=1)
    
    def create_button(self, text, row, col):
        """Create individual calculator button"""
        # Determine button color scheme
        if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            bg = self.current_theme["numbers_bg"]
            fg = self.current_theme["numbers_fg"]
        elif text in ['÷', '×', '-', '+', '=', 'xⁿ']:  # Added ÷ and ×
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
        settings_window.title(self.get_text("settings_title"))
        settings_window.geometry("300x220")  # Increased height for version
        settings_window.configure(bg=self.current_theme["bg"])
        settings_window.resizable(False, False)
        
        # Center settings window
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Language
        tk.Label(settings_window, text=self.get_text("language_label"),
                bg=self.current_theme["bg"], fg=self.current_theme["display_fg"]).pack(pady=5)
        lang_var = tk.StringVar(value=self.get_current_language_display())
        lang_combo = ttk.Combobox(settings_window, textvariable=lang_var,
                                 values=self.get_localized_languages(), state="readonly")
        lang_combo.pack(pady=5)
        
        # Theme
        tk.Label(settings_window, text=self.get_text("theme_label"),
                bg=self.current_theme["bg"], fg=self.current_theme["display_fg"]).pack(pady=5)
        theme_var = tk.StringVar(value=self.get_localized_themes()[["dark", "light", "blue"].index(self.settings["theme"])])
        theme_combo = ttk.Combobox(settings_window, textvariable=theme_var,
                                  values=self.get_localized_themes(), state="readonly")
        theme_combo.pack(pady=5)
        
        def save_and_close():
            self.settings.update({
                "language": self.get_language_key(lang_var.get()),
                "theme": self.get_theme_key(theme_var.get())
            })
            self.save_settings()
            settings_window.destroy()
            self.apply_settings()
        
        tk.Button(settings_window, text=self.get_text("save_btn"),
                 command=save_and_close, bg=self.current_theme["operations_bg"],
                 fg="white", font=('Arial', 12)).pack(pady=10)
        
        # Version info in bottom-right corner
        version_label = tk.Label(settings_window, text="v1.1.0", 
                                bg=self.current_theme["bg"], fg=self.current_theme["label_fg"],
                                font=('Arial', 8))
        version_label.pack(side='right', padx=5, pady=5)
    
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
        elif text in ['÷', '×', '-', '+']:  # Added ÷ and ×
            self.input_operation(text)
        elif text == '=':
            self.calculate()
        elif text == self.get_text("btn_clear"):
            self.clear()
        elif text == self.get_text("btn_backspace"):
            self.backspace()
        elif text == self.get_text("btn_plus_minus"):
            self.plus_minus()
        elif text == self.get_text("btn_percent"):
            self.percentage()
        elif text == self.get_text("btn_power"):
            self.power_function()
        elif text == self.get_text("btn_decimal"):
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
            self.operation_label.config(text=f"{self.current_input}{self.get_text('power_prompt')}")
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
                    
                    # Use Decimal for precise formatting
                    result_str = f"{result:.10f}"
                    result_str = result_str.rstrip('0').rstrip('.')
                    
                    self.current_input = result_str
                    self.update_display()
                
                self.power_mode = False
                self.power_base = None
                self.power_count = ""
                self.new_input = True
                
            except ValueError:
                self.show_error(self.get_text("error_input"))
    
    def calculate(self):
        """Main calculations with decimal precision"""
        if self.power_mode and self.power_count:
            self.calculate_power()
            return
            
        if self.previous_input and self.current_input and self.operation:
            try:
                # Use Decimal for precise calculations
                getcontext().prec = 20
                
                # Convert operation symbol for calculation
                operation = self.operation
                if operation == '÷':
                    operation = '/'
                elif operation == '×':
                    operation = '*'
                
                prev = Decimal(self.previous_input)
                curr = Decimal(self.current_input)
                
                operations = {
                    '+': prev + curr,
                    '-': prev - curr,
                    '*': prev * curr,
                    '/': prev / curr if curr != 0 else None
                }
                
                if operation == '/' and curr == 0:
                    self.show_error(self.get_text("error_division"))
                    return
                
                result = operations[operation]
                
                # Convert to string and format nicely
                result_str = f"{float(result):.10f}"  # Show up to 10 decimal places
                
                # Remove trailing zeros and unnecessary decimal point
                result_str = result_str.rstrip('0').rstrip('.')
                
                # Handle edge cases
                if result_str == '':
                    result_str = '0'
                elif result_str.startswith('.'):
                    result_str = '0' + result_str
                elif result_str.endswith('.'):
                    result_str = result_str[:-1]
                    
                self.current_input = result_str
                self.previous_input = ""
                self.operation = None
                self.new_input = True
                self.update_display()
                self.operation_label.config(text="")
                
            except ValueError:
                self.show_error(self.get_text("error_input"))
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
                value_str = f"{value:.10f}"
                value_str = value_str.rstrip('0').rstrip('.')
                if value_str == '':
                    value_str = '0'
                self.current_input = value_str
                self.update_display()
            except ValueError:
                self.show_error(self.get_text("error_input"))
    
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

def main():
    """Main entry point with error handling"""
    try:
        calculator = AdvancedCalculator()
        calculator.run()
    except Exception as e:
        error_msg = f"Fatal error:\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        show_error_dialog(error_msg)

if __name__ == "__main__":
    main()