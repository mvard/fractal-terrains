#!/bin/python3
import random
from PIL import Image
import PIL.ImageDraw as ImageDraw

imageWidth = 513
imageHeight = 256
H = 0.7
displacement = 50
points = [(0, imageHeight), (imageWidth - 1, imageHeight)]
next_points = []

while points[0][0] + points[1][0] > 2:
    next_points = [points[0]]
    for i in range(0, len(points) - 1):
        midpoint_x = (points[i][0] + points[i + 1][0])/2
        midpoint_y = (points[i][1] + points[i + 1][1])/2
        next_points.append(
            (midpoint_x, midpoint_y + random.randint(-displacement, displacement))
        )
        next_points.append(points[i + 1])
    displacement = int(displacement * 2 ** (-H))
    points = next_points

# normalization
minimum = min(points, key=lambda x: x[1])[1]
maximum = max(points, key=lambda x: x[1])[1]
points = list(map(lambda p: (p[0], (p[1] - minimum) * (252 - 32) / (maximum - minimum) + 32), points))

points.insert(0, (0, 0))
points.append((imageWidth - 1, 0))

# generate image
im = Image.new("L", (imageWidth, imageHeight))
draw = ImageDraw.Draw(im)
draw.polygon(points, fill=255)
im.save("temp.png", "PNG")

exit(0)
