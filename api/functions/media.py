from PIL import Image

inputfile = "/Users/halley/Documents/warsaw.jpeg"
outputfile = "/Users/halley/Documents/compress.jpeg"

im = Image.open(inputfile)
im.save(outputfile, optimize=True, quality=30)
