from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import os
import platform
import subprocess
class ImageService:
    def __init__(self):
        self.original_img = None     # for Pillow operations
        self.last_file_path = None   # path to the original file

    def load_img(self, file_path):
        """Loads an image and stores its path"""
        self.last_file_path = file_path
        self.original_img = Image.open(file_path)
        return self.original_img

    def save_img_with_wm(self, wm_text, font_size=32, position="Bottom-Right"):
        """Adds a watermark and saves the image"""
        if self.original_img is None:
            raise ValueError("Image not loaded.")

        img = self.original_img.copy().convert("RGBA")
        font_path = Path("fonts/Roboto.ttf")
        font = ImageFont.truetype(str(font_path), size=font_size)
        # font = ImageFont.load_default()

        text = wm_text

        # Draw the watermark text
        draw = ImageDraw.Draw(img)
        w, h = img.size
        bbox = draw.textbbox((0, 0), wm_text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        coords = {
            "Top-Left": (10, 10),
            "Top-Right": (w - tw - 10, 10),
            "Center": ((w - tw) // 2, (h - th) // 2),
            "Bottom-Left": (10, h - th - 10),
            "Bottom-Right": (w - tw - 10, h - th - 10)
        }
        x, y = coords.get(position, coords["Bottom-Right"])
        draw.text((x, y), wm_text, font=font, fill=(0, 0, 0, 128))

        # Create output directory if it doesn't exist
        output_dir = Path("Images/output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filename based on original image name
        stem = Path(self.last_file_path).stem
        output_path = output_dir / f"{stem}_watermarked.png"

        # Save the watermarked image
        img.save(output_path)
        return output_path

    def open_output_folder(self):
        """Opens the folder containing the saved image"""
        if not self.last_file_path:
            raise ValueError("The file has not been saved yet.")

        folder = Path("Images/output").resolve()

        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{folder}"')
        elif platform.system() == "Darwin":
            subprocess.call(["open", folder])
        else:
            subprocess.call(["xdg-open", str(folder)])

