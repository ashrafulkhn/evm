import tkinter as tk
from tkinter import Frame, RAISED, BOTH, PhotoImage, Button, Label, Entry, Toplevel, END, Canvas, Scrollbar, TclError
from ttkthemes import themed_tk as tk
from time import sleep
from os import system
from tkinter import simpledialog, messagebox, Canvas
from PIL import Image
import os
import time
from print_actions import print_image
from escpos.printer import *
import barcode
from barcode.writer import ImageWriter
from PIL import Image,ImageDraw, ImageFont

import time
import RPi.GPIO as GPIO

root = tk.ThemedTk()
root.title("Home Page")
root.geometry('600x1024')
root.configure(bg='white')
root.get_themes()
root.wm_attributes('-fullscreen', 'True')
root.set_theme("clearlooks")

file_path_top = 'time_delay_top.txt'  # Change this to your actual path
file_path_bottom = 'time_delay_bottom.txt'  # Change this to your actual path

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set GPIO for different Purposes
# TBD
Tm = 12
Bm = 13
glass_T = 27
glass_B = 17
led_g = 6
led_r = 5
reset = 16

# Set GPIO mode for respective GPIOs
# Purposes to be discussed
# TBD
GPIO.setup(Tm, GPIO.OUT)
GPIO.setup(Bm, GPIO.OUT)
GPIO.setup(glass_T, GPIO.OUT)
GPIO.setup(glass_B, GPIO.OUT)
GPIO.setup(led_g,GPIO.OUT)
GPIO.setup(led_r,GPIO.OUT)
GPIO.setup(reset,GPIO.IN)

# Set Initial State for the Output GPIO.
# Purposes to be discussed
# TBD
GPIO.output(glass_T, GPIO.HIGH)
GPIO.output(glass_B, GPIO.HIGH)
GPIO.output(led_g, GPIO.LOW)
GPIO.output(led_r, GPIO.HIGH)

pwm_top = GPIO.PWM(Tm, 50)
pwm_bottom = GPIO.PWM(Bm, 50)

reset_val = 0

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

def reset_pi():
    reset_val = GPIO.input(reset)
    if reset_val == 1:
        system("sudo reboot")

def top_motor():
    pwm_top = GPIO.PWM(Tm, 50)
    pwm_top.start(6)
    time_delay_top = decrement_value_in_file(file_path_top)
    print(time_delay_top)
    time.sleep(time_delay_top)
    pwm_top.stop()

def top_motor_re():
    pwm_top = GPIO.PWM(Tm, 52)
    pwm_top.start(6)
    time_delay_top = decrement_value_in_file(file_path_top)
    print(time_delay_top)
    time.sleep(3)
    pwm_top.stop()

def bottom_motor():
    pwm_bottom = GPIO.PWM(Bm, 50)
    pwm_bottom.start(8)
    time_delay_bottom = decrement_value_in_file(file_path_bottom)
    print(time_delay_bottom)
    time.sleep(time_delay_bottom)
    pwm_bottom.stop()

def bottom_motor_re():
    pwm_bottom = GPIO.PWM(Bm, 52)
    pwm_bottom.start(8)
    time_delay_bottom = decrement_value_in_file(file_path_bottom)
    print(time_delay_bottom)
    time.sleep(3)
    pwm_bottom.stop()

def top_glass_on():
    GPIO.output(glass_T, GPIO.LOW)
   # time.sleep(6)
   # GPIO.output(glass_T, GPIO.HIGH)

def top_glass_off():
    GPIO.output(glass_T, GPIO.HIGH)

def bottom_glass_on():
    GPIO.output(glass_B, GPIO.LOW)
   # time.sleep(6)
    #GPIO.output(glass_B, GPIO.HIGH)

def bottom_glass_off():
    GPIO.output(glass_B, GPIO.HIGH)

def select_message():
    messagebox.showinfo(title =None, message = "Please Select a Symbol")

# Printer 1 Path in Linux
# p1 = File("/dev/usb/lp0")
# p1.set(font='a',align="center",width=1,height=1)

# Printer 2 Path in Linux
# p2 = File("/dev/usb/lp1")
# p2.set(font='a',align="center",width=1,height=1)

# def load_images(folder_path):
# 	images = []
# 	for filename in os.listdir(folder_path):
# 		if filename.endswith(('.png', '.jpg', '.jpeg')):
# 			images.append(os.path.join(folder_path, filename))
# 	return images

def clear_frame(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

def convert_image_to_png(image_path):
	img = Image.open(image_path)
	img.thumbnail((600, 1024))
	new_path = image_path.rsplit('.', 1)[0] + '.png'
	img.save(new_path, 'PNG')
	return new_path

# small_images = load_images("small")
# small_images = [convert_image_to_png(img) for img in small_images]

# print_images = load_images("print")
# print_images = [convert_image_to_png(img) for img in print_images]

# Frame consituency_window details are mentioned here
def show_constituency_screen(base_frame):
    # constituency_window = Toplevel(root)
    # constituency_window.attributes('-fullscreen', "True")
    # constituency_window.geometry('600x1024')
    # constituency_window.configure(bg='white')
    clear_frame(base_frame)

    # Frame to control the label
    frame1 = Frame(base_frame,
                    height=1024,
                    width=600,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    label = Label(frame1,
                  text="Your constituency name is \n \"MOMBASA\"",
                  font=("Arial", 30, 'bold'),
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
                        font=("Arial",15, "bold"),
                        command=lambda: on_yes_clicked(base_frame))
    yes_button.pack(side="left", padx=50)

    no_button = Button(button_frame,
                       text="No",
                       width=10,
                       height=2,
                       bg="#F44336",
                       fg="white",
                       font=("Arial", 15, "bold"),
                       command=lambda: on_no_clicked(base_frame))
    no_button.pack(side="right", padx=50)

def on_yes_clicked(base_frame):
    clear_frame(base_frame)
    grid_screen(base_frame, "small")

def on_no_clicked(base_frame):
    # messagebox.showinfo("Contact Polling Officer", "Please Contact your polling officer.")
    clear_frame(base_frame)
    voting_terminated_screen(base_frame)

def start_timer(frame, seconds, time_label, on_timeout):
    """
    A timer function that updates a label and executes a callback when time runs out.
    
    :param frame: The parent frame where the timer runs.
    :param seconds: Total seconds for the countdown.
    :param time_label: The label where the remaining time is displayed.
    :param on_timeout: The function to execute when the timer runs out.
    """
    def countdown(time_left):
        if time_left > 0:
            time_label.config(text=f"Time Left to accept: {time_left} seconds")
            frame.after(1000, countdown, time_left - 1)
            print("If")
        elif not has_voted:
            print("Elif")
            on_timeout()  # Execute the callback when timer runs out
        else:
            print("Else")
            on_timeout()

    countdown(seconds)

# def open_image_screen(image_path):
#     global has_voted
#     has_voted = False
#     image_window = Toplevel(root)
#     image_window.attributes('-fullscreen', True)
#     image_window.configure(bg='white')

#     # Display Image
#     photo = PhotoImage(file=image_path)
#     lbl = Label(image_window, image=photo)
#     lbl.image = photo
#     lbl.pack(pady=(50, 10))

#     # Timer Label
#     time_label = Label(image_window, text="Time Left: 5 seconds", bg='white', font=("Arial", 24))
#     time_label.pack(pady=(20, 10))

#     # Accept and Cancel Buttons
#     accept_img = PhotoImage(file="buttons/accept_test.png")
#     btn_accept = Button(image_window, image=accept_img, command=lambda: accept_image(image_path, image_window))
#     btn_accept.image = accept_img
#     btn_accept.pack(side="left", padx=10, pady=10)

#     cancel_img = PhotoImage(file="buttons/cancel_test.png")
#     btn_cancel = Button(image_window, image=cancel_img, command=lambda: cancel_image(image_path, image_window))
#     btn_cancel.image = cancel_img
#     btn_cancel.pack(side="right", padx=10, pady=10)

#     # Start Timer
#     start_timer(image_window, 5, time_label, lambda: accept_image(image_path, image_window))

def accept_image(image_path, base_frame):
    global has_voted
    if not has_voted:
        has_voted = True
       # encoding = "shift-jis"
       # message = "Voted"
       # encoded_text = message.encode(encoding)
        # print_image(image_path)
        # image_window.destroy()

        # clear_frame(image_window)
        # frame = Frame(image_window,
        #               bg="green")
        # frame.pack()

        # success_ok_btn =  Button(frame, text="Close",
        #                          fg='white',
        #                          bg='green',
        #                          command= lambda: on_success_ok_btn(image_window=image_window))
        # success_ok_btn.pack(fill=BOTH)
        clear_frame(base_frame)
        messagebox.showinfo(title =None, message = "Vote Successful")
        open_vote_window(base_frame)

def cancel_image(image_path,base_frame):
#    encoding = "shift-jis"
#    message = "Cancelled"
#    encoded_text = message.encode(encoding)
#    print_image(image_path, encoded_text)
    clear_frame(base_frame)
    messagebox.showwarning(title =None, message = "Vote Cancelled")
    open_vote_window(base_frame)

def on_success_ok_btn(image_window):
    # Timer Label
    time_label = Label(image_window, text="Time Left: 5 seconds", bg='white', font=("Arial", 24))
    time_label.pack(pady=(20, 10))
    # Start Timer
    start_timer(image_window, 5, time_label, lambda: destroy_window(image_window))
    show_constituency_screen(image_window)

def destroy_window(window):
    window.destroy()
	
def voting_terminated_screen(base_frame):
    clear_frame(base_frame)  # Clear all previous widgets available on the Frame of the this page.
    frame1 = Frame(base_frame,
                    bg= "white",
                    width=600,
                    height=1024
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    head_label = Label(frame1,
                        bg="white",\
                        fg="black",
                        font=("Arial", 45),
                        text="Your Voting is terminated."
                        )
    head_label.pack()
    message_label = Label(frame1,
                        bg="white",\
                        fg="black",
                        font=("Arial", 40),
                        text="Go Back to the Polling Booth Officer"
                        )
    message_label.pack()

    # Timer Label
    time_label = Label(frame1, text="Time Left: 5 seconds", bg='white', font=("Arial", 24))
    # time_label.pack(pady=(800, 10))
    time_label.pack()

    # Start Timer
    start_timer(frame1, 5, time_label, lambda: open_vote_window(base_frame))
    print("The voting has been terminated.")

def open_vote_window(base_frame):
    """
    Displays a fullscreen window to ask user to vote. Only one Button on this page.

    :param image_path: Frame e.g. base_frame
    """
    vote_frame = Frame(base_frame,
                       height=1024,
                       width=600,
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
                        font=("Arial", 25, 'bold'),
                        command=lambda: close_vote_window(base_frame)
                        )
    btn_vote.pack(expand=True)
	
def close_vote_window(base_frame):
    clear_frame(base_frame)
    show_constituency_screen(base_frame=base_frame)
    # home(base_frame, "small")

def confirm():
    global confirmation_response
    confirmation_response = None

    def auto_confirm_yes():
        global confirmation_response
        confirmation_response = "yes"
        confirm_window.destroy()
        # image_window.destroy()

    def countdown(time_left):
        global has_voted
       # if not has_voted:
        try:
            if timer_label.winfo_exists():  # Check if the label exists before updating
                timer_label.config(text=f"Auto-confirming in {str(time_left).zfill(2)} seconds...")
            else:
                print("Label no longer exists.")
            if time_left > 0:
                timer_label.config(text=f"Auto-confirming in {str(time_left).zfill(2)} seconds...")
                root.after(1000, countdown, time_left - 1)
            else:
                auto_confirm_yes()
                confirm_window.destroy()
        except TclError as e:
            print(f"Error during countdown: {e}")        
    def on_response(response):
        global confirmation_response
        confirmation_response = response
        confirm_window.destroy()

    # Create a new top-level window for the confirmation dialog
    confirm_window = Toplevel(root)
    confirm_window.title("Confirmation")
    confirm_window.attributes('-topmost', True)
    confirm_window.geometry('600x1024')
    
    message_label = Label(confirm_window, text="Do you wish to confirm your vote?")
    message_label.pack(pady=20)
    
    timer_label = Label(confirm_window, text="Auto-confirming in 15 seconds...", font=("Helvetica", 12))
    timer_label.pack(pady=20)
    
    yes_button = Button(confirm_window, text="Yes",height=3, width=10,command = lambda: on_response("yes"))
    yes_button.pack(side="left", padx=20, pady=10)
    
    no_button = Button(confirm_window, text="No", height=3, width =10,command = lambda: on_response("no"))
    no_button.pack(side="right", padx=20, pady=10)
    # Start the countdown
    countdown(15)

    # Wait for user response or auto-confirm
    root.wait_window(confirm_window)
    
    if confirmation_response == "yes":
        message = "Voted"
     #   encoding = "shift-jis"
      #  message = text.encode(encoding)
    elif confirmation_response == "no":
        message = "Cancelled"
       # encoding = "shift-jis"
       # message = text.encode(encoding)
    else:
        # Default if no response was set (which should not happen)
        message = b"Cancelled"

    return message

# Print Image functions was here. Ashraful has moved it to print action file

        
    
# def select(n):
# 	open_image_screen(print_images[n])

# frame = Frame(root, bg='white')
# frame.pack(fill=BOTH, expand=True)

# canvas = Frame(frame)
# #canvas.grid(row=0, column=0, sticky="nsew")

# #button_frame = Frame(frame, height=120, bg='white')
# #button_frame.grid(row=1, column=0, sticky="ew")

# canvas = Canvas(frame,bg = 'white')
# canvas.pack(side="left", fill=BOTH, expand = True)
# scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview, width=30)
# scrollbar.pack(side="right", fill="y")
# scrollable_frame = Frame(canvas, bg = 'white')

# scrollable_frame.bind(
# "<Configure>",
# lambda e: canvas.configure(
# scrollregion=canvas.bbox("all")
# ) 
# )

# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# canvas.configure(yscrollcommand=scrollbar.set)


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

# # Bind touch and mouse scroll events
# canvas.bind("<Button-1>", on_press)  # Bind to detect when the user touches
# canvas.bind("<B1-Motion>", on_touch_scroll)  # Bind to detect when the user moves the finger
# root.bind_all("<MouseWheel>", on_mouse_wheel)

# #canvas_height = root.winfo_screenheight() - 1200 
# #canvas.configure(height= canvas_height)

# for idx, img_path in enumerate(small_images):
#     photo = PhotoImage(file=img_path)
#     img_name = os.path.basename(img_path).rsplit('.', 1)[0]
#     btn = Button(scrollable_frame, image=photo, command=lambda p=img_path, i=idx: select(i), highlightthickness=0, bd=0)
#     btn.image = photo
#     btn.grid(row=int(idx // 2 * 2), column=int(idx % 2), padx=5, pady=5)
#     label = Label(scrollable_frame, text=img_name, bg='white')
#     label.grid(row=int(idx // 2 * 2 + 1), column=int(idx % 2), padx=80, pady=50, sticky="w")

# bottom_frame = Frame(root,height=100,bg='grey')
# bottom_frame.pack(fill='x', side='bottom')

# For password controls
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
        
        
def verify_home():
    dialog = PasscodeDialog(root)
    if dialog.result == "1234":
        messagebox.showinfo(title =None, message = "Access Granted")
        desktop()
    else: 
        messagebox.showerror(title =None, message = "Access Denied, Incorrect Passcode")

        
def verify_shutdown():
    dialog = PasscodeDialog(root)
    if dialog.result == "1234":
        messagebox.showinfo(title =None, message = "Access Granted")
        shutdown()
    else: 
        messagebox.showerror(title =None, message = "Access Denied, Incorrect Passcode")
    
        
def shutdown():
    # os.system("sudo shutdown -h now")
    os.system("pkill -f main_ashraf_2911.py")


def desktop():
    os.system("pkill -f main_ashraf_2911.py")
    
def select(n):
	open_image_screen(print_images[n])

# import os
# from tkinter import *

def grid_screen(base_frame, image_directory_path):
    """
    Displays a scrollable grid of image buttons. Clicking an image button opens `open_image_screen`.

    :param base_frame: Root Tkinter window or any frame.
    :param image_directory_path: Path to the directory containing images.
    """

    clear_frame(base_frame)

    # Frame to control the label
    frame1 = Frame(base_frame,
                    height=1024,
                    width=600,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Scrollable Canvas
    canvas = Canvas(frame1, bg='white')
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(frame1, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollable Frame
    scrollable_frame = Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    # Load images from directory and create buttons
    image_files = [os.path.join(image_directory_path, f) for f in os.listdir(image_directory_path) if f.endswith((".png", ".jpg", ".jpeg"))]
    for idx, img_path in enumerate(image_files):
        photo = PhotoImage(file=img_path)
        button = Button(scrollable_frame,
                        image=photo,
                        bg="white",
                        highlightthickness=0,
                        bd=0,
                        command=lambda p=img_path: open_image_screen(base_frame, p))
        button.image = photo
        button.grid(row=idx // 2, column=idx % 2, padx=10, pady=10)

    # Enable Mouse and Touch Scrolling
    def on_touch_scroll(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind("<B1-Motion>", on_touch_scroll)

def open_image_screen(base_frame, image_path):
    """
    Displays a fullscreen window for the selected image with a timer, accept, and cancel buttons.

    :param image_path: Path to the selected image.
    """
    global has_voted
    has_voted = False
    clear_frame(base_frame)
    # image_window.attributes('-fullscreen', True)
    # image_window.configure(bg='white')

    # Frame to control the Widgets
    frame1 = Frame(base_frame,
                    height=1024,
                    width=600,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Display Image
    photo = PhotoImage(file=image_path)
    lbl = Label(frame1, image=photo)
    lbl.image = photo
    lbl.pack(pady=(50, 10))

    # Timer Label
    time_label = Label(frame1, text="Time Left: 5 seconds", bg='white', font=("Arial", 24))
    time_label.pack(pady=(20, 10))

    # Accept and Cancel Buttons
    accept_img = PhotoImage(file="buttons/accept_test.png")
    btn_accept = Button(frame1, image=accept_img, command=lambda: accept_image(image_path, base_frame))
    btn_accept.image = accept_img
    btn_accept.pack(side="left", padx=10, pady=10)

    cancel_img = PhotoImage(file="buttons/cancel_test.png")
    btn_cancel = Button(frame1, image=cancel_img, command=lambda: cancel_image(image_path, base_frame))
    btn_cancel.image = cancel_img
    btn_cancel.pack(side="right", padx=10, pady=10)

    # Start Timer
    start_timer(frame1, 5, time_label, lambda: accept_image(image_path, base_frame))

def start_timer(frame, seconds, time_label, on_timeout):
    """
    Starts a countdown timer and updates the timer label. Calls `on_timeout` when time runs out.

    :param frame: The parent frame where the timer runs.
    :param seconds: Total seconds for the countdown.
    :param time_label: Label to display the remaining time.
    :param on_timeout: Function to execute when the timer expires.
    """
    def countdown(time_left):
        if time_left > 0:
            time_label.config(text=f"Time Left: {time_left} seconds")
            frame.after(1000, countdown, time_left - 1)
        else:
            on_timeout()

    countdown(seconds)

# shutdown_img = PhotoImage(file="../buttons/shutdown_test.png") 
# d = Button(bottom_frame, image=shutdown_img, bg= 'grey', fg='grey',command=verify_shutdown) 
# d.grid(row=0,column=0, padx=80, pady=10) 

# home_img = PhotoImage(file = "../buttons/home_test.png") 
# h = Button(bottom_frame, image=home_img, bg= 'grey',fg='grey',command=verify_home) 
# h.grid(row=0,column=1, padx=80, pady=10)
        
# show_constituency_screen()

# root.after(100, show_constituency_screen)\
# clear_frame(root)

base_frame = Frame(root, bg="red")
base_frame.pack(fill='both', expand=True)

open_vote_window(base_frame)
# home(root, "small")
root.mainloop()
