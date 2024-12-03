import tkinter as tk
from tkinter import Frame, RAISED, BOTH, PhotoImage, Button, Label, Entry, Toplevel, END, Canvas, Scrollbar, TclError, Image
from ttkthemes import themed_tk as tk
from os import system
from tkinter import Canvas
import os, time, random
# from print_actions import print_image
from escpos.printer import *
import barcode
from barcode.writer import ImageWriter
from PIL import Image,ImageDraw, ImageFont

import RPi.GPIO as GPIO

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
    pwm_top.start(6)
    time_delay_top = decrement_value_in_file(file_path_top)
    print(time_delay_top)
    time.sleep(3)
    pwm_top.stop()

def bottom_motor():
    pwm_bottom = GPIO.PWM(bottom_motor_pin, 50)
    pwm_bottom.start(8)
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

def top_glass_on():
    GPIO.output(top_glass_pin, GPIO.LOW)
   # time.sleep(6)
   # GPIO.output(glass_T, GPIO.HIGH)
    
def top_glass_off():
    GPIO.output(top_glass_pin, GPIO.HIGH)

def bottom_glass_on():
    GPIO.output(bottom_glass_pin, GPIO.LOW)
   # time.sleep(6)
    #GPIO.output(glass_B, GPIO.HIGH)
    
def bottom_glass_off():
    GPIO.output(bottom_glass_pin, GPIO.HIGH)

# =========PRINTER===========================
# PRINTER SETUP
# Printer 1 Path in Linux
top_printer = File("/dev/usb/lp0")
top_printer.set(font='a',align="center",width=1,height=1)

# Printer 2 Path in Linux
bottom_printer = File("/dev/usb/lp1")
bottom_printer.set(font='a',align="center",width=1,height=1)

def print_image(img_path):
    global print_select	
    rand = random.randint(1, 2)
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.output(green_led_pin, GPIO.HIGH)
    if rand == 1:
        print_select = 1	
    elif rand == 2:
        print_select = 2

    if print_select == 1:
     #   p1.writelines(vote_status + "\n")
        bottom_printer._raw(b'\x1b@')
        bottom_printer.set(align='center')
        bottom_printer.set(font='a', align = "center", width=1, height=1)
        bottom_printer._raw(b'\x1b\x21x')
        bottom_printer.image(img_path)
        bottom_motor_re()
     #   time.sleep(1)
        time.sleep(3)
        #bottom_motor()
        bottom_glass_on()
        
        # message = confirm()
        # This is the confirmation of print. The return message should be "Voted" or "Cancelled" here.
        message = "Voted"

        bottom_printer._raw(b'\n')
        ean = barcode.get('ean13', '123456789012', writer=ImageWriter())
        filename = ean.save('barcode')
        barcode_image = Image.open(filename)
        barcode_image = barcode_image.rotate(90, expand=True)  
        new_size = (100,200)
        barcode_image = barcode_image.resize(new_size, Image.ANTIALIAS)
       
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

    elif print_select == 2:
        top_printer._raw(b'\x1b@')
        top_printer.set(align='center')
        top_printer.set(font='a', align = "center", width=1, height=1)
        top_printer._raw(b'\x1b\x21x')
        top_printer.image(img_path)
        time.sleep(1)
        top_motor_re()
        time.sleep(3)
        top_glass_on()
        #top_motor

        # message = confirm()
        # This is the confirmation of print. The return message should be "Voted" or "Cancelled" here.

        top_printer._raw(b'\n')
        ean = barcode.get('ean13', '123456789012', writer=ImageWriter())
        filename = ean.save('barcode')
        barcode_image = Image.open(filename)
        barcode_image = barcode_image.rotate(90, expand=True)  
        new_size = (100,200)
        barcode_image = barcode_image.resize(new_size, Image.ANTIALIAS)
       
        barcode_image.save('../resized_rotated_barcode.png')
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
        top_printer.image('../combined_image.png')
        barcode_datåa = "12345678"
        top_printer._raw(b'\x1dV\x00')
        top_printer.cut()
        top_printer.flush()
        top_motor()
        time.sleep(6)
        top_glass_off()
        GPIO.output(red_led_pin, GPIO.HIGH)
        GPIO.output(green_led_pin, GPIO.LOW)

# ============GUI Related Fuctions==========
# ========ROOT WINDOW CREATION==============
root = tk.ThemedTk()
root.title("Vote Printing Machine")
root.geometry('600x1024')
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
            time_label.config(text=f"Time Left to accept: {time_left} seconds")
            frame.after(1000, countdown, time_left - 1)
        # elif not has_voted:
        #     print("Elif")
        #     on_timeout()  # Execute the callback when timer runs out
        else:
            on_timeout()
    countdown(seconds)

# =======Applications Screens==========

# Screen :: Home screen of the Application
def open_vote_window(base_frame):
    """
    Displays a fullscreen window to ask user to vote. Only one Button on this page.

    :param image_path: Frame e.g. base_frame
    """
    clear_frame(base_frame)
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
                        command=lambda: show_constituency_screen(base_frame)
                        )
    btn_vote.pack(expand=True)

# Screen :: Constituency Screen
def show_constituency_screen(base_frame):
    """
    Frame consituency_window details are mentioned here
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
    clear_frame(base_frame)
    voting_terminated_screen(base_frame)

# Screen :: Grid Screen
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
        photo = PhotoImage(file=img_path)
        button = Button(scrollable_frame,
                        image=photo,
                        bd=0,
                        border=4,
                        highlightbackground="white",
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="flat",
                        height=200,
                        width=200,
                        borderwidth=4,
                        activebackground="white",
                        activeforeground="white",
                        command=lambda p=img_path: open_image_screen(base_frame, p))
        
        button.image = photo
        # button.grid(row=idx // 2, column=idx % 2, padx=10, pady=10, sticky="news")

        # Add a label below the image for the file name (without extension)
        file_name = os.path.basename(img_path).split('.')[0]  # Remove the extension
        label = Label(scrollable_frame, text=file_name, bg="#000000", border=4,fg="white", font=("Arial", 20, "bold"), borderwidth=1, relief="solid", padx=5, pady=5)

        button.grid(row=row_image, column=col_image, padx=30, pady=30, sticky="news")      # Buttons in two columns
        label.grid(row=row_label, column=col_label, padx=30, pady=5, sticky="news")     # Labels below the button
        
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
                    height=1024,
                    width=600,
                    bg='white'
                    )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Display Image
    photo = PhotoImage(file=image_path)
    lbl = Label(frame1, 
                image=photo,
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
    lbl.image = photo
    lbl.pack(pady=(50, 10))

    # Timer Label
    time_label = Label(frame1, text="Time Left: 5 seconds", bg='white', font=("Arial", 24))
    time_label.pack(pady=(20, 10))

    # Accept and Cancel Buttons
    accept_img = PhotoImage(file="buttons/accept_test.png")

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

    cancel_img = PhotoImage(file="buttons/cancel_test.png")
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

    # Start Timer
    start_timer(frame1, 5, time_label, lambda: accept_image(image_path, base_frame))

def accept_image(image_path, base_frame):
    global has_voted
    if not has_voted:
        has_voted = True
        print(image_path)
        confirm_print_screen(base_frame)

def cancel_image(image_path,base_frame):
    clear_frame(base_frame)
    # voting_terminated_screen(base_frame)
    grid_screen(base_frame, "small")

# Screen :: Ask to confirm if the print was as selected image
def confirm_print_screen(base_frame):
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
                  text="Is the \n Print as Voted?",
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
                        command=lambda: on_print_yes_clicked(base_frame))
    yes_button.pack(side="left", padx=50)

    no_button = Button(button_frame,
                       text="No",
                       width=10,
                       height=2,
                       bg="#F44336",
                       fg="white",
                       font=("Arial", 15, "bold"),
                       command=lambda: on_print_no_clicked(base_frame))
    no_button.pack(side="right", padx=50)

def on_print_no_clicked(base_frame):
    print_barcode("Voted")
    cancel_vote(base_frame)

def cancel_vote(base_frame):
    print_barcode("Cancelled")
    # print("Vote Print Cancelled.")
    voting_terminated_screen(base_frame)

def on_print_yes_clicked(base_frame):
    # print("Vote print confirmed.")
    voting_thanks_screen(base_frame)

# Screen :: Thank you for Voting Screen
def voting_thanks_screen(base_frame):
    clear_frame(base_frame)  # Clear all previous widgets available on the Frame of this page.
    frame1 = Frame(base_frame,
                   bg="white",
                   width=600,
                   height=1024
                   )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Centering the heading label
    head_label = Label(frame1,
                       bg="white",
                       fg="black",
                       font=("Arial", 35, "bold"),
                       text="Thank you for Voting."
                       )

    head_label.place(relx=0.5, rely=0.4, anchor="center")

    # Centering the message label
    message_label = Label(frame1,
                          bg="white",
                          fg="black",
                          font=("Arial", 25, "bold"),
                          text="All the best :)"
                          )
    message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Arial", 24))
    time_label.place(relx=0.5, rely=0.95, anchor="center")

    # Start Timer
    start_timer(frame1, 5, time_label, lambda: open_vote_window(base_frame))
    # print("Thank you for Voting.")


# Screen :: Vote Terminated Screen
def voting_terminated_screen(base_frame):
    clear_frame(base_frame)  # Clear all previous widgets available on the Frame of this page.
    frame1 = Frame(base_frame,
                   bg="white",
                   width=600,
                   height=1024
                   )
    frame1.pack_propagate(False)
    frame1.pack(fill='both', expand=True)

    # Centering the heading label
    head_label = Label(frame1,
                       bg="white",
                       fg="black",
                       font=("Arial", 35),
                       text="Your Voting is terminated."
                       )
    head_label.place(relx=0.5, rely=0.4, anchor="center")

    # Centering the message label
    message_label = Label(frame1,
                          bg="white",
                          fg="black",
                          font=("Arial", 25),
                          text="Go Back to the Polling Booth Officer"
                          )
    message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Timer Label (positioned at the bottom)
    time_label = Label(frame1,
                       text="Time Left: 5 seconds",
                       bg="white",
                       font=("Arial", 24))
    time_label.place(relx=0.5, rely=0.95, anchor="center")

    # Start Timer
    start_timer(frame1, 5, time_label, lambda: open_vote_window(base_frame))
    print("The voting has been terminated.")

# Continue the main script
base_frame = Frame(root, bg="white")
base_frame.pack(fill='both', expand=True)

open_vote_window(base_frame)
# home(root, "small")
root.mainloop()