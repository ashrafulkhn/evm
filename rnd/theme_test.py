import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self):
        # Define color schemes for day and night mode
        self.themes = {
            "day": {
                "bg": "#f9f9f9",  # Light background
                "fg": "#000000",  # Dark text
                "button_bg": "#ffffff",
                "button_fg": "#000000",
                "frame_bg": "#e0e0e0"
            },
            "night": {
                "bg": "#2c2c2c",  # Dark background
                "fg": "#ffffff",  # Light text
                "button_bg": "#444444",
                "button_fg": "#ffffff",
                "frame_bg": "#3c3c3c"
            }
        }
        self.current_theme = "day"

    def set_theme(self, theme):
        """Switch to the given theme."""
        if theme in self.themes:
            self.current_theme = theme
        else:
            raise ValueError(f"Theme '{theme}' not recognized.")

    def get_theme(self):
        """Get the current theme colors."""
        return self.themes[self.current_theme]


class App:
    def __init__(self, root):
        self.root = root
        self.theme_manager = ThemeManager()

        # Apply initial theme
        self.apply_theme()

        # Create UI components
        self.create_widgets()

    def apply_theme(self):
        """Apply the current theme to the entire application."""
        theme = self.theme_manager.get_theme()

        # Update root window background
        self.root.configure(bg=theme["bg"])

    def create_widgets(self):
        """Create UI components."""
        # Frame
        theme = self.theme_manager.get_theme()
        self.frame = tk.Frame(self.root, bg=theme["frame_bg"])
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Label
        self.label = tk.Label(
            self.frame,
            text="Select Theme:",
            bg=theme["frame_bg"],
            fg=theme["fg"],
            font=("Arial", 14)
        )
        self.label.pack(pady=10)

        # Buttons
        self.day_button = tk.Button(
            self.frame,
            text="Day Mode",
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            command=lambda: self.switch_theme("day")
        )
        self.day_button.pack(side="left", padx=5)

        self.night_button = tk.Button(
            self.frame,
            text="Night Mode",
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            command=lambda: self.switch_theme("night")
        )
        self.night_button.pack(side="left", padx=5)

    def switch_theme(self, theme):
        """Switch theme and reapply styles."""
        self.theme_manager.set_theme(theme)
        self.apply_theme()

        # Update widget styles to match new theme
        theme = self.theme_manager.get_theme()
        self.label.configure(bg=theme["frame_bg"], fg=theme["fg"])
        self.frame.configure(bg=theme["frame_bg"])
        self.day_button.configure(bg=theme["button_bg"], fg=theme["button_fg"])
        self.night_button.configure(bg=theme["button_bg"], fg=theme["button_fg"])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Themed Tkinter App")
    root.geometry("400x200")
    app = App(root)
    root.mainloop()
