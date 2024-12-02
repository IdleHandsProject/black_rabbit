import time
from rpi_ws281x import PixelStrip, Color

# LED configuration:
LED_COUNT = 2960        # Number of LED pixels.
LED_PIN = 18            # GPIO pin connected to the pixels (18 uses PWM).
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 5            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 13    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0         # Set to 1 for GPIOs 13, 19, 41, 45 or 53

# Initialize the LED strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Function to turn all LEDs off
def turn_off_leds():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))  # Set color to black (off)
    strip.show()  # Send the signal to turn off LEDs

# Execute the function
if __name__ == "__main__":
    turn_off_leds()
    print("All LEDs turned off.")
