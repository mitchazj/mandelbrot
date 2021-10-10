# Generate the Mandelbrot set

from PIL import Image
import numpy as np
import time


def MandelbrotIter(c):
    z = 0
    for i in range(0, 255):
        z = z * z + c
        if abs(z) > 2:
            return i
    return 255


def Mandelbrot(x, y):
    return MandelbrotIter(complex(x, y))


def MandelbrotImage(width, height):
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (Mandelbrot(i/width*4-2, j/height*4-2), 0, 0)
    return image


def main():
    start = time.time()
    image = MandelbrotImage(1000, 1000)
    image.save("mandelbrot.png")
    print("Time:", time.time() - start)


main()
