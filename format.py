import drawBot as db
import os
import math
from typing import Tuple, Literal

MINIMUM_MARGIN = 0

BACKGROUND_WIDTH = 1280
BACKGROUND_HEIGHT = 800
FRAME_ASPECT_RATIO = 16 / 10
BLUR_AMOUNT = 50

def getScaling(im: db.ImageObject, mode: Literal['fill', 'fit'], margin: int) -> Tuple[int, int, float, float]:
  srcWidth, srcHeight = db.imageSize(im)
  srcAspectRatio = srcWidth / srcHeight

  outWidth = outHeight = factorWidth = factorHeight = finalX = finalY = 0

  [leftRatio, rightRatio] = [FRAME_ASPECT_RATIO, srcAspectRatio] if mode == 'fill' else [srcAspectRatio, FRAME_ASPECT_RATIO]
  if leftRatio > rightRatio: 
    outWidth = BACKGROUND_WIDTH - (margin * 2)
    outHeight = srcHeight / srcWidth * outWidth
  else:
    outHeight = BACKGROUND_HEIGHT - (margin * 2)
    outWidth = srcWidth / srcHeight * outHeight

  factorWidth  = outWidth  / srcWidth
  factorHeight = outHeight / srcHeight

  finalX = math.floor((BACKGROUND_WIDTH / 2) - (outWidth / 2))
  finalY = math.floor((BACKGROUND_HEIGHT - outHeight) / 2)
  
  return [finalX, finalY, factorWidth, factorHeight]

if __name__ == '__main__':

  inputDirectory = './input'
  outputDirectory = './output'
  for filename in os.listdir(inputDirectory):
      filepath = os.path.join(inputDirectory, filename)

      if os.path.isfile(filepath) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        print(f'Starting file: {filepath}')

        db.newDrawing()
        db.newPage(BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        db.fill(200, 200, 200)
        db.rect(0, 0, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)

        im = db.ImageObject(filepath)
        [finalX, finalY, scaleWidth, scaleHeight] = getScaling(im, 'fill', -BLUR_AMOUNT)
        
        with db.savedState():
          db.translate(finalX, finalY)
          db.scale(scaleWidth, scaleHeight)
          im.gaussianBlur(BLUR_AMOUNT)
          im.colorControls(1, -0.025, 1)
          x, y = im.offset()
          db.image(im, (x, y))
        
        del im, finalX, finalY, scaleWidth, scaleHeight
        im = db.ImageObject(filepath)
        [finalX, finalY, scaleWidth, scaleHeight] = getScaling(im, 'fit', 0)

        with db.savedState():
          db.translate(finalX, finalY)
          db.scale(scaleWidth, scaleHeight)
          db.image(im, (0, 0))

        db.saveImage(os.path.join(outputDirectory, filename).replace('JPG', 'jpg'))
  
  db.endDrawing()