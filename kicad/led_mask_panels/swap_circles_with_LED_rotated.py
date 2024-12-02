import re

# File paths
input_file = 'rabbit_mask.kicad_pcb'
output_file = 'rabbit_mask_rotated.kicad_pcb'

# LED footprint template
led_template = '''(footprint "project_footprints:LED_SK6812_EC15_1.5x1.5mm" (layer "F.Cu")
    (tstamp {tstamp})
    (at {x} {y} 180)
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
    inside_circle_block = False  # To track if we're in a circle block
    global led_counter
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            match = circle_pattern.search(line)
            if match:
                x1, y1, x2, y2 = map(float, match.groups())
                radius = calculate_radius(x1, y1, x2, y2)
                
                if abs(radius - target_radius) < 0.001:  # Match the radius 0.617
                    # Generate a tstamp for the new footprint
                    tstamp = re.sub(r'[^\w]', '', str(match.groups()))  # Create a basic tstamp from the coordinates
                    ref = "D{}".format(led_counter)  # Create a unique reference name, e.g., LED1, LED2, ...
                    led_counter += 1  # Increment the LED counter
                    
                    # Replace the circle with the LED footprint at the center (x1, y1)
                    led_footprint = led_template.format(tstamp=tstamp, ref=ref, x=x1, y=y1)
                    outfile.write(led_footprint)
                    inside_circle_block = True  # Skip the following lines in this block
                else:
                    outfile.write(line)
            elif inside_circle_block:
                # Skip all the remaining lines in the circle block (like stroke, fill, etc.)
                if line.strip().startswith(')'):  # End of the block
                    inside_circle_block = False  # Exit the circle block
            else:
                outfile.write(line)


# Run the function
replace_circles_with_leds(input_file, output_file)