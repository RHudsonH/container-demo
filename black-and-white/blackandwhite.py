import os
from PIL import Image, ImageEnhance
import PIL

file = os.getenv('IN_FILE')

img = Image.open(file)
img = img.rotate(270, PIL.Image.Dither.NONE, expand = 1)
img = img.convert("L")
img.save(os.getenv('OUT_FILE'))