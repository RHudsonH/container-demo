import os
from PIL import Image


file = os.getenv('IN_FILE')

img = Image.open(file)
res = img.resize((225, 300))

res.save(os.getenv('OUT_FILE'))