int[][] ledCoordinates;
int numPixels;
float scaleFactor = 5;  // Set the scale factor here (0.5 for 50% of original size)

void setup() {
  // Manually calculate the scaled dimensions
  size(380, 258);  // Hard-coded dimensions for 2000 x 2000 scaled by 0.5
  
  background(0);  // Set background color to white
  
  // Read coordinates from the .pxl file
  loadLEDCoordinates("coordinates_grid_mirrored.pxl");
  
  // Apply the scaling factor
  scale(scaleFactor);
  
  // Set fill color and no stroke for the circles
  fill(255, 0, 0);  // Red color for LED circles
  noStroke();
  
  // Draw the circles at the LED coordinates
  for (int i = 0; i < numPixels; i++) {
    int x = ledCoordinates[i][0];
    int y = ledCoordinates[i][1];
    
    // Draw a 10-pixel diameter circle at each coordinate
    ellipse(x+1, y+1, 1, 1);
  }
}

void draw() {
  // No need to draw continuously in this case
}

// Function to load LED coordinates from the .pxl file
void loadLEDCoordinates(String filename) {
  String[] lines = loadStrings(filename);
  numPixels = int(lines[0]);
  ledCoordinates = new int[numPixels][2];
  String coordinateLines = join(lines, "");
  coordinateLines = coordinateLines.substring(coordinateLines.indexOf("[") + 1, coordinateLines.lastIndexOf("]")).trim();
  String[] coordsList = split(coordinateLines, "],[");
  for (int i = 0; i < numPixels; i++) {
    String coord = coordsList[i].replace("[", "").replace("]", "").trim();
    String[] coords = split(coord, ',');
    ledCoordinates[i][0] = int(trim(coords[0]));
    ledCoordinates[i][1] = int(trim(coords[1]));
  }
}
