import cv2
import numpy as np
import time
import sys

# Load the pixel grid map
def load_pixel_grid(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Process each line, skipping the first line and ignoring empty/malformed lines
        pixel_map = []
        for line in lines[1:]:
            line = line.strip("[], \n")
            if line:  # Check if line is not empty
                try:
                    x, y = map(int, line.split(','))
                    pixel_map.append((x, y))
                except ValueError:
                    print(f"Warning: Skipping malformed line: {line}")
    return pixel_map


def simulate_fps(video_path, pixel_grid_path):
    import cv2
    import time
    
    # Load pixel map
    pixel_map = load_pixel_grid(pixel_grid_path)

    # Open video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    total_time = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to 74x51 if necessary
        frame_rgb = cv2.resize(frame, (75, 51))  # Ensure frame is 74x51
        
        # Start timing
        start_time = time.time()
        
        # Reorder pixels using the pixel map with boundary check
        reordered_pixels = []
        for x, y in pixel_map:
            if 0 <= y < 51 and 0 <= x < 75:  # Ensure coordinates are within bounds
                reordered_pixels.append(frame_rgb[y, x])
            else:
                print(f"Warning: Skipping out-of-bounds coordinate ({x}, {y})")
        time.sleep(0.09)
        # End timing
        
        elapsed_time = time.time() - start_time
        total_time += elapsed_time
        frame_count += 1
        print(f"frame")

    cap.release()
    
    # Calculate FPS
    avg_time_per_frame = total_time / frame_count if frame_count > 0 else 0
    fps = 1 / avg_time_per_frame if avg_time_per_frame > 0 else 0
    print(f"Average FPS: {fps:.2f}")


if __name__ == "__main__":
    video_path = sys.argv[1]  # Path to the video file
    pixel_grid_path = "pixel_grid.pxl"  # Path to the pixel grid map file

    simulate_fps(video_path, pixel_grid_path)
