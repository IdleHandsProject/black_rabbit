import cv2
import json
import sys
from PIL import Image

# Load the pixel map
def load_pixel_map(filename="pixel_grid.pxl"):
    with open(filename, "r") as f:
        data = f.readlines()
        num_pixels = int(data[0].strip())  # First line should be the number of pixels
        pixel_coords = json.loads("".join(data[1:]))  # Load the coordinates array from JSON
    return pixel_coords

# Load a video frame and display pixel output
def display_frame_as_text(video_path, pixel_coords):
    # Open the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return
    
    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read frame from video.")
        cap.release()
        return
    
    # Resize frame to 74x51 if needed (the frame should already be this size)
    frame_resized = cv2.resize(frame, (74, 51))
    img = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
    
    # Map the colors to pixel coordinates
    output = []
    for idx, (x, y) in enumerate(pixel_coords):
        # Get pixel color at (x, y)
        if x < 74 and y < 51:  # Ensure coordinates are within bounds
            color = img.getpixel((x, y))  # Returns (R, G, B)
            output.append(f"Pixel {idx + 1} at ({x}, {y}): Color {color}")
    
    # Print output
    for line in output:
        print(line)

    cap.release()

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python display_frame_as_text.py <video_file>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    pixel_coords = load_pixel_map()
    display_frame_as_text(video_path, pixel_coords)
