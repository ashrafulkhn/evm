from escpos.printer import File
from PIL import Image, ImageDraw, ImageFont
import os
import time
import io
from barcode import EAN13
from barcode.writer import ImageWriter
import barcode

# Function to print an image with a border and frame
def print_image_old(printer, image_path):
    frame_size = (350, 350)  # Frame including border
    image_size = (250, 250)  # Image size inside frame
    offset = 50

    # Create a frame with a border
    frame = Image.new("RGB", frame_size, "white")
    draw = ImageDraw.Draw(frame)
    draw.rectangle([(0, 0), (frame_size[0] - 1, frame_size[1] - 1)], outline="black", width=3)

    image = Image.open(image_path).resize(image_size, Image.Resampling.LANCZOS)
    frame.paste(image, (offset, offset))

    # Print the frame
    # printer.image(frame)
    frame.show()
    printer.cut()

# Function to print an image with a border and frame
def print_image(printer, image_path):
    # Define frame dimensions and image offset
    frame_size = (350, 350)  # Frame dimensions
    image_size = (250, 250)  # Image dimensions
    offset = 50  # Offset for centering the image

    # Create a white background frame
    frame = Image.new("RGBA", frame_size, (255, 255, 255, 255))  # RGBA for transparency support
    draw = ImageDraw.Draw(frame)
    draw.rectangle([(0, 0), (frame_size[0] - 1, frame_size[1] - 1)], outline="black", width=3)

    # Open and resize the image
    image = Image.open(image_path).resize(image_size, Image.Resampling.LANCZOS)

    # Ensure the image has an alpha channel
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Paste the image onto the white frame with transparency handling
    frame.paste(image, (offset, offset), image)  # Use the image as its own mask for transparency

    # Convert the final image to RGB (remove transparency if needed for printing)
    final_image = frame.convert("RGB")

    # Save or show the result (for testing purposes)
    # final_image.show()  # Display the frame with the pasted image
    # final_image.save("output_preserved_image.png")  # Save the result

    printer.image(final_image)
    printer.cut()

# Function to print barcode and status with a border
def print_barcode_status_old(printer, barcode_value, vote_status):
    frame_width = 350
    frame_height = 100
    barcode_width = 15
    barcode_height = 5

    frame = Image.new("RGB", (frame_width, frame_height), "white")
    draw = ImageDraw.Draw(frame)

    # Draw border
    draw.rectangle([(0, 0), (frame_width - 1, frame_height - 1)], outline="black", width=3)

    # Load font (Adjust path or use a default if custom fonts aren't available)
    try:
        font = ImageFont.truetype("arial.ttf", 25)
    except IOError:
        font = ImageFont.load_default()

    if vote_status.upper() == "VOTED":
        # Draw barcode
        # printer.barcode(barcode, "EAN13", width=2, height=30, pos="OFF", align_ct=True)
        buffer = io.BytesIO()
        print("DEBUG:: Bugger Creted.")

                # Define writer options for custom size
        writer_options = {
            "module_width": barcode_width / 10.0,  # Convert width from mm to cm
            "module_height": barcode_height / 10.0,  # Convert height from mm to cm
            "font_size": 10,  # Adjust the text font size if needed
            "text_distance": 5,  # Distance between the text and the barcode
            "quiet_zone": 6.5,  # Quiet zone width
        }

        ean = EAN13(barcode_value, writer=ImageWriter())
        ean.write(buffer, options=writer_options)
        print("DEBUG:: Written to buffer.")
        # Move the buffer pointer to the beginning
        buffer.seek(0)

        # Open the buffer as a PIL image, Now we can do all operations required on this one PIL image.
        barcode_image = Image.open(buffer)
        # barcode_image = barcode_image.resize((50,200), Image.Resampling.LANCZOS)

        # Convert the barcode to image and rotate to 90 degrees.
        bar_image = barcode_image.rotate(90)

        # Align the image to be on the left of the paper.
        # printer.image(bar_image)
        # bar_image.show()

        # Add text in the middle
        # bbox = font.getbbox(vote_status)
        # text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # draw.text(((frame_width - text_width) // 2, (frame_height - text_height) // 2), vote_status, font=font, fill="black")
        # printer.image(frame)
    elif vote_status.upper() == "REJECTED":
        # Only draw the status in the middle
        bbox = font.getbbox(vote_status)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((frame_width - text_width) // 2, (frame_height - text_height) // 2), vote_status, font=font, fill="black")
        printer.image(frame)

    # frame.show()
    printer.cut()

def print_barcode_status(printer, barcode_value, vote_status):
    frame_width = 350
    frame_height = 350
    barcode_width = 2  # Width of the barcode's module (bar width in mm)
    barcode_height = 30  # Height of the barcode in mm

    # Create the frame
    frame = Image.new("RGBA", (frame_width, frame_height), (255, 255, 255, 255))  # White background
    draw = ImageDraw.Draw(frame)

    # Draw border
    draw.rectangle([(0, 0), (frame_width - 1, frame_height - 1)], outline="black", width=3)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    if vote_status.upper() == "VOTED":
        # Generate barcode as PIL Image
        buffer = io.BytesIO()
        writer_options = {
            "module_width": barcode_width / 10.0,
            "module_height": barcode_height / 10.0,
            "font_size": 2,
            "text_distance": 2,
            "quiet_zone": 2,
        }
        ean = EAN13(barcode_value, writer=ImageWriter())
        ean.write(buffer, options=writer_options)
        buffer.seek(0)
        barcode_image = Image.open(buffer).convert("RGBA")  # Ensure RGBA mode

        # Rotate barcode images
        barcode_right = barcode_image.rotate(90, expand=True)
        barcode_left = barcode_image.rotate(270, expand=True)

        # Extract alpha channel for transparency handling
        mask_right = barcode_right.split()[-1]  # Extract the alpha channel
        mask_left = barcode_left.split()[-1]

        # Paste rotated barcodes on the frame
        frame.paste(barcode_left, (5, (frame_height - barcode_left.height) // 2), mask_left)
        frame.paste(barcode_right, (frame_width - barcode_right.width - 5, (frame_height - barcode_right.height) // 2), mask_right)

        # Draw the vote_status in the middle
        # text_width, text_height = draw.textsize(vote_status, font=font)
        bbox = font.getbbox(vote_status)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = (frame_width - text_width) // 2
        text_y = (frame_height - text_height) // 2
        draw.text((text_x, text_y), vote_status, font=font, fill="black", align="center")

    elif vote_status.upper() == "REJECTED":
        # Draw the vote_status in the middle
        # text_width, text_height = draw.textsize(vote_status, font=font)
        bbox = font.getbbox(vote_status)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = (frame_width - text_width) // 2
        text_y = (frame_height - text_height) // 2
        draw.text((text_x, text_y), vote_status, font=font, fill="black", align="center")

    # Convert frame to RGB for printing
    final_image = frame.convert("RGB")

    # Send to printer (for testing, we'll just save the image)
    # final_image.show()  # Display the frame
    final_image.save("barcode_status_frame.png")  # Save the result
    printer.image(final_image)
    printer.cut()

# Function to print blank space with a border
def print_blank(printer, width):
    frame_width = 350
    frame_height = width
    frame = Image.new("RGB", (frame_width, frame_height), "white")
    draw = ImageDraw.Draw(frame)

    # Draw border
    draw.rectangle([(0, 0), (frame_width - 1, frame_height - 1)], outline="black", width=3)

    # Print the blank space with border
    printer.image(frame)
    printer.cut()

# Main function
def main():
    # Printer setup
    try:
        print("Printer selection started.")
        top_printer = File("/dev/usb/lp0")  # Path to the printer in Linux
        top_printer.set(font='a', align="center", width=1, height=1)

        # Project directory and image path
        project_dir = os.getcwd()  # Get current working directory
        image_path = os.path.join(project_dir, "Camera.png")  # Image path
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        # Step 1: Print image
        print("Printing image...")
        print_image(top_printer, image_path)
        time.sleep(5)  # 2-second delay

        # # Step 2: Print barcode and status
        # print("Printing barcode and status (VOTED)...")
        # print_barcode_status(top_printer, "123456789012", "VOTED")
        # time.sleep(5)  # 2-second delay

        print("Printing barcode and status (REJECTED)...")
        print_barcode_status(top_printer, "984756354", "REJECTED")
        time.sleep(5)  # 2-second delay

        # Step 3: Print blank space
        print("Printing blank space...")
        print_blank(top_printer, 200)

        # top_printer.text("Thank you!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'top_printer' in locals():
            top_printer.close()

if __name__ == "__main__":
    main()
