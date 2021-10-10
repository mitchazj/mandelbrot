# Generate the Mandelbrot set

import time
from PIL import Image


def mandelbrot_iter(c):
    """Get the mandelbrot value for a complex number c"""
    z = 0
    for i in range(0, 255):
        z = z * z + c
        if abs(z) > 2:
            return i
    return 255


def mandelbrot(x, y):
    """Compute the Mandelbrot value at x, y"""
    return mandelbrot_iter(complex(x, y))


def mandelbrot_image(width, height):
    """Compute a Mandelbrot image with dimensions width, height"""
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (mandelbrot(i/width*4-2, j/height*4-2), 0, 0)
    return image


def main():
    """Generate the Mandelbrot image"""
    start = time.time()
    image = mandelbrot_image(1000, 1000)
    image.save("mandelbrot.png")
    print("Time:", time.time() - start)


main()
