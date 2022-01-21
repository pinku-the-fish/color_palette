from PIL import Image, ImageDraw
from main import bin_pixels
import numpy as np
import copy


def color_choosing(bins, color_difference=100, palette_length=10):
    bins = copy.deepcopy(bins)
    colors_by_difference = [bins[0].average_pixel]  # colors_by_difference - cbd
    percentage_of_different_colors = 0.9
    cbd_num = 20

    for b in bins:
        color_ok = 0
        for clr in colors_by_difference:
            if (abs(clr[0] - b.average_pixel[0]) + abs(clr[1] - abs(b.average_pixel[1])) +
                    abs(clr[2] - abs(b.average_pixel[2]))) > color_difference:
                color_ok += 1
        if color_ok > len(colors_by_difference)*percentage_of_different_colors:
            colors_by_difference.append((b.average_pixel[0], b.average_pixel[1], b.average_pixel[2]))
        if len(colors_by_difference) == cbd_num:
            break

    if len(colors_by_difference) > palette_length:
        return colors_by_difference[0:palette_length]
    else:
        return colors_by_difference


def draw(im, colors):
    tile_size = int(im.width / len(colors))
    palette = Image.new('RGB', (im.width, tile_size), (0, 0, 0))
    dst = Image.new('RGB', (im.width, im.height + tile_size))
    palette_draw = ImageDraw.Draw(palette)

    ctr = 0
    for clr in colors:
        palette_draw.rectangle(((ctr, 0), ((ctr + 1) * tile_size, tile_size)), fill=(int(clr[0]), int(clr[1]), int(clr[2])))
        ctr += tile_size
        if ctr/tile_size == len(colors):
            break

    dst.paste(im, (0, 0))
    dst.paste(palette, (0, im.height))
    dst.save(r"data/clrs.jpg", quality=100)


# ////////////////////////////////

image = r"data/tst6.jpg"
the_bins, bins_3d = bin_pixels(image)
draw(Image.open(image), color_choosing(the_bins))
