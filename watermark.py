import Image, ImageEnhance
import re

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    im = Image.open(str(im))
    mark = Image.open(str(mark))
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tiled':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scaled':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    elif position == "bottomleft":
        x = 0 
        y = im.size[1]-mark.size[1]
        layer.paste(mark, (x, y))
    elif position == "bottomright":
        x = im.size[0]-mark.size[0] 
        y = im.size[1]-mark.size[1]
        layer.paste(mark, (x, y))
    elif position == "upperright":
        x = im.size[0]-mark.size[0]
        y = 0
        layer.paste(mark, (x, y))
    elif position == "upperleft":
        x = 0 
        y = 0
        layer.paste(mark, (x, y))
    else:
        if position[0].endsWith("%") and position[1].endsWith("%"):
            px = re.search("(?P<num>.*)%", position[0].toUtf8()).group(1).toInt()[0]
            py = re.search("(?P<num>.*)%", position[1].toUtf8()).group(1).toInt()[0]
            x = px*im.size[0]/100
            y = py*im.size[1]/100
            position = (x, y)
        else:
            position = (position[0].toInt()[0], position[1].toInt()[0])
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)
