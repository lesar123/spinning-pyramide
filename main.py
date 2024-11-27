import math
import os
import time


# Function to rotate a point around the X-axis (horizontal)
def rotate_x(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    new_y = cos_a * y - sin_a * z
    new_z = sin_a * y + cos_a * z
    return x, new_y, new_z


# Function to map 3D coordinates to 2D for ASCII rendering with depth
def project(x, y, z, scale, width, height):
    # Perspective projection formula to reduce the 3D to 2D with enhanced depth
    fov = 5  # Field of view factor
    factor = fov / (z + 5)  # Perspective factor that accounts for depth
    x_projected = int(x * factor * scale + width / 2)
    y_projected = int(y * factor * scale + height / 2)
    return x_projected, y_projected


# Define colors using ANSI escape codes
colors = [
    "\033[91m",  # Red
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[94m",  # Blue
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
    "\033[97m",  # White
]

# Reset color
reset_color = "\033[0m"

# Define a list of characters to make the pyramid prettier
characters = ['*', '#', '@', '%', '&', '!', '+', '=', '-', ':']

# Function to fill the triangle face (scanline fill)
def fill_triangle(x1, y1, x2, y2, x3, y3, canvas, width, height, color, char):
    # Sort points by y-coordinate (top to bottom)
    points = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda p: p[1])

    (x1, y1), (x2, y2), (x3, y3) = points  # Get the sorted points

    # Interpolation function for calculating x at a given y
    def interpolate(x1, y1, x2, y2, y):
        if y2 == y1:
            return x1  # Prevent division by zero for horizontal lines
        return int(x1 + (x2 - x1) * (y - y1) / (y2 - y1))

    # Function to draw a horizontal line between two x-coordinates at a given y
    def draw_line(x1, y1, x2, y2, color, char):
        if x1 > x2:  # Ensure x1 <= x2
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            if 0 <= x < width and 0 <= y1 < height:
                canvas[y1][x] = color + char + reset_color  # Draw pixel

    # Fill the triangle by scanning from top to bottom
    for y in range(y1, y3 + 1):
        if y < 0 or y >= height:
            continue

        # Handle upper part of the triangle (from y1 to y2)
        if y <= y2:
            x_left = interpolate(x1, y1, x2, y2, y)
            x_right = interpolate(x1, y1, x3, y3, y)
        # Handle lower part of the triangle (from y2 to y3)
        else:
            x_left = interpolate(x2, y2, x3, y3, y)
            x_right = interpolate(x1, y1, x3, y3, y)

        # Draw the horizontal line between x_left and x_right for the current y
        draw_line(x_left, y, x_right, y, color, char)


# Draw the rotating pyramid in ASCII
def draw_pyramid(angle_x):
    # Define the 3D coordinates of the pyramid vertices
    base_points = [
        (1, -1, 1),  # Front-right base vertex
        (1, 1, 1),  # Back-right base vertex
        (-1, 1, 1),  # Back-left base vertex
        (-1, -1, 1)  # Front-left base vertex
    ]

    # Top vertex of the pyramid
    top_vertex = (0, 0, 2)

    # Rotate all vertices around X-axis
    rotated_base = [rotate_x(x, y, z, angle_x) for x, y, z in base_points]
    rotated_top = rotate_x(top_vertex[0], top_vertex[1], top_vertex[2], angle_x)

    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Set up the terminal window size
    width, height = 40, 20
    scale = 5  # Size scaling factor for a smaller pyramid

    # Create an empty canvas
    canvas = [[' ' for _ in range(width)] for _ in range(height)]

    # Draw pyramid faces by connecting the rotated vertices
    for i in range(4):
        x1, y1 = project(*rotated_base[i], scale, width, height)
        x2, y2 = project(*rotated_base[(i + 1) % 4], scale, width, height)
        x3, y3 = project(*rotated_top, scale, width, height)

        # Choose a character to display and draw solid filled triangle face
        char = characters[i % len(characters)]
        color = colors[i % len(colors)]
        fill_triangle(x1, y1, x2, y2, x3, y3, canvas, width, height, color, char)

    # Print the canvas to the terminal
    for row in canvas:
        print(''.join(row))

    time.sleep(0.1)  # Slow down the loop for visibility


# Main loop to continuously spin the pyramid around the X-axis
def main():
    angle_x = 0
    while True:
        draw_pyramid(angle_x)
        angle_x += 0.1  # Rotate on X-axis


if __name__ == "__main__":
    main()
