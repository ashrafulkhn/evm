from tkinter import Tk, Frame, Canvas, PhotoImage, Button, Label
from PIL import Image, ImageTk

def button_command():
    print("png Button pressed!")

root = Tk()
root.geometry("600x1024")
root.attributes("-fullscreen", True)

# Frame1 (full size of root)
frame1 = Frame(root, width=600, height=1024, bg="white")
frame1.place(x=0, y=0)

# Frame2 (centered in Frame1)
frame2 = Frame(frame1, width=300, height=150, bg="white")
frame2.place(relx=0.5, rely=0.5, anchor="center")

# Load the image
original_image = Image.open("tiktok.png")  # Replace with the actual image file path

# Create a PhotoImage that fits exactly within Frame2
button_width, button_height = 300, 150  # Frame2's dimensions
image_ratio = original_image.width / original_image.height
frame_ratio = button_width / button_height

if image_ratio > frame_ratio:
    # Image is wider, fit by width
    new_width = button_width
    new_height = int(button_width / image_ratio)
else:
    # Image is taller, fit by height
    new_height = button_height
    new_width = int(button_height * image_ratio)

resized_image = original_image.resize((new_width-5, new_height-5), Image.Resampling.LANCZOS)
button_image = ImageTk.PhotoImage(resized_image)

# Add the image as a Label in Frame2
image_label = Button(frame2, 
                    image=button_image, 
                    highlightthickness=0, 
                    highlightbackground="white", 
                    highlightcolor="white",
                    fg="white",
                    bg="white", 
                    relief="flat",
                    borderwidth=0,
                    activebackground="white",
                    activeforeground="white",
                    command=button_command
                    )
image_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the image
root.mainloop()
