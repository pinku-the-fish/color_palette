from main import *
import copy

sorted_bins, bins_3d, im = bin_pixels(r"data/tst5.jpg")


def bmeeef(sb):
    sb = copy.deepcopy(sb)
    sb[0].average_pixel = (-6, -6, -6)
    print(sb[0])


print(sorted_bins[0])
bmeeef(sorted_bins)
print(sorted_bins[0])