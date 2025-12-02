import image
import math
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def pixelMapper(old, rgbFunction):
    """Return a new image by applying rgbFunction to every pixel in old."""
    width = old.getWidth()
    height = old.getHeight()
    new = image.EmptyImage(width, height)
    
    for row in range(height):
        for col in range(width):
            pixel = old.getPixel(col, row)
            new.setPixel(col, row, rgbFunction(pixel))
    
    return new


# grayscale
def grayscale(oldPixel):
    R = oldPixel.getRed()
    G = oldPixel.getGreen()
    B = oldPixel.getBlue()
    avgIntensity = (R + G + B) // 3
    return image.Pixel(avgIntensity,avgIntensity, avgIntensity)


# sephia
def sephia(oldPixel):
    R = oldPixel.getRed()
    G = oldPixel.getGreen()
    B = oldPixel.getBlue()

    newR = min(255, int(R * 0.393 + G * 0.769 + B * 0.189))
    newG = min(255, int(R * 0.349 + G * 0.686 + B * 0.168))
    newB = min(255, int(R * 0.272 + G * 0.534 + B * 0.131))

    newPixel = image.Pixel(newR, newG, newB)
    return newPixel


# invert
def negativePixel(oldPixel):
    newRed   = 255 - oldPixel.getRed()
    newGreen = 255 - oldPixel.getGreen()
    newBlue  = 255 - oldPixel.getBlue()
    newPixel = image.Pixel(newRed, newGreen, newBlue)
    return newPixel


# highlight purple
def highlight_purple(oldPixel):
    r = oldPixel.getRed()
    g = oldPixel.getGreen()
    b = oldPixel.getBlue()

    if not (b > g and r > g and b > r // 1.5):
            avg = (r + g + b) // 3   # get the average intensity of the three pixel colors
            return image.Pixel(avg, avg, avg)
    else:
        return image.Pixel(r, g, b)


# vertical flip
def vertical_flip(original):
    height = original.getHeight()
    width = original.getWidth()
    last = width - 1 
    
    flippedImage = image.EmptyImage(width, height)
    for x in range(width):          
        for y in range(height):
            pixel = original.getPixel(last - x, y)
            flippedImage.setPixel(x, y, pixel)
            
    return flippedImage


# horizontal flip
def horizontal_flip(originalImage):
    height = originalImage.getHeight()
    width = originalImage.getWidth()
    last = height - 1   

    flippedImage = image.EmptyImage(width, height)
    for x in range(width):                                 
        for y in range(height):
            pixel = originalImage.getPixel(x, last - y)     
            flippedImage.setPixel(x, y, pixel)              
            
    return flippedImage


# mirror vertical
def mirror_vertical(orig):
    width = orig.getWidth()
    height = orig.getHeight()
    last = width - 1

    mirror_image = image.EmptyImage(width, height)

    # Copy left half normally
    for x in range(width // 2):
        for y in range(height):
            pixel = orig.getPixel(x, y)
            mirror_image.setPixel(x, y, pixel)

    # Copy left half onto right half (mirrored)
    for x in range(width // 2, width):
        for y in range(height):
            pixel = orig.getPixel(last - x, y)
            mirror_image.setPixel(x, y, pixel)

    return mirror_image


# mirror horizontal
def mirror_horizontal(orig):
    width = orig.getWidth()
    height = orig.getHeight()
    last = height - 1

    mirror_image = image.EmptyImage(width, height)

    # Copy top half normally
    for x in range(width):
        for y in range(height // 2):
            pixel = orig.getPixel(x, y)
            mirror_image.setPixel(x, y, pixel)

    # Copy top half onto bottom half (mirrored)
    for x in range(width):
        for y in range(height // 2, height):
            pixel = orig.getPixel(x, last - y)
            mirror_image.setPixel(x, y, pixel)

    return mirror_image


# edge detect
def convolve(originalImage, pixelRow, pixelCol, kernel):
    kernelColBase = pixelCol - 1
    kernelRowBase = pixelRow - 1
    total = 0
    for row in range(kernelRowBase, kernelRowBase+3):
        for col in range(kernelColBase, kernelColBase+3):
            kColIndex = col - kernelColBase
            kRowIndex = row - kernelRowBase
            pixel = originalImage.getPixel(col, row)
            intensity = pixel.getRed()
            total = total + intensity * kernel[kRowIndex][kColIndex]
    return total


def convertToGrayscale(originalImage):
    width = originalImage.getWidth()
    height = originalImage.getHeight()
    modifiedImage = image.EmptyImage(width, height)
    for row in range(height):
        for col in range(width):
            pixel = originalImage.getPixel(col, row)
            pixelIntensity = pixel.getRed() + pixel.getGreen() + pixel.getBlue()
            avgRGB = pixelIntensity // 3
            pixel = image.Pixel(avgRGB, avgRGB, avgRGB)            
            modifiedImage.setPixel(col, row, pixel)
    return modifiedImage


def edge_detect(original, threshold):
    grayscale = convertToGrayscale(original)

    edgeImage = image.EmptyImage(original.getWidth(), original.getHeight())
    black = image.Pixel(0, 0, 0)
    white = image.Pixel(255, 255, 255)
    xMask = [ [-1, -2, -1], [0, 0, 0], [1,2,1] ]
    yMask = [ [1, 0, -1], [2, 0, -2], [1,0,-1] ]
    
    for row in range(1, original.getHeight()-1):
        for col in range(1, original.getWidth()-1):
            gX = convolve(grayscale, row, col, xMask)
            gY = convolve(grayscale, row, col, yMask)
            g = math.sqrt(gX**2 + gY**2)
            if g > threshold:
                edgeImage.setPixel(col, row, black)
            else:
                edgeImage.setPixel(col, row, white) 
    return edgeImage


# blur
def blur_image(original):
    width = original.getWidth()
    height = original.getHeight()

    # 3x3 weighted kernel
    kernel = [
        [1, 2, 1],
        [2, 1, 2],
        [1, 2, 1]
    ]
    kernel_sum = 12 
    blurred = image.EmptyImage(width, height)

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            sumR = 0
            sumG = 0
            sumB = 0

            # apply kernel
            for i in range(3):          # rows
                for j in range(3):      # columns

                    pixel = original.getPixel(col + j - 1, row + i - 1)
                    weight = kernel[i][j]

                    sumR += pixel.getRed()   * weight
                    sumG += pixel.getGreen() * weight
                    sumB += pixel.getBlue()  * weight

            # weighted average
            newR = sumR // kernel_sum
            newG = sumG // kernel_sum
            newB = sumB // kernel_sum

            # was giving ValueError: Error: pixel value 257 is out of range
            newR = max(0, min(255, newR))
            newG = max(0, min(255, newG))
            newB = max(0, min(255, newB))

            blurred.setPixel(col, row, image.Pixel(newR, newG, newB))

    return blurred



class image_processor:
    """Tkinter GUI app for applying image filters."""
    def __init__(self, filename):
        # setup window
        self.root = tk.Tk()
        self.root.title("Image Processing App")

        # load image
        self.original = image.FileImage(filename)
        self.current = self.original

        # options for dropdown
        self.filters = [
            "Grayscale",
            "Sephia",
            "Invert",
            "Highlight Purple",
            "Flip Horizontal",
            "Flip Vertical",
            "Mirror Horizontal",
            "Mirror Vertical",
            "Edge Detect",
            "Blur"
        ]

        self.selected = tk.StringVar(self.root)
        self.selected.set(self.filters[0])
        self.menu = tk.OptionMenu(self.root, self.selected, *self.filters)
        self.menu.pack(pady=10)

        # buttons
        apply_btn = ttk.Button(self.root, text="Apply Filter", command=self.apply_filter)
        reset_btn = ttk.Button(self.root, text="Reset to Original", command=self.reset_image)

        apply_btn.pack(pady=5)
        reset_btn.pack(pady=5)

        # canvas to display image
        self.canvas = tk.Canvas(self.root, width=self.original.getWidth(), height=self.original.getHeight())
        self.canvas.pack()

        self.update_display()

        self.root.mainloop()
    
    def convert_for_tk(self, img):
        width = img.getWidth()
        height = img.getHeight()

        # extract pixel data manually into a 3D list
        pixel_data = []
        for y in range(height):
            row = []
            for x in range(width):
                p = img.getPixel(x, y)
                row.append((p.getRed(), p.getGreen(), p.getBlue()))
            pixel_data.append(row)

        # convert to PIL
        pil = Image.new("RGB", (width, height))
        for y in range(height):
            for x in range(width):
                pil.putpixel((x, y), pixel_data[y][x])

        return ImageTk.PhotoImage(pil, master=self.root)

    def update_display(self):
        tk_image = self.convert_for_tk(self.current)
        self.tk_ref = tk_image  # prevent garbage collection
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    def reset_image(self):
        self.current = self.original
        self.update_display()

    def apply_filter(self):
        choice = self.selected.get()

        if choice == "Grayscale":
            self.current = pixelMapper(self.current, grayscale)

        elif choice == "Sephia":
            self.current = pixelMapper(self.current, sephia)

        elif choice == "Invert":
            self.current = pixelMapper(self.current, negativePixel)

        elif choice == "Highlight Purple":
            self.current = pixelMapper(self.current, highlight_purple)
        
        elif choice == "Flip Horizontal":
            self.current = horizontal_flip(self.current)

        elif choice == "Flip Vertical":
            self.current = vertical_flip(self.current)

        elif choice == "Mirror Horizontal":
            self.current = mirror_horizontal(self.current)

        elif choice == "Mirror Vertical":
            self.current = mirror_vertical(self.current)

        elif choice == "Edge Detect":
            self.current = edge_detect(self.current, threshold=150)

        elif choice == "Blur":
            self.current = blur_image(self.current)
        
        self.update_display()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image_processor.py <imagefile>")
        sys.exit(1)

    filename = sys.argv[1]
    app = image_processor(filename)
