import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import Image

rnd = np.random.default_rng(seed=654982)
sample_coverage = 0.0001
im = Image.open(r"data\tst2.jpg")
drawn_pixels_number = int(sample_coverage * im.width * im.height)
if drawn_pixels_number > 2500:
    drawn_pixels_number = 2500
drawn_xy = [(rnd.integers(low=0, high=im.width), rnd.integers(low=0, high=im.height)) for _ in
            range(drawn_pixels_number)]

sample_rgb = list(map(im.getpixel, drawn_xy))


# -----------------------------------------------------

class Bean:

    def __init__(self, centre, bean_number):
        self.centre = centre
        self.x_spread = [centre[0] - beans_size/2, centre[0] + beans_size/2]
        self.y_spread = [centre[1] - beans_size/2, centre[1] + beans_size/2]
        self.z_spread = [centre[2] - beans_size/2, centre[2] + beans_size/2]
        self.bean_number = bean_number


pixels_in_beans_list = []
beans_list = []
beans_size = 51

for r in range(0, int(255/beans_size)):
    beans_list.append([])
    for g in range(0, int(255 / beans_size)):
        beans_list[r].append([])
        for b in range(0, int(255 / beans_size)):
            beans_list[r][g].append([])

for x in range(0, 255, beans_size):
    for y in range(0, 255, beans_size):
        for z in range(0, 255, beans_size):
            beans_list[math.floor(x/beans_size)][math.floor(y/beans_size)][math.floor(z/beans_size)].append(Bean((x+(beans_size/2), y+(beans_size/2), z+(beans_size/2)), (math.floor(x/beans_size), math.floor(y/beans_size), math.floor(z/beans_size))))

for r in range(0, int(255/beans_size)):
    pixels_in_beans_list.append([])
    for g in range(0, int(255 / beans_size)):
        pixels_in_beans_list[r].append([])
        for b in range(0, int(255 / beans_size)):
            pixels_in_beans_list[r][g].append([])

for pixel in sample_rgb:
    pixels_in_beans_list[math.floor(pixel[0] / beans_size)][math.floor(pixel[1] / beans_size)][math.floor(pixel[1] / beans_size)].append(pixel)
    # print(math.floor(pixel[0]/beans_size), math.floor(pixel[1]/beans_size), math.floor(pixel[1]/beans_size))
    # print(pixel)

print(pixels_in_beans_list)
print(beans_list)

# -----------------------------------------------------

# for later addressing elements as: [::, 0], [::, 1], [::, 2]
sample_rgb = np.array(sample_rgb)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
color_values_scaled = [(c[0] / 255, c[1] / 255, c[2] / 255) for c in sample_rgb]
ax.scatter(sample_rgb[::, 0], sample_rgb[::, 1], sample_rgb[::, 2],
           alpha=0.2, c=color_values_scaled)
ax.w_xaxis.line.set_color("red")
ax.set_xlim3d(0, 255)
ax.set_xlabel('red')
ax.w_yaxis.line.set_color("green")
ax.set_ylim3d(0, 255)
ax.set_ylabel('green')
ax.w_zaxis.line.set_color("blue")
ax.set_zlim3d(0, 255)
ax.set_zlabel('blue')
plt.show()

# print(im)
