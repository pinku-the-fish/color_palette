from ColorBin import ColorBin
import numpy as np

rnd = np.random.default_rng(seed=4723794)
color_bins = [ColorBin() for _ in range(5)]

for cb in color_bins:
    how_many_pixels = rnd.integers(0, 100)
    cb.pixels = list(zip(rnd.integers(0, 255, size=how_many_pixels, endpoint=True),
                         rnd.integers(0, 255, size=how_many_pixels, endpoint=True),
                         rnd.integers(0, 255, size=how_many_pixels, endpoint=True)))
    cb.process_pixels()

print(sorted(color_bins, key=lambda el: el.pixels_number, reverse=True))
