from PIL import Image, ImageDraw
from ColorBin import ColorBin
import numpy as np
import copy


def bin_pixels(image_path: str, bins_number: int = 10, xy_bins_number: int = 10, sample_coverage: float = 0.25,
               max_pixels: int = 100000):
    rnd = np.random.default_rng()
    im = Image.open(image_path)
    drawn_pixels_number = int(sample_coverage * im.width * im.height)
    if drawn_pixels_number > max_pixels:
        drawn_pixels_number = max_pixels

    drawn_xy = [(rnd.integers(low=0, high=im.width), rnd.integers(low=0, high=im.height)) for _ in
                range(drawn_pixels_number)]

    colors = map(im.getpixel, drawn_xy)
    color_bins = [ColorBin() for _ in range(bins_number ** 3)]

    color_bins_3d = []
    for x in range(bins_number):
        color_bins_3d.append([])
        for y in range(bins_number):
            color_bins_3d[x].append([])
            for z in range(bins_number):
                color_bins_3d[x][y].append([])

    bin_size = 256 / bins_number
    bin_ctr = 0

    for ctr_x in range(bins_number):
        for ctr_y in range(bins_number):
            for ctr_z in range(bins_number):
                color_bins[bin_ctr].bin_3d_position = (ctr_x, ctr_y, ctr_z)
                color_bins[bin_ctr].center = (ctr_x * bin_size + (bin_size / 2), ctr_y * bin_size + (bin_size / 2),
                                              ctr_z * bin_size + (bin_size / 2))
                color_bins_3d[ctr_x][ctr_y][ctr_z] = color_bins[bin_ctr]
                bin_ctr += 1

    for k, clr in enumerate(colors):
        bin_pos = [int(np.floor(rgb_val / bin_size)) for rgb_val in clr]
        color_bins_3d[bin_pos[0]][bin_pos[1]][bin_pos[2]].pixels.append(clr)
        color_bins_3d[bin_pos[0]][bin_pos[1]][bin_pos[2]].xy_positions.append(drawn_xy[k])

    for cb in color_bins:
        cb.process_pixels()

    xy_bin_size_x = im.width / xy_bins_number
    xy_bin_size_y = im.height / xy_bins_number

    for the_bin in color_bins:
        for pixel in the_bin.pixels:
            xy_index_x = int(np.floor(pixel[0] / xy_bin_size_x))
            xy_index_y = int(np.floor(pixel[1] / xy_bin_size_y))
            the_bin.xy_indices.add((xy_index_x, xy_index_y))

    sorted_color_bins_with_pixels = list(filter(lambda b: b.pixels_number > 0,
                                                sorted(color_bins, key=lambda el: el.pixels_number, reverse=True)))
    return sorted_color_bins_with_pixels, color_bins_3d


# def basic_color_choosing(sorted_color_bins, color_difference=100, color_number=10):
#     colors = [sorted_color_bins[0].average_pixel]
#
#     color_ok = 0
#     for scb in sorted_color_bins[1:len(sorted_color_bins)]:
#         for clr in colors:
#             if (abs(clr[0] - scb.average_pixel[0]) + abs(clr[1] - abs(scb.average_pixel[1])) +
#                     abs(clr[2] - abs(scb.average_pixel[2]))) > color_difference:
#                 color_ok += 1
#         if color_ok > len(colors):
#             colors.append((scb.average_pixel[0], scb.average_pixel[1], scb.average_pixel[2]))
#         if len(colors) == color_number:
#             break
#
#     return colors
#
#
# def color_choose_color_accent(sorted_color_bins, how_many_closest_farthest):
#     sorted_color_bins = copy.deepcopy(sorted_color_bins)
#     h = sorted_color_bins[0]
#     for scb in sorted_color_bins:
#         scb.distance = np.sqrt((h.center[0] - scb.center[0]) ** 2 + (h.center[1] - scb.center[1]) ** 2 +
#                                (h.center[2] - scb.center[2]) ** 2)
#     bins_by_remoteness = sorted(sorted_color_bins, key=lambda el: el.distance)
#     cut_point = int(0.5 * len(bins_by_remoteness))
#     colors_to_return = []
#     if how_many_closest_farthest[0] != 0:
#         closest_colors = basic_color_choosing(sorted(bins_by_remoteness[0:cut_point], key=lambda el: el.pixels_number,
#                                                      reverse=True), color_number=how_many_closest_farthest[0])
#         colors_to_return = colors_to_return + list(closest_colors)
#
#     if how_many_closest_farthest[1] != 0:
#         farthest_colors = basic_color_choosing(sorted(bins_by_remoteness[cut_point:len(bins_by_remoteness)],
#                                                       key=lambda el: el.pixels_number, reverse=True),
#                                                color_number=how_many_closest_farthest[1])
#         colors_to_return = colors_to_return + list(farthest_colors)
#
#     return colors_to_return
#
#
# def color_choose_xy_accents(sorted_color_bins, how_many_closest_farthest_standard, how_many_closest_farthest_accents):
#     sorted_color_bins = copy.deepcopy(sorted_color_bins)
#     for scb in sorted_color_bins:
#         scb.weight = np.sum(np.std(scb.xy_positions))
#     std_colors = color_choose_color_accent(sorted(sorted_color_bins, key=lambda b: b.weight, reverse=True),
#                                            how_many_closest_farthest_standard)
#     for scb in sorted_color_bins:
#         scb.weight = (1.0 / np.sum(np.std(scb.xy_positions)))
#     acc_colors = color_choose_color_accent(sorted(sorted_color_bins, key=lambda b: b.weight, reverse=True),
#                                            how_many_closest_farthest_accents)
#     colors = list(std_colors) + list(acc_colors)
#
#     return colors
#
#
# def draw(im, colors):
#     tile_size = int(im.width / len(colors))
#     palette = Image.new('RGB', (im.width, tile_size), (0, 0, 0))
#     dst = Image.new('RGB', (im.width, im.height + tile_size))
#     palette_draw = ImageDraw.Draw(palette)
#     ctr = 0
#     for clr in colors:
#         palette_draw.rectangle(((ctr, 0), ((ctr + 1) * tile_size, tile_size)),
#                                fill=(int(clr[0]), int(clr[1]), int(clr[2])))
#         ctr += tile_size
#         if ctr / tile_size == len(colors):
#             break
#
#     dst.paste(im, (0, 0))
#     dst.paste(palette, (0, im.height))
#     dst.save(r"data/clrs.jpg", quality=100)
#

# sorted_bins, bins_3d, image = bin_pixels(r"data/tst20.jpg")
# result = color_choose_xy_accents(sorted_bins, (3, 3), (3, 3))
# draw(image, result)
