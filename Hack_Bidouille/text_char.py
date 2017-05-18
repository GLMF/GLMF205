from PIL import Image, ImageFont, ImageDraw
import numpy as np

def text2image(text, fontName='Hack-Regular.ttf', pt=11, saveName=None):
    font = ImageFont.truetype(fontName, pt)
    (w, h) = font.getsize(text)
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    if not saveName is None:
        image.save(saveName)
    return image

if __name__ == '__main__':
    image = text2image('LINUX MAGAZINE')
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    arr = np.where(arr, '#', ' ')
    for row in arr:
        print(''.join(row))
