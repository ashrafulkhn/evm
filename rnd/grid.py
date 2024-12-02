import os
from tkinter import Frame, Canvas, Scrollbar, Button, Label, PhotoImage, Image
from ttkthemes import themed_tk as tk

def clear_frame(frame):
    """Clear all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def open_image_screen(base_frame, img_path):
    """Placeholder function for opening the image screen."""
    print(f"Opening image screen for {img_path}")

def grid_screen(base_frame, image_directory_path):
    """
    Displays a scrollable grid of image buttons. Clicking an image button opens `open_image_screen`.

    :param base_frame: Root Tkinter window or any frame.
    :param image_directory_path: Path to the directory containing images.
    """

    clear_frame(base_frame)

    # Frame to control the label
    frame1 = Frame(base_frame, height=1024, width=600, bg='white')
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

    frame2 = Frame(scrollable_frame, height=20, bg="red")
    frame2.place(relx=1.0, rely=0.9, anchor="center")

    scrollable_frame.bind("<Configure>", configure_scroll_region)
    
    col_image=1 # start from column 1
    row_image=3 # start from row 3 
    col_label=1 # start from column 1
    row_label=4 # start from row 3 

    # Load images from directory and create buttons
    image_files = [os.path.join(image_directory_path, f) for f in os.listdir(image_directory_path) if f.endswith((".png", ".jpg", ".jpeg"))]

    for idx, img_path in enumerate(image_files):
        photo = Image(img_path)
        photo=photo.resize((200, 200))
        photo = PhotoImage(photo)
        
        # Create Button with image
        button = Button(scrollable_frame,
                        image=photo,
                        bd=0,
                        border=4,
                        highlightbackground="white",
                        highlightcolor="white",
                        fg="white",
                        bg="white", 
                        relief="flat",
                        borderwidth=4,
                        activebackground="white",
                        activeforeground="white",
                        command=lambda p=img_path: open_image_screen(base_frame, p))
        button.image = photo  # Keep reference to avoid garbage collection
        
        # Add a label below the image for the file name (without extension)
        file_name = os.path.basename(img_path).split('.')[0]  # Remove the extension
        label = Label(scrollable_frame, text=file_name, bg="#000000", border=4,fg="white", font=("Arial", 20, "bold"), borderwidth=1, relief="solid", padx=5, pady=5)
        
        # Place the button and label in two columns
        # row = idx // 2
        # col = idx % 1
        
        button.grid(row=row_image, column=col_image, padx=30, pady=30, sticky="n")      # Buttons in two columns
        label.grid(row=row_label, column=col_label, padx=30, pady=5, sticky="nsew")     # Labels below the button
        
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

    # Enable Mouse and Touch Scrolling
    def on_touch_scroll(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind("<B1-Motion>", on_touch_scroll)

root = tk.ThemedTk()
root.title("Vote Printing Machine")
root.geometry('600x1024')
root.configure(bg='white')
root.get_themes()
root.wm_attributes('-fullscreen', 'True')
root.set_theme("clearlooks")

# Continue the main script
base_frame = Frame(root, bg="white")
base_frame.pack(fill='both', expand=True)

grid_screen(base_frame, "../print")
# home(root, "small")
root.mainloop()