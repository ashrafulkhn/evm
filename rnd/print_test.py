import tkinter as tk
from tkinter import Frame, LEFT, RIGHT, RAISED, BOTH, PhotoImage, Button, Label, Entry, Toplevel, END, Canvas, Scrollbar, TclError, Image
from ttkthemes import themed_tk as tk
from os import system
from tkinter import Canvas, simpledialog, messagebox
import os, time, random
# from print_actions import print_image
from escpos.printer import *
import barcode
from barcode.writer import ImageWriter
from PIL import Image,ImageDraw, ImageFont


# Printer setup using Linux device paths
# top_printer = 1
top_printer = File("/dev/usb/lp0")
top_printer.set(font='a', align="center", width=1, height=1)

# bottom_printer = 2
bottom_printer = File("/dev/usb/lp1")
bottom_printer.set(font='a', align="center", width=1, height=1)

# Global variable to store the selected printer
selected_printer = None

# Function to randomly select a printer
def select_printer():
    global selected_printer
    selected_printer = random.choice([top_printer, bottom_printer])
    print(f"Selected printer : {selected_printer}")

# Function to print the image on the selected printer
def print_image(image_path):
    try:
        if not selected_printer:
            raise ValueError("Printer not selected!")
        image = Image.open(image_path)
        selected_printer.image(image)
        selected_printer.cut()
    except Exception as e:
        print(f"Error printing image: {e}")

# Function to generate and print Barcode and "Correct" text
def print_correct(image_name):
    try:
        if not selected_printer:
            raise ValueError("Printer not selected!")
        barcode_text = generate_barcode_text(image_name, "Correct")
        if barcode_text:
            selected_printer.image(barcode_text)
            selected_printer.cut()
    except Exception as e:
        print(f"Error printing barcode and correct text: {e}")

# Function to print "Not Correct"
def print_not_correct():
    try:
        if not selected_printer:
            raise ValueError("Printer not selected!")
        selected_printer.text("Not Correct\n")
        selected_printer.cut()
    except Exception as e:
        print(f"Error printing 'Not Correct': {e}")

def generate_barcode_id():
    return random.randint(1000, 9999)  # Generates a 4-digit random number

# Function to generate barcode and text
def generate_barcode_text(image_name, text):
    try:
        # Generate a unique barcode ID if the image name doesn't include one
        barcode_id = generate_barcode_id()

        width, height = 200, 100  # Canvas size for barcode and text
        image = Image.new('1', (width, height), 255)  # Create a blank white image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 20)  # Load a font

        # Add text
        draw.text((10, 10), f"{text} {barcode_id}", font=font, fill=0)

        # Draw barcode (simple vertical lines for simulation)
        for x in range(50, 350, 10):
            draw.line([(x, 50), (x, 100)], fill=0, width=2)
        
        return image
    except Exception as e:
        print(f"Error generating barcode and text: {e}")
        return None


# Function to handle "Yes" button
def handle_yes(image_name):
    print_correct(image_name)
    confirmation_screen.destroy()

# Function to handle "No" button
def handle_no():
    print_not_correct()
    confirmation_screen.destroy()

# Main Application
def main():
    global confirmation_screen

    # Create main window
    root = tk.ThemedTk()
    root.title("Vote Printing Machine")
    root.geometry('480x800')
    root.configure(bg='white')
    root.get_themes()
    root.wm_attributes('-fullscreen', 'True')
    root.set_theme("clearlooks")

    # First screen
    def confirm_print_screen(img_path):
        global confirmation_screen

        # Select printer randomly
        select_printer()
        print(f"Selected Printer: {'Top Printer' if selected_printer == top_printer else 'Bottom Printer'}")
        # print(f"Selected Printer: {'Top Printer' if selected_printer == 1 else 'Bottom Printer'}")

        # Print the image
        print_image(img_path)

        # Open confirmation screen
        confirmation_screen = Toplevel(root)
        confirmation_screen.title("Confirm Print")

        Label(confirmation_screen, text="Is the printed image correct?").pack(pady=20)

        Button(confirmation_screen, text="Yes", command=lambda: handle_yes(img_path)).pack(side=LEFT, padx=10)
        Button(confirmation_screen, text="No", command=handle_no).pack(side=RIGHT, padx=10)

    img_path = PhotoImage("tiktok.png")
    # Button to print image
    Button(root, 
           text="Print Image",
           width=100,
           height=20,
           font=("Arial", 50, "bold"),
           command=lambda: confirm_print_screen(img_path)
        ).pack(pady=50)

    root.mainloop()

# Run the application
if __name__ == "__main__":
    main()

def print_image_old(img_path):        
    # message = confirm()
    message = confirm_print_screen(base_frame)
    # This is the confirmation of print. The return message should be "Voted" or "Cancelled" here.
    # message = "Voted"

    bottom_printer._raw(b'\n')
    ean = barcode.get('ean13', '123456789012', writer=ImageWriter())
    filename = ean.save('barcode')
    barcode_image = Image.open(filename)
    barcode_image = barcode_image.rotate(90, expand=True)  
    new_size = (100,200)
    barcode_image = barcode_image.resize(new_size, Image.Resampling.LANCZOS)
    
    barcode_image.save('resized_rotated_barcode.png')
    combined_width = barcode_image.width + 200  
    combined_height = max(barcode_image.height, 50)  
    combined_image = Image.new('RGB', (combined_width, combined_height), 'white')
    barcode_x_position = -30
    combined_image.paste(barcode_image, (barcode_x_position, 0))
    draw = ImageDraw.Draw(combined_image)
    font_size = 58
    font = ImageFont.truetype("usr/share/fonts/truetype/msttcorefonts/Arial.ttf", 24)  # Load a default font; adjust as necessary
    text_position = (barcode_image.width + 10, (combined_height - font_size) // 2)  # Adjust text position
    draw.text(text_position, message, fill='black', font=font)
    combined_image.save('../combined_image.png')
    bottom_printer.image('../combined_image.png')
    barcode_datåa = "12345678"
    bottom_printer._raw(b'\x1dV\x00')
    bottom_printer.cut()
    bottom_printer.flush()
    #time.sleep(0.1)
    bottom_motor()
    time.sleep(6)
    bottom_glass_off()
    GPIO.output(red_led_pin, GPIO.HIGH)
    GPIO.output(green_led_pin, GPIO.LOW)