import cv2
import numpy as np
import time
import sys
from rpi_ws281x import PixelStrip, Color

# LED configuration
LED_COUNT = 2960      # Number of LED pixels
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 5          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # Channel 0 for GPIOs 18, 20, or 21


# Load the pixel map
def load_pixel_grid(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_pixels = int(lines[0].strip())
    pixel_map = []
    for line in lines[1:]:
        if line.strip():
            try:
                x, y = map(int, line.strip("[], \n").split(','))
                pixel_map.append((x, y))
            except ValueError:
                print(f"Skipping malformed line: {line}")

    if len(pixel_map) != num_pixels:
        print(f"Warning: Expected {num_pixels} pixels but got {len(pixel_map)} in the file.")

    return pixel_map

def adjust_gamma(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)

def adjust_brightness_and_gamma(frame, brightness_factor=0.5, gamma=2.0):
    # Apply brightness reduction
    frame = frame * brightness_factor
    frame = np.clip(frame, 0, 255)  # Ensure values stay within valid range

    # Apply gamma correction
    gamma_correction = 255 * (frame / 255) ** (1 / gamma)
    return np.clip(gamma_correction, 0, 255).astype(np.uint8)

# Function to turn all LEDs off
def turn_off_leds():
    for i in range(2960):
        strip.setPixelColor(i, Color(0, 0, 0))  # Set color to black (off)
    strip.show()  # Send the signal to turn off LEDs


# Function to play the video on LEDs
def play_video_on_leds(video_path, pixel_grid_path):
    pixel_map = load_pixel_grid(pixel_grid_path)
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Initialize FPS calculation variables
    frame_count = 0
    fps_start_time = time.time()
    fps_interval = 1  # 1 second interval for averaging FPS

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        frame = cv2.resize(frame, (75, 51))  # Ensure frame is 74x51
        # Extract color values for each pixel in the correct order

        # Apply gamma correction
        frame = adjust_gamma(frame, gamma=0.4)

        # Adjust contrast and brightness
        frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=1)

        # Inside your main video processing loop, before reordering the pixels, apply the adjustment:
        adjusted_frame = adjust_brightness_and_gamma(frame, brightness_factor=0.5, gamma=2.0)

        reordered_pixels = [frame[y, x] for x, y in pixel_map]

        # Write the pixels to the LED strip
        for i, (b, g, r) in enumerate(reordered_pixels):
            strip.setPixelColor(i, Color(r, g, b))

        strip.show()
        frame_count += 1
        if (time.time() - fps_start_time) >= fps_interval:
            fps = frame_count / (time.time() - fps_start_time)
            print(f"FPS: {fps:.2f}")

            # Reset the counter and timer
            frame_count = 0
            fps_start_time = time.time()
        #time.sleep(0.5)  # 50 FPS frame delay (adjust if needed)

    cap.release()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))  # Set color to black (off)
    strip.show()  # Send the signal to turn off LEDs
    strip.show()  # Clear the LEDs at the end

# Usage
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <video_path> <pixel grid file>")
        sys.exit(1)

    video_path = sys.argv[1]
    pixel_grid_path = sys.argv[2]
    #pixel_grid_path = "pixel_grid.pxl"
    time.sleep(1)
    play_video_on_leds(video_path, pixel_grid_path)

