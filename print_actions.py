import random

def print_image(img_path):
    global print_select	
    rand = random.randint(1, 2)
    GPIO.output(led_r, GPIO.LOW)
    GPIO.output(led_g, GPIO.HIGH)
    if rand == 1:
        print_select = 1	
    elif rand == 2:
        print_select = 2
    if print_select == 1:
     #   p1.writelines(vote_status + "\n")
        p1._raw(b'\x1b@')
        p1.set(align='center')
        p1.set(font='a', align = "center", width=1, height=1)
        p1._raw(b'\x1b\x21x')
        p1.image(img_path)
        bottom_motor_re()
     #   time.sleep(1)
        time.sleep(3)
        #bottom_motor()
        bottom_glass_on()
        
        message = confirm()
        p1._raw(b'\n')
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
        p1.image('../combined_image.png')
        barcode_datåa = "12345678"
        p1._raw(b'\x1dV\x00')
        p1.cut()
        p1.flush()
        #time.sleep(0.1)
        bottom_motor()
        time.sleep(6)
        bottom_glass_off()
        GPIO.output(led_r, GPIO.HIGH)
        GPIO.output(led_g, GPIO.LOW)

    elif print_select == 2:
        p2._raw(b'\x1b@')
        p2.set(align='center')
        p2.set(font='a', align = "center", width=1, height=1)
        p2._raw(b'\x1b\x21x')
        p2.image(img_path)
        time.sleep(1)
        top_motor_re()
        time.sleep(3)
        top_glass_on()
        #top_motor
        message = confirm()
        p2._raw(b'\n')
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
        p2.image('../combined_image.png')
        barcode_datåa = "12345678"
        p2._raw(b'\x1dV\x00')
        p2.cut()
        p2.flush()
        top_motor()
        time.sleep(6)
        top_glass_off()
        GPIO.output(led_r, GPIO.HIGH)
        GPIO.output(led_g, GPIO.LOW)