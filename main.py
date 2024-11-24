import math
import os
import time


# Function to rotate a point around the Y-axis (vertical)
def rotate_y(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    new_x = cos_a * x - sin_a * z
    new_z = sin_a * x + cos_a * z
    return new_x, y, new_z


# Function to rotate a point around the X-axis (horizontal)
def rotate_x(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    new_y = cos_a * y - sin_a * z
    new_z = sin_a * y + cos_a * z
    return x, new_y, new_z


# Function to map 3D coordinates to 2D for ASCII rendering
def project(x, y, z, scale, width, height):
    # Perspective projection formula to reduce the 3D to 2D
    fov = 4  # Field of view factor
    factor = fov / (z + 5)  # Perspective factor
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
    "\033[90m",  # Gray
]

# Reset color
reset_color = "\033[0m"


# Draw the rotating pyramid in ASCII
def draw_pyramid(angle_x, angle_y):
    # Define the 3D coordinates of the pyramid vertices
    base_points = [
        (1, -1, 1),  # Front-right base vertex
        (1, 1, 1),  # Back-right base vertex
        (-1, 1, 1),  # Back-left base vertex
        (-1, -1, 1)  # Front-left base vertex
    ]

    # Top vertex of the pyramid
    top_vertex = (0, 0, 2)

    # Rotate all vertices around X and Y axes
    rotated_base = [rotate_y(*rotate_x(x, y, z, angle_x), angle_y) for x, y, z in base_points]
    rotated_top = rotate_y(*rotate_x(top_vertex[0], top_vertex[1], top_vertex[2], angle_x), angle_y)

    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Set up the terminal window size
    width, height = 40, 20
    scale = 10  # Size scaling factor

    # Create an empty canvas
    canvas = [[' ' for _ in range(width)] for _ in range(height)]

    # Function to draw a line between two points on the canvas
    def draw_line(x1, y1, x2, y2, color):
        # Bresenham's line algorithm to draw lines between two points
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < width and 0 <= y1 < height:
                canvas[y1][x1] = color + '*' + reset_color  # Mark the point with an asterisk and color

            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    # Draw pyramid faces by connecting the rotated vertices
    for i in range(4):
        x1, y1 = project(*rotated_base[i], scale, width, height)
        x2, y2 = project(*rotated_base[(i + 1) % 4], scale, width, height)
        x3, y3 = project(*rotated_top, scale, width, height)

        # Draw the three edges of each triangle face with different colors
        color = colors[i % len(colors)]
        draw_line(x1, y1, x2, y2, color)
        draw_line(x2, y2, x3, y3, color)
        draw_line(x3, y3, x1, y1, color)

    # Print the canvas to the terminal
    for row in canvas:
        print(''.join(row))

    time.sleep(0.1)  # Slow down the loop for visibility


# Main loop to continuously spin the pyramid on both axes
def main():
    angle_x = 0
    angle_y = 0
    while True:
        draw_pyramid(angle_x, angle_y)
        angle_x += 0.1  # Rotate on X-axis
        angle_y += 0.1  # Rotate on Y-axis


if __name__ == "__main__":
    main()
