import math
def rotate(x,y,theta):
    return (x*math.cos(theta) - y*math.sin(theta), x*math.sin(theta) + y*math.cos(theta))

def shiftbyalignment(alignment):
    if alignment == 1:
        x = -2.5
        y = 0
    elif alignment == 2:
        x = 2.5
        y = 0
    elif alignment == 4:
        x = 0
        y = 0.5
    elif alignment == 5:
        x = -2.5
        y = 0.5
    elif alignment == 6:
        x = 2.5
        y=0.5
    elif alignment == 8:
        x = 0
        y = -0.5
    elif alignment == 9:
        x = -2.5
        y = -0.5
    elif alignment == 10:
        x = 2.5
        y = 0.5
    else:
        x = 0
        y = 0
    return (x,y)

def shfitCoordinate(shape, alignment, rad):
    factor = 1
    xshift = shiftbyalignment(alignment)[0]
    yshift = shiftbyalignment(alignment)[1]
    point = shape.getPart(0)
    point.X += (rotate(xshift,yshift,rad)[0]*factor)
    point.Y += (rotate(xshift,yshift,rad)[1]*factor)
    return point