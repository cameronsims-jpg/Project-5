# Project-5
Image Processing Application

## Overview
This project is a GUI-based Image Processing Application. The program loads an input image and allows the user to apply 10 different filters of pixel-based and full-image transformations. Those filters include grayscale, sephia, invert, flips, mirrors, blur, and edge detection.

## Version
Requires:
- python3  
- Tkinter 
- Pillow (to display the images)

## Image Processing Features
- **Grayscale** – converts each pixel to its average intensity
- **Sephia** – applies a tone transformation
- **Invert** – changes pixels to negative using RGB inversion
- **Highlight Purple** – preserves purple-tinted pixels and grays out all others
- **Flip Horizontal** – flips the image top to bottom
- **Flip Vertical** – flips the image left to right
- **Mirror Horizontal** – copies the top half onto the bottom half
- **Mirror Vertical** – copies the left half onto the right half
- **Edge Detect** – uses gradient magnitude and highlights edges
- **Blur** – applies a weighted 3×3 blur kernel that blurs image

## Usage
Run from the command line:
```
python image_processor.py <imagefile>
```

## Testing
Examples
```
python image_processor.py flower.jpg
```
