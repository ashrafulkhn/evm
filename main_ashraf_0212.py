import tkinter as tk
from tkinter import Frame, RAISED, BOTH, PhotoImage, Button, Label, Entry, Toplevel, END, Canvas, Scrollbar, TclError
from ttkthemes import themed_tk as tk
from os import system
from tkinter import simpledialog, messagebox, Canvas
from PIL import Image
import os
import time
from print_actions import print_image
from escpos.printer import *

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
            print("If")
        # elif not has_voted:
        #     print("Elif")
        #     on_timeout()  # Execute the callback when timer runs out
        else:
            print("Else")
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

# Screens :: Constituency Screen

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
    # messagebox.showinfo("Contact Polling Officer", "Please Contact your polling officer.")
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
                        bd=0,
    # `                   highlightthickness=0, 
                        highlightbackground="white", 
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="flat",
                        borderwidth=0,
                        activebackground="white",
                        activeforeground="white",
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

# Screen :: Enlarged Image Screen
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
    # btn_cancel = Button(frame1, image=cancel_img, command=lambda: cancel_image(image_path, base_frame))
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
        # clear_frame(base_frame)
        # messagebox.showinfo(title =None, message = "Vote Successful")
        confirm_print_screen(base_frame)

def cancel_image(image_path,base_frame):
#    encoding = "shift-jis"
#    message = "Cancelled"
#    encoded_text = message.encode(encoding)
#    print_image(image_path, encoded_text)
    clear_frame(base_frame)
    # messagebox.showwarning(title =None, message = "Vote Cancelled")
    # open_vote_window(base_frame)
    voting_terminated_screen(base_frame)

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
    cancel_vote(base_frame)

def cancel_vote(base_frame):
    print("Vote Print Cancelled.")
    voting_terminated_screen(base_frame)

def on_print_yes_clicked(base_frame):
    print("Vote print confirmed.")
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
                       font=("Arial", 35),
                       text="Thank you for Voting."
                       )

    head_label.place(relx=0.5, rely=0.4, anchor="center")

    # Centering the message label
    message_label = Label(frame1,
                          bg="white",
                          fg="black",
                          font=("Arial", 25),
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
    print("Thank you for Voting.")


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