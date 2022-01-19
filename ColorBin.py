import numpy as np


class ColorBin:

    def __init__(self, center: tuple = (None, None, None), bin_3d_position: tuple = (None, None, None)):
        self.center = center
        self.bin_3d_position = bin_3d_position
        self.pixels = []
        self.average_pixel = None
        self.pixels_number = int
        self.distance = None

    def __repr__(self) -> str:
        return f"3d{self.bin_3d_position}: #{self.pixels_number}, avg{self.average_pixel}"

    def process_pixels(self):
        self.pixels_number = len(self.pixels)
        if self.pixels_number > 0:
            self.average_pixel = np.mean(np.array(self.pixels), axis=0)
        else:
            self.average_pixel = None



