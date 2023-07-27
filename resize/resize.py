import os
from PIL import Image

def main():
    file = os.getenv('IN_FILE')

    img = Image.open(file)
    res = img.resize((225, 300))

    res.save(os.getenv('OUT_FILE'))

if __name__ == "__main__":
    main()