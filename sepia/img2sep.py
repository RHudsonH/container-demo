import os
from PIL import Image, ImageEnhance
import PIL

def main():
    file = os.getenv('IN_FILE')

    img = Image.open(file)
    img = img.convert("RGB")
    x,y = img.size
    for ly in range(y):
        for lx in range(x):
            coordinate = lx, ly
            r,g,b = img.getpixel(coordinate)
            sr = int(r * 0.8 + 2)
            sg = int(g * 0.6 + 2)
            sb = int(b * 0.4 + 2)
            img.putpixel((lx,ly), (sr, sg, sb))


    img.save(os.getenv('OUT_FILE'))

if __name__ == "__main__":
    main()