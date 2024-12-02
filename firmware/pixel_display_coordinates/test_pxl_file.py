import json

# Load and test pixel map file
try:
    with open("pixel_grid.pxl", "r") as f:
        data = f.readlines()
        num_pixels = int(data[0].strip())  # First line should be the number of pixels
        pixel_coords = json.loads("".join(data[1:]))  # Load the coordinates array from JSON

    # Check that we have the correct number of pixels
    if len(pixel_coords) != num_pixels:
        print(f"Error: Expected {num_pixels} pixels, but found {len(pixel_coords)} in the file.")
    else:
        print(f"Loaded {num_pixels} pixel coordinates successfully.")
        
    # Print out a sample of coordinates to verify
    for i, (x, y) in enumerate(pixel_coords[:2960]):  # Display the first 10 for testing
        print(f"Pixel {i + 1}: (x: {x}, y: {y})")

except FileNotFoundError:
    print("Error: pixel_grid.pxl file not found.")
except json.JSONDecodeError:
    print("Error: pixel_grid.pxl file format is incorrect.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
