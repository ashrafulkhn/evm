import RPi.GPIO as GPIO
import time

# GPIO pin number in BCM mode
SERVO_PIN = 18

# Frequency for the servo motor (typically 50 Hz)
FREQ = 50

# Duty cycle values for 0 and 180 degrees (adjust as per your servo specifications)
DUTY_MIN = 2.5  # Corresponds to 0 degrees
DUTY_MAX = 12.5  # Corresponds to 180 degrees

def angle_to_duty_cycle(angle):
    """
    Convert angle (0-180) to duty cycle.
    """
    return DUTY_MIN + (angle / 180.0) * (DUTY_MAX - DUTY_MIN)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Initialize PWM
pwm = GPIO.PWM(SERVO_PIN, FREQ)
pwm.start(0)

try:
    while True:
        # Move the servo in 30-degree steps
        for angle in range(0, 181, 30):  # 0 to 180 degrees
            duty = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(duty)
            print(f"Angle: {angle}°, Duty Cycle: {duty:.2f}%")
            time.sleep(1)  # Pause for the servo to reach the position

        # Return the servo back to 0 degrees
        for angle in range(180, -1, -30):  # 180 to 0 degrees
            duty = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(duty)
            print(f"Angle: {angle}°, Duty Cycle: {duty:.2f}%")
            time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    pwm.stop()
    GPIO.cleanup()
