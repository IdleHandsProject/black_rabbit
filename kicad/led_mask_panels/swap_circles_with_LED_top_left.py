import re

# File paths
input_file = 'rabbit_mask.kicad_pcb'
output_file = 'rabbit_mask_mod_orged.kicad_pcb'

# LED footprint template
led_template = '''(footprint "project_footprints:LED_BB-2020BGR-TRB" (layer "F.Cu")
    (tstamp {tstamp})
    (at {x} {y})
    (attr smd)
    (fp_text reference "{ref}" (at 0.175 -2.635) (layer "F.SilkS") hide
        (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text value "LED_BB-2020BGR-TRB" (at 0 2.365) (layer "F.Fab") hide
        (effects (font (size 1 1) (thickness 0.15)))
    )
)
'''

# Circle pattern to match center and end coordinates
circle_pattern = re.compile(r'\(gr_circle \(center ([\d.]+) ([\d.]+)\) \(end ([\d.]+) ([\d.]+)\)')

# Radius we're interested in (0.617)
target_radius = 0.617

def calculate_radius(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

led_counter = 1  # Start the counter for naming LEDs

def replace_circles_with_leds(input_file, output_file):
    global led_counter
    circles = []  # List to store the circles

    # First pass: collect all circles with the correct radius
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            match = circle_pattern.search(line)
            if match:
                x1, y1, x2, y2 = map(float, match.groups())
                radius = calculate_radius(x1, y1, x2, y2)
                
                if abs(radius - target_radius) < 0.001:  # Match the radius 0.617
                    # Store the circle info: index of the line and coordinates
                    circles.append((i, x1, y1))

    # Sort circles first by Y (top to bottom), then by X (left to right)
    circles.sort(key=lambda c: (c[2], c[1]))  # Sort by Y (index 2), then X (index 1)

    # Second pass: replace circles with LEDs in the sorted order
    with open(output_file, 'w') as outfile:
        skip_until_closing_paren = False  # To skip until we hit the closing parenthesis
        circle_indices = {i for i, _, _ in circles}  # Create a set of circle line indices

        for i, line in enumerate(lines):
            if skip_until_closing_paren:
                # Skip lines until we find the closing parenthesis of the circle block
                if line.strip().startswith(')'):
                    skip_until_closing_paren = False  # End skipping once we hit the closing parenthesis
                continue  # Skip this line

            if i in circle_indices:
                # Get the corresponding circle data (X, Y) from the list
                _, x, y = next(circle for circle in circles if circle[0] == i)
                
                # Generate a tstamp for the new footprint
                tstamp = re.sub(r'[^\w]', '', "{}{}".format(x, y))  # Create a basic tstamp from the coordinates
                ref = "D{}".format(led_counter)  # Create a unique reference name, e.g., D1, D2, ...
                led_counter += 1  # Increment the LED counter
                
                # Replace the circle with the LED footprint at the center (x1, y1)
                led_footprint = led_template.format(tstamp=tstamp, ref=ref, x=x, y=y)
                outfile.write(led_footprint)

                # Start skipping lines until the closing parenthesis
                skip_until_closing_paren = True
            else:
                outfile.write(line)


# Run the function
replace_circles_with_leds(input_file, output_file)
