import math

def polar_to_cartesian(direction, magnitude):
    # converts a vector into cartesian coordinates
    x = magnitude * math.cos(direction)
    y = magnitude * math.sin(direction)
    return [x, y]

def angle_trunc(a):
    # used to fix negative values in point_direction
    while a < 0.0:
        a += math.pi * 2
    return a

def point_direction(coord1, coord2):
    # obtains direction in degrees from [x1,y1] to [x2,y2]
    dy = coord2[1] - coord1[1]
    dx = coord2[0] - coord1[0]
    return angle_trunc(math.atan2(dy, dx)) * 180 / math.pi