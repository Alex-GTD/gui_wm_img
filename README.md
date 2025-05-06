
---

````markdown
# Image Viewer App

A simple image viewer built with Python and Tkinter.  
Supports opening image files, automatic resizing to fit the screen, and basic canvas interaction.

## Features

- Open and display `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif` files
- Resize large images to fit the window
- Scrollable canvas for oversized images
- Simple and clean UI for quick image preview

## Requirements

- Python 3.9+
- [Pillow](https://pypi.org/project/Pillow/)
- (Optional) [Tkinter](https://docs.python.org/3/library/tkinter.html) (preinstalled with most Python distributions)

## Installation

```bash
pip install -r requirements.txt
````

## Usage

```bash
python main.py
```

## Project Structure

```
.
├── main.py           # GUI application entry point
├── services.py       # Image loading and processing
├── assets/
│   └── logo.png      # Optional watermark/logo (if used)
├── requirements.txt
└── README.md
```
