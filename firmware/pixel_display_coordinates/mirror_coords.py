import sys
# Function to load the coordinates from the .pxl file
def load_coordinates(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Debugging: Print the lines read from the file
    print("File content:")
    for line in lines:
        print(line.strip())

    # First line is the number of pixels
    num_pixels = int(lines[0].strip())
    coordinates = []

    # Parsing the lines containing coordinates
    print("\nParsed coordinates:")
    for line in lines[2:num_pixels + 2]:  # Skip the first 2 lines (count and opening bracket)
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Remove any trailing commas and ensure the line has brackets
        line = line.rstrip(',').strip()  
        if line.startswith('[') and line.endswith(']'):
            # Remove the outer brackets
            line = line[1:-1].strip()  
            try:
                # Split by comma and extract x, y coordinates
                x, y = map(int, line.split(','))
                coordinates.append((x, y))  # Append the coordinate as a tuple
                print(f"Parsed: {x}, {y}")  # Debugging: Print each parsed coordinate
            except ValueError:
                print(f"Skipping invalid line: {line}")

    # Debugging: Print the final list of coordinates
    print("\nFinal list of coordinates:", coordinates)
    
    return coordinates

# Function to find the right-most pixel (highest x value)
def find_right_most_pixel(coordinates):
    if not coordinates:
        raise ValueError("No coordinates found! The coordinate list is empty.")
    right_most_x = max(x for x, y in coordinates)  # Find max x value
    return right_most_x

# Function to mirror the coordinates along the y-axis
def mirror_coordinates(coordinates, center_x):
    mirrored_coordinates = []
    for x, y in coordinates:
        mirrored_x = center_x + (center_x - x)  # Mirror the x-coordinate
        mirrored_coordinates.append((mirrored_x, y))  # Keep the y-coordinate the same
    return mirrored_coordinates

# Function to save the mirrored coordinates to a new .pxl file
def save_coordinates(output_filename, original_coordinates, mirrored_coordinates):
    num_pixels = len(original_coordinates) + len(mirrored_coordinates)
    with open(output_filename, 'w') as file:
        file.write(f"{num_pixels}\n[\n")
        
        # Write original coordinates
        for coord in original_coordinates:
            file.write(f"[{coord[0]},{coord[1]}],\n")
        
        # Write mirrored coordinates
        for coord in mirrored_coordinates:
            file.write(f"[{coord[0]},{coord[1]}],\n")
        
        file.write("]\n")

# Main function to process the mirroring
def process_mirroring(input_file, output_file):
    # Load the original coordinates
    coordinates = load_coordinates(input_file)
    
    # Check if any coordinates were loaded
    if not coordinates:
        print("Error: No valid coordinates were found in the input file.")
        return
    
    # Find the right-most x value and add 5 to define the mirror axis
    right_most_x = find_right_most_pixel(coordinates)
    center_x = right_most_x + 1
    
    # Mirror the coordinates based on the center_x
    mirrored_coordinates = mirror_coordinates(coordinates, center_x)
    
    # Save both original and mirrored coordinates into a new file
    save_coordinates(output_file, coordinates, mirrored_coordinates)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 mirror_coords.py <input file(pxl)> <output file>")
        sys.exit(1)
    
    #video_path = sys.argv[1]
    #pixel_grid_path = "pixel_grid.pxl"
    #play_video_on_leds(video_path, pixel_grid_path)

    input_file = sys.argv[1]  # Replace with your coordinates.pxl file
    output_file = sys.argv[2]  # Output file for mirrored coordinates

    #input_file = 'coordinates_grid.pxl'  # Replace with your coordinates.pxl file
    #output_file = 'coordinates_grid_mirrored.pxl'  # Output file for mirrored coordinates

    process_mirroring(input_file, output_file)
