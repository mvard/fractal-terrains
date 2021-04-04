#!/bin/python3
import random
import sys
from collections import namedtuple

import PIL.ImageDraw as ImageDraw
from PIL import Image

Point = namedtuple("Point", "x y")

IMAGE_WIDTH = 513
IMAGE_HEIGHT = 256
IMAGE_FILL = 32

def generate_heights(roughness, H):
    points = [Point(0, IMAGE_HEIGHT), Point(IMAGE_WIDTH - 1, IMAGE_HEIGHT)]
    next_points = []

    while points[0].x + points[1].x > 2:
        next_points = [points[0]]
        for i in range(0, len(points) - 1):
            midpoint_x = (points[i].x + points[i + 1].x)/2
            midpoint_y = (points[i].y + points[i + 1].y)/2
            next_points.append(
                    Point(midpoint_x, midpoint_y + random.randint(-roughness, roughness))
                )
            next_points.append(points[i + 1])
        roughness = int(roughness * 2 ** (-H))
        points = next_points

    return points

# normalization
def normalize_heights(points):
    min_height = min(points, key=lambda x: x[1])[1]
    max_height = max(points, key=lambda x: x[1])[1]
    height_range = max_height - min_height
    norm_height_range = IMAGE_HEIGHT - IMAGE_FILL
    points = list(
        map(lambda p: (p[0], (p[1] - min_height) * (norm_height_range) / height_range + 32), points)
    )

    return points

def render_heights_to_png(points, filename):
    points.insert(0, (0, 0))
    points.append((IMAGE_WIDTH - 1, 0))

    # generate image
    image = Image.new("L", (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.polygon(points, fill=255)
    image.save(filename)

def main():
    H = 0.7
    roughness = 20
    points = generate_heights(roughness, H)
    points = normalize_heights(points)
    render_heights_to_png(points, "temp.png")

    sys.exit(0)

if __name__ == "__main__":
    main()
