import tkinter as tk
from tkinter import Frame, RAISED, BOTH, PhotoImage, Button, Label, Entry, Toplevel, END, Canvas, Scrollbar, TclError, Image
from ttkthemes import themed_tk as tk
from os import system
from tkinter import Canvas, simpledialog, messagebox
import os, time, random
# from print_actions import print_image
from escpos.printer import *
import barcode
from barcode.writer import ImageWriter
from PIL import Image,ImageDraw, ImageFont, ImageTk
from configparser import ConfigParser
import RPi.GPIO as GPIO

# ========DEFINE BASE DIRECTORY=====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Default path : {BASE_DIR}")

# ========CONFIGURATION PARSER======
config = ConfigParser()
config.read('config.ini')

# Get values from the config file
printing_width      = int(config['PRINTING']['width'])
printing_height     = int(config['PRINTING']['height'])
grid_image_width    = int(config['GRID_RESIZE']['width'])
grid_image_height   = int(config['GRID_RESIZE']['height'])
large_image_width   = int(config['LARGE_RESIZE']['width'])
large_image_height  = int(config['LARGE_RESIZE']['height'])
rotation_angle      = int(config['IMAGE']['rotation_angle'])
base_directory      = config['PATHS']['base_directory']

# Timer configuration
confim_selection_timer  = int(config['TIMERS']['confim_selection_timer'])
confirm_print_timer     = int(config['TIMERS']['confirm_print_timer'])
termination_timer       = int(config['TIMERS']['termination_timer'])
thanks_screen_timer     = int(config['TIMERS']['thanks_screen_timer'])
constituency_timer     = int(config['TIMERS']['constituency_timer'])

# ========EXTERNAL I/O DEVICE FUNCTIONS======
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set GPIO for different Purposes
top_motor_pin       = 12
bottom_motor_pin    = 13
top_glass_pin       = 27
bottom_glass_pin    = 17
green_led_pin       = 6
red_led_pin         = 5
reset_button_pin    = 16

# Set GPIO mode for respective GPIOs
GPIO.setup  (top_motor_pin,       GPIO.OUT)
GPIO.setup  (bottom_motor_pin,    GPIO.OUT)
GPIO.setup  (top_glass_pin,       GPIO.OUT)
GPIO.setup  (bottom_glass_pin,    GPIO.OUT)
GPIO.setup  (green_led_pin,       GPIO.OUT)
GPIO.setup  (red_led_pin,         GPIO.OUT)
GPIO.setup  (reset_button_pin,    GPIO.IN)

# Set Initial State for the Output GPIO.
GPIO.output(top_glass_pin, GPIO.HIGH)
GPIO.output(bottom_glass_pin, GPIO.HIGH)

GPIO.output(green_led_pin, GPIO.LOW)
GPIO.output(red_led_pin, GPIO.HIGH)

# ========Add-On Functions=======
file_path_top = os.path.join(BASE_DIR, 'time_delay_top.txt')
# Change this to your actual path
file_path_bottom = os.path.join(BASE_DIR, 'time_delay_bottom.txt')  # Change this to your actual path

print("Files completed.")

def read_value_from_file(file_path):
    """Reads the value from the file and returns it as a float."""
    try:
        with open(file_path, 'r') as file:
            value = file.read().strip()  # Read and strip any extra whitespace
            return float(value)  # Convert to float
    except FileNotFoundError:
        print("File not found. Returning default value 0.00.")
        return 0.00  # Default value if file doesn't exist
    except ValueError:
        print("The file does not contain a valid float value.")
        raise

def write_value_to_file(file_path, value):
    """Writes the value to the file, formatted to two decimal places."""
    with open(file_path, 'w') as file:
        file.write(f"{value:.2f}")  # Format the float to 2 decimal places and write

def decrement_value_in_file(file_path):
    """Reads the value from the file, decrements it by 0.03, and writes it back."""
    try:
        # Read the current value from the file
        current_value = read_value_from_file(file_path)

        # Print the current value
        print(f"Current value: {current_value:.2f}")

        # Decrement the value
        new_value = current_value - 0.03

        # Print the new decremented value
        print(f"New value: {new_value:.2f}")

        # Write the new value back to the file
        write_value_to_file(file_path, new_value)
        return current_value

    except Exception as e:
        print(f"An error occurred: {e}")

def resize_image(image_path, width, height):
    try:
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)  # Convert to PhotoImage
        return tk_image
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")
        return None

def resize_print_image(image_path, width, height):
    try:
        image = Image.open(image_path)
        # Rotate 90 degrees clockwise
        rotated_image = image.rotate(-90, expand=True)
        # Resize the rotated image
        resized_image = rotated_image.resize((width, height), Image.Resampling.LANCZOS)
        return resized_image  # Return the rotated and resized Pillow image
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")
        return None


# =====FUNCTIONS=======
def reset_pi():
    reset_val = GPIO.input(reset_button_pin)
    if reset_val == 1:
        system("sudo reboot")

def top_motor():
    pwm_top = GPIO.PWM(top_motor_pin, 50)
    pwm_top.start(6)
    time_delay_top = decrement_value_in_file(file_path_top)
    print(time_delay_top)
    time.sleep(time_delay_top)
    pwm_top.stop()

def top_motor_re():
    pwm_top = GPIO.PWM(top_motor_pin, 52)
    pwm_top.start(8)
    time_delay_top = decrement_value_in_file(file_path_top)
    print(time_delay_top)
    time.sleep(3)
    pwm_top.stop()

def bottom_motor():
    pwm_bottom = GPIO.PWM(bottom_motor_pin, 50)
    pwm_bottom.start(6)
    time_delay_bottom = decrement_value_in_file(file_path_bottom)
    print(time_delay_bottom)
    time.sleep(time_delay_bottom)
    pwm_bottom.stop()
    
def bottom_motor_re():
    pwm_bottom = GPIO.PWM(bottom_motor_pin, 52)
    pwm_bottom.start(8)
    time_delay_bottom = decrement_value_in_file(file_path_bottom)
    print(time_delay_bottom)
    time.sleep(3)
    pwm_bottom.stop()

def glass_action(glass_pin, state):
    if glass_pin in [top_glass_pin, bottom_glass_pin]:
        # Determine the GPIO output state based on "ON" or "OFF"
        output_state = GPIO.LOW if state == "ON" else GPIO.HIGH
        GPIO.output(glass_pin, output_state)
        print(f" INFO:: Glass {glass_pin} is {state}")
    else:
        print("Error:: Glass Not defined.")

def led_action(led_pin, state):
    if led_pin in [red_led_pin, green_led_pin]:
        # Determine the GPIO output state based on "ON" or "OFF"
        output_state = GPIO.LOW if state == "ON" else GPIO.HIGH
        GPIO.output(led_pin, output_state)
    else:
        print("Error:: LED Pin Not defined.")

# =========PRINTER===========================
# PRINTER SETUP
try:
    # Printer 1 Path in Linux
    # top_printer = 1
    print("Printer selection started.")
    top_printer = File("/dev/usb/lp0")
    top_printer.set(font='a',align="center",width=1,height=1)

    # Printer 2 Path in Linux
    # bottom_printer = 2
    bottom_printer = File("/dev/usb/lp1")
    bottom_printer.set(font='a',align="center",width=1,height=1)
except Exception as e:
    print(f"Error Occured during printer selection:: {e}")

# Global variable to store the selected printer
selected_printer = None

print("Printer Added.")

# Function to randomly select a printer
def select_printer():
    global selected_printer
    selected_printer = random.choice([top_printer, bottom_printer])
    # selected_printer = top_printer
    print(f"Selected printer : {selected_printer}")

def print_image(image_path):
    global selected_printer
    try:
        if not selected_printer:
            raise ValueError("Printer not selected.")
    except Exception as e:
        print(f"Error printing image: {e}")

    led_action(green_led_pin, "OFF")
    led_action(red_led_pin, "ON")
    selected_printer._raw(b'\x1b@')
    # selected_printer.set(align='center')
    selected_printer.set(font='a', align = "center", width=1, height=1)
    selected_printer._raw(b'\x1b\x21x')
    resized_image = resize_print_image(image_path, printing_height, printing_width)
    selected_printer.image(resized_image)
    # selected_printer.image(image_path)

    (bottom_motor if selected_printer == bottom_printer else top_motor)()  # Start the Approprite Motor 
    glass_pin = (bottom_glass_pin if selected_printer == bottom_printer else top_glass_pin)  # Start the Appropriate Glass
    glass_action(glass_pin, "ON")

    # except AttributeError as e:
    #     print(f"Error printing image: {e}")
    
    selected_printer.close()

def print_vote_status(image_name, vote_status):
    global selected_printer
    message = vote_status
    try:
        if not selected_printer:
            raise ValueError("Printer not selected!")

        # Comment these line if any problem arises.
        selected_printer._raw(b'\x1b@')
        # selected_printer.set(align='center')
        selected_printer.set(font='a', align = "center", width=1, height=1)
        # selected_printer._raw(b'\x1b\x21x')
        #  Comment upto here

        selected_printer._raw(b'\n')
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
        selected_printer.image('../combined_image.png')
        barcode_dataa = "12345678"
        selected_printer._raw(b'\x1dV\x00')
        selected_printer.cut()
        selected_printer.flush()
        #time.sleep(0.1)
        (bottom_motor if selected_printer == bottom_printer else top_motor)()  # Start the Approprite Motor

    except Exception as e:
        print(f"Error printing barcode and correct text: {e}")

# ============GUI Related Fuctions==========
# ========ROOT WINDOW CREATION==============
root = tk.ThemedTk()
root.title("Vote Printing Machine")
root.geometry('480x800')
root.configure(bg='white')
root.get_themes()
root.wm_attributes('-fullscreen', 'True')
root.set_theme("clearlooks")

# =======Add-On Functions==========
def clear_frame(frame):
    """
    Clears all the Widgets from the frame.
    :param frame: Frame e.g. base_frame
    """
    for widget in frame.winfo_children():
        widget.destroy()

def start_timer(frame, seconds, time_label, on_timeout):
    """
    A timer function that updates a label and executes a callback when time runs out.
    
    :param frame: The parent frame where the timer runs.
    :param seconds: Total seconds for the countdown.
    :param time_label: The label where the remaining time is displayed.
    :param on_timeout: The function to execute when the timer runs out.
    """
    global has_voted
    def countdown(time_left):
        if time_left > 0:
            time_label.config(text=f"Time Left to accept: {time_left} seconds", font=("Candara", 12))
            frame.after(1000, countdown, time_left - 1)
        # elif not has_voted:
        #     print("Elif")
        #     on_timeout()  # Execute the callback when timer runs out
        else:
            on_timeout()
    countdown(seconds)

class PasscodeDialog(simpledialog.Dialog):
    def body(self, master):
        self.passcode = ""
        self.label = Label(master, text="Enter Passcode")
        self.label.grid(row=0, column=0, columnspan=3)
        
        self.entry = Entry(master, show="*")
        self.entry.grid(row=1, column=0,columnspan=3)
        
        buttons = [
        ('1',2, 0), ('2', 2, 1), ('3', 2, 2),
        ('4',3, 0), ('5', 3, 1), ('6', 3, 2),
        ('7',4, 0), ('8', 4, 1), ('9', 4, 2),
        ('0', 5, 1)]
        
        for (text, row, column)in buttons:
            button = Button(master, text=text, command=lambda t=text: self.on_button(t))
            button.grid(row=row, column=column, sticky="nsew")
        return self.entry
        
    def on_button(self, text):
        self.passcode += text
        self.entry.insert(END, text)
        
    def apply(self):
        self.result = self.passcode

def on_power_button(action):
    pass_status = confirm_password()
    if pass_status == 1:
        if action == "close_app":
            # Close app routine
            os.system("pkill -f main_2412.py") 
            # pass 
        elif action == "shutdown":
            # Shutdown routine
            os.system("sudo shutdown -h now")
        else:
            print("Unexpected Error.")
    else:
        messagebox.showerror(title =None, message = "Access Denied, Incorrect Passcode")

def confirm_password():
    dialog_entry = PasscodeDialog(root)
    if dialog_entry.result == "1234":
        print("Password is correct.")
        return 1
    else:
        print("Password is incorrect.")
        return 0

# =======Applications Screens==========

# Screen :: Home screen of the Application
def open_vote_window1(base_frame):
    """
    Displays a fullscreen window to ask user to vote. Only one Button on this page.

    :param image_path: Frame e.g. base_frame
    """
    clear_frame(base_frame)
    vote_frame = Frame(base_frame,
                       height=800,
                       width=480,
                       bg='white'
                       )
    vote_frame.pack_propagate(False)
    vote_frame.pack(fill='both', expand=True)
    
    btn_vote = Button(vote_frame,
                        text="   Press to Vote   ", 
                        width=12,
                        height=2,
                        bg="#4CAF50",
                        fg="white",
                        font=("Candara", 25, 'bold'),
                        command=lambda: show_constituency_screen(base_frame)
                        )
    btn_vote.pack(expand=True)

def open_vote_window(base_frame):
    """
    Displays a fullscreen window to ask user to vote. Only one Button on this page.

    :param image_path: Frame e.g. base_frame
    """
    global selectd_printer

    clear_frame(base_frame)
    vote_frame = Frame(base_frame,
                       height=800,
                       width=480,
                       bg='white'
                       )
    vote_frame.pack_propagate(False)
    vote_frame.pack(fill='both', expand=True)
    
    vote_frame.background_image = PhotoImage(file=os.path.join(BASE_DIR, "assets", "open_vote_window", "background.png"))
    vote_frame.vote_button_image = PhotoImage(file=os.path.join(BASE_DIR, "assets", "open_vote_window", "Button.png"))
    vote_frame.power_button_image = PhotoImage(file=os.path.join(BASE_DIR, "assets", "open_vote_window", "Power.png"))
    vote_frame.close_button_image = PhotoImage(file=os.path.join(BASE_DIR, "assets", "open_vote_window", "Close.png"))

    backgound_image_label = Label(vote_frame, image=vote_frame.background_image)
    vote_button = Button(vote_frame,
                        image=vote_frame.vote_button_image,
                        highlightthickness=0, 
                        highlightbackground="white", 
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="raised",
                        borderwidth=1,
                        activebackground="white",
                        activeforeground="white", 
                        command=lambda: show_constituency_screen(base_frame)
                         )
    power_button = Button(vote_frame,
                        image=vote_frame.power_button_image,
                        highlightthickness=0, 
                        highlightbackground="white", 
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="raised",
                        borderwidth=1,
                        activebackground="white",
                        activeforeground="white",
                        command=lambda: on_power_button("close_app")
                        )
    close_button = Button(vote_frame,
                        image=vote_frame.close_button_image,
                        highlightthickness=0, 
                        highlightbackground="white", 
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="raised",
                        borderwidth=1,
                        activebackground="white",
                        activeforeground="white",
                        command=lambda: on_power_button("close_app")
                        )

    backgound_image_label.place(
        x=0,
        y=0,
        width=480,
        height=800
        )
    vote_button.place(
        x=41,
        y=595,
        width=413,
        height=146
        )
    power_button.place(
        x=15,
        y=13,
        width=70,
        height=70
        )
    # close_button.place(
    #     x=384,
    #     y=13,
    #     width=100,
    #     height=70
    #     )

    glass_pin = (bottom_glass_pin if selected_printer == bottom_printer else top_glass_pin)
    glass_action(glass_pin, "OFF")

    led_action(red_led_pin, "OFF")
    led_action(green_led_pin, "ON")

# Screen :: Constituency Screen
def show_constituency_screen(base_frame):
    """
    Frame consituency_window details are mentioned here
    """ 
    clear_frame(base_frame)

    # Frame to control the label
    frame1 = Frame(base_frame,
                    height=800,
                    width=480,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    label = Label(frame1,
                  text="Is your constituency \n \"XYZ\" ?",
                  font=("Candara", 20, 'bold'),
                  bg='white',
                  fg='black',
                  justify='center'
                  )
    label.pack(pady=200)

    # Frame for Buttons
    button_frame = Frame(frame1, bg='white')
    button_frame.pack(expand=True)

    # Styled Yes Button
    yes_button = Button(button_frame, 
                        text="Yes", 
                        width=10,
                        height=2,
                        bg= "#4CAF50",
                        fg= 'white',
                        font=("Candara",15, "bold"),
                        command=lambda: on_yes_clicked(base_frame))
    yes_button.pack(side="left", padx=20)

    no_button = Button(button_frame,
                       text="No",
                       width=10,
                       height=2,
                       bg="#F44336",
                       fg="white",
                       font=("Candara", 15, "bold"),
                       command=lambda: on_no_clicked(base_frame))
    no_button.pack(side="right", padx=20)

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Candara", 9))
    time_label.place(relx=0.5, rely=0.95, anchor="center")

    # Start Timer
    start_timer(frame1, constituency_timer, time_label, lambda: open_vote_window(base_frame))

def on_yes_clicked(base_frame):
    grid_screen(base_frame, image_directory_path=os.path.join(BASE_DIR, "print"))

def on_no_clicked(base_frame):
    voting_terminated_screen(base_frame)

# Screen :: Grid Screen
def grid_screen(base_frame, image_directory_path):
    """
    Screen :: Displays a scrollable grid of image buttons. Clicking an image button opens `open_image_screen`.

    :param base_frame: Root Tkinter window or any frame.
    :param image_directory_path: Path to the directory containing images.
    """
    clear_frame(base_frame)

    # Frame to control the label
    frame1 = Frame(base_frame,
                    height=800,
                    width=480,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Scrollable Canvas
    canvas = Canvas(frame1, bg='white')
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(frame1, 
                        orient="vertical", 
                        command=canvas.yview, 
                        width=30,
                        relief="flat",
                        takefocus=1,
                        troughcolor="black"
                        )
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollable Frame
    scrollable_frame = Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    col_image=1 # start from column 1
    row_image=3 # start from row 3 
    col_label=1 # start from column 1
    row_label=4 # start from row 3 

    # Load images from directory and create buttons
    image_files = [os.path.join(image_directory_path, f) for f in os.listdir(image_directory_path) if f.endswith((".png", ".jpg", ".jpeg"))]
    for idx, img_path in enumerate(image_files):
        resized_photo = resize_image(img_path, grid_image_width, grid_image_height)
        if resized_photo is None:
            continue  # Skip the image if resizing failed
        button = Button(
            scrollable_frame,
            image=resized_photo,
            bd=0,
            border=4,
            highlightbackground="white",
            highlightcolor="white",
            fg="white",
            bg="white",
            relief="flat",
            height=150,
            width=150,
            borderwidth=4,
            activebackground="white",
            activeforeground="white",
            command=lambda p=img_path: open_image_screen(base_frame, p)
        )
        button.image = resized_photo  # Keep a reference to avoid garbage collection
        # button.grid(row=row_image, column=col_image, padx=30, pady=30, sticky="news")

        # Add a label below the image for the file name (without extension)
        file_name = os.path.basename(img_path).split('.')[0]  # Remove the extension
        label = Label(scrollable_frame, text=file_name, bg="#000000", border=4,fg="white", font=("Candara", 15, "bold"), borderwidth=1, relief="solid", padx=5, pady=5)

        button.grid(row=row_image, column=col_image, padx=30, pady=30, sticky="news")      # Buttons in two columns
        label.grid(row=row_label, column=col_label, padx=10, pady=2, sticky="news")     # Labels below the button
        
        if(col_label==2):                   # start new line after third column
            row_label=row_label+2           # start wtih next row
            col_label=1                     # start with first column
        else:                               # within the same row
            col_label=col_label+1           # increase to next column

        if(col_image==2):                   # start new line after third column
            row_image=row_image+2           # start wtih next row
            col_image=1                     # start with first column
        else:                               # within the same row
            col_image=col_image+1           # increase to next column 

    # # Enable Mouse and Touch Scrolling
    # def on_touch_scroll(event):
    #     canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    # def on_mouse_wheel(event):
    #     canvas.yview_scroll(int(-1 * event.delta / 120), "units")
    # def on_press(evt):
    #     canvas.offset_y = evt.y_root  # Record the y position when the finger touches

    # def on_touch_scroll(evt):
    #     delta = evt.y_root - canvas.offset_y  # Calculate the distance moved
    #     canvas.offset_y = evt.y_root  # Update the offset
    #     if delta < 0:
    #         canvas.yview_scroll(-1, "units")  # Scroll up if moved up
    #     else:
    #         canvas.yview_scroll(1, "units")  # Scroll down if moved down

    # def on_mouse_wheel(event):
    #     canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  # For mouse scrolling

    # canvas.bind("<Button-1>", on_press)  # Bind to detect when the user touches
    # canvas.bind("<B1-Motion>", on_touch_scroll)
    # canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    # ================================================
    # Enable Mouse, Touch, and Keyboard Scrolling

    def on_press(evt):
        canvas.offset_y = evt.y_root  # Record the y position when the touch starts

    def on_touch_scroll(evt):
        delta = evt.y_root - canvas.offset_y  # Calculate the distance moved
        canvas.offset_y = evt.y_root  # Update the offset
        if delta < 0:
            canvas.yview_scroll(-1, "units")  # Scroll up if moved up
        else:
            canvas.yview_scroll(1, "units")  # Scroll down if moved down

    def on_mouse_wheel(event):
        if event.num == 5 or event.delta < 0:  # Scroll down
            canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta > 0:  # Scroll up
            canvas.yview_scroll(-1, "units")

    def on_key_press(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")  # Scroll up
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")  # Scroll down

    # Bind events
    canvas.bind("<Button-1>", on_press)  # Detect touch start
    canvas.bind("<B1-Motion>", on_touch_scroll)  # Detect touch movement
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Detect mouse scroll
    canvas.bind_all("<KeyPress-Up>", on_key_press)  # Up arrow key
    canvas.bind_all("<KeyPress-Down>", on_key_press)  # Down arrow key

    # For Linux systems, bind <Button-4> and <Button-5> for mouse scroll
    canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

# Screen :: Enlarged Image Screen
def open_image_screen(base_frame, image_path):
    """
    Displays a fullscreen window for the selected image with a timer, accept, and cancel buttons.

    :param image_path: Path to the selected image.
    """
    global has_voted
    has_voted = False
    clear_frame(base_frame)

    # Frame to control the Widgets
    frame1 = Frame(base_frame,
                    height=800,
                    width=480,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Display Image
    resized_image = resize_image(image_path, large_image_height, large_image_width)
    # photo = PhotoImage(file=image_path)
    lbl = Label(frame1, 
                image=resized_image,
                bd=0,
                border=4,
                highlightbackground="white",
                highlightcolor="white",
                fg="white",
                bg="white", 
                relief="flat",
                height=400,
                width=400,
                borderwidth=4,
                activebackground="white",
                activeforeground="white"
                )
    lbl.image = resized_image
    lbl.pack(pady=(50, 10))

    # Accept and Cancel Buttons
    accept_img = PhotoImage(file=os.path.join(BASE_DIR, "buttons", "accept_test.png"))

    btn_accept = Button(frame1,
                        highlightthickness=0, 
                        highlightbackground="white", 
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="flat",
                        borderwidth=0,
                        activebackground="white",
                        activeforeground="white", 
                        image=accept_img, 
                        command=lambda: accept_image(image_path, base_frame))
    btn_accept.image = accept_img
    btn_accept.pack(side="left", padx=50, pady=10)

    cancel_img = PhotoImage(file=os.path.join(BASE_DIR, "buttons", "cancel_test.png"))
    btn_cancel = Button(frame1,
                        highlightthickness=0, 
                        highlightbackground="white", 
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="flat",
                        borderwidth=0,
                        activebackground="white",
                        activeforeground="white", 
                        image=cancel_img, 
                        command=lambda: cancel_image(image_path, base_frame))
    btn_cancel.image = cancel_img
    btn_cancel.pack(side="right", padx=10, pady=10)

    # # Timer Label
    # time_label = Label(frame1, text="Time Left: 5 seconds", bg='white', font=("Candara", 9))
    # # time_label.pack(pady=(20, 10))
    # time_label.pack()

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Candara", 9))
    time_label.place(relx=0.5, rely=0.95, anchor="center")

    # Start Timer
    start_timer(frame1, confim_selection_timer, time_label, lambda: accept_image(image_path, base_frame))

def accept_image(image_path, base_frame):
    global selected_printer
    select_printer()
    print(f"INFO:: Selected Printer: {'Top Printer' if selected_printer == top_printer else 'Bottom Printer'}")
    print_image(image_path)
    confirm_print_screen(base_frame, image_path)

def cancel_image(image_path,base_frame):
    clear_frame(base_frame)
    grid_screen(base_frame, image_directory_path=os.path.join(BASE_DIR, "print"))

# Screen :: Ask to confirm if the print was as selected image
def confirm_print_screen(base_frame, image_path):
    """
      Screen :: Ask to confirm if the print was as selected image

      :param base_frame : Root Tkinter window or any frame.
      :param image_directory_path: Path to the directory containing images.
    """
    
    clear_frame(base_frame)

    # Frame to control the label
    frame1 = Frame(base_frame,
                    height=800,
                    width=480,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Display Image
    resized_image = resize_image(image_path, large_image_height, large_image_width)
    lbl = Label(frame1, 
                image=resized_image,
                bd=0,
                border=4,
                highlightbackground="white",
                highlightcolor="white",
                fg="white",
                bg="white", 
                relief="flat",
                borderwidth=4,
                activebackground="white",
                activeforeground="white"
                )
    lbl.image = resized_image
    lbl.pack(pady=(50, 10))

    label = Label(frame1,
                  text="Confirm if the print \n match your vote?",
                  font=("Candara", 20, 'bold'),
                  bg='white',
                  fg='black',
                  justify='center'
                  )
    label.pack(pady=50)

    # Frame for Buttons
    button_frame = Frame(frame1, bg='white')
    button_frame.pack(expand=True)

    # Styled Yes Button
    yes_button = Button(button_frame, 
                        text="Yes", 
                        width=10,
                        height=2,
                        bg= "#4CAF50",
                        fg= 'white',
                        font=("Candara",15, "bold"),
                        command=lambda: on_print_accepted(base_frame, image_path))
    yes_button.pack(side="left", padx=20)

    no_button = Button(button_frame,
                       text="No",
                       width=10,
                       height=2,
                       bg="#F44336",
                       fg="white",
                       font=("Candara", 15, "bold"),
                       command=lambda: on_print_rejected(base_frame, image_path))
    no_button.pack(side="right", padx=20)

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Candara", 9))
    time_label.place(relx=0.5, rely=0.95, anchor="center")

    # Start Timer
    start_timer(frame1, confim_selection_timer, time_label, lambda: on_print_accepted(base_frame, image_path))

def on_print_accepted(base_frame, image_path):
    global vote_status 
    vote_status = "Voted Success"
    print_vote_status(image_path, vote_status)
    voting_thanks_screen(base_frame)

def on_print_rejected(base_frame, image_path):
    global vote_status
    vote_status = "Cancelled"
    print_vote_status(image_path, vote_status)
    voting_terminated_screen(base_frame)

# Screen :: Thank you for Voting Screen
def voting_thanks_screen(base_frame):
    global selected_printer
    clear_frame(base_frame)  # Clear all previous widgets available on the Frame of this page.
    frame1 = Frame(base_frame,
                   bg="white",
                   width=480,
                   height=800
                   )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Centering the heading label
    head_label = Label(frame1,
                       bg="white",
                       fg="black",
                       font=("Candara", 20, "bold"),
                       text="Thank you for Voting."
                       )

    head_label.place(relx=0.5, rely=0.4, anchor="center")

    # Centering the message label
    message_label = Label(frame1,
                          bg="white",
                          fg="black",
                          font=("Candara", 15, "bold"),
                          text="All the best :)"
                          )
    # message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Candara", 9))
    time_label.place(relx=0.5, rely=0.95, anchor="center")
    time_label.place(anchor="center")

    # Start Timer
    start_timer(frame1, thanks_screen_timer, time_label, lambda: open_vote_window(base_frame))
    # print("Thank you for Voting.")

# Screen :: Vote Terminated Screen
def voting_terminated_screen(base_frame):
    global selected_printer
    clear_frame(base_frame)  # Clear all previous widgets available on the Frame of this page.
    frame1 = Frame(base_frame,
                   bg="white",
                   width=480,
                   height=800
                   )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Centering the heading label
    head_label = Label(frame1,
                       bg="white",
                       fg="black",
                       font=("Candara", 20, "bold"),
                       text="Your Voting is terminated."
                       )
    head_label.place(relx=0.5, rely=0.4, anchor="center")

    # Centering the message label
    message_label = Label(frame1,
                          bg="white",
                          fg="black",
                          font=("Candara", 20),
                          text="Go Back \n to the Polling Booth Officer"
                          )
    message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Candara", 9))
    time_label.place(relx=0.5, rely=0.95, anchor="center")

    # Start Timer
    start_timer(frame1, termination_timer, time_label, lambda: open_vote_window(base_frame))
    # print("The voting has been terminated.")

print("Starting Application.")

def main():
    print("Starting Application main.")
    base_frame = Frame(root, bg="purple")
    base_frame.pack(fill='both', expand=True)

    open_vote_window(base_frame)
    # home(root, "small")
    root.mainloop()

if __name__ == "__main__":
    main()
