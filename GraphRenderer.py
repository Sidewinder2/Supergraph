import math
import random
from PIL import Image, ImageDraw
import VectorMath

def draw_circular_graph(node_keys, edges, filename="Graph Renders\\test.png",
                        image_width = 400, image_height = 400,
                        inner_radius = 10, outer_radius = 100,
                        circle_color = (255,255,255), edge_color = (0,0,0), background_color = (255,0,0),
                        line_width = 1):
    # wraps graph renderer to draw points in a circular fashion around a central point

    coordinates = get_circular_graph_coords(image_width / 2, image_height / 2, node_keys, outer_radius)
    render_coordinates(coordinates=coordinates,edges=edges, filename=filename, image_width=image_width,
                                     image_height=image_height,circle_radius=inner_radius,circle_color=circle_color,
                                     edge_color=edge_color,background_color = background_color, line_width = line_width)

def draw_scatter_graph(node_keys, edges, filename="Graph Renders\\test.png",
                        image_width = 400, image_height = 400, inner_radius = 10, margin = 0,
                        circle_color = (255,255,255), edge_color = (0,0,0), background_color = (255,0,0),
                        line_width = 1):
    # wraps graph renderer to draw points in a scattered fashion

    coordinates = get_scatter_graph_coords(image_width, image_height, node_keys, margin)
    render_coordinates(coordinates=coordinates,edges=edges, filename=filename, image_width=image_width,
                                     image_height=image_height,circle_radius=inner_radius,circle_color=circle_color,
                                     edge_color=edge_color,background_color = background_color, line_width = line_width)

def get_circular_graph_coords(x, y, node_keys, radius):
    # Calculates coordinates in a circle
    # returns dictionary containing node keys to coordinates
    return_dict = dict()  # returns coordinates for each node

    assert len(node_keys) > 0
    deg_current = 0
    deg_increment = float(360 / len(node_keys))

    for circle in node_keys:
        coords = VectorMath.polar_to_cartesian(deg_current, radius)
        coords[0] += x
        coords[1] += y
        return_dict[circle] = coords
        deg_current += deg_increment

    return return_dict

def get_scatter_graph_coords(width, height, node_keys, margin):
    # Calculates coordinates in a scatterplot
    # returns dictionary containing node keys to coordinates
    return_dict = dict()  # returns coordinates for each node

    assert len(node_keys) > 0
    assert width > margin * 2, "Margin must be less than image width"
    assert height > margin * 2, "Margin must be less than image height"

    for scatterpoint in node_keys:
        x = random.randint(margin, width - margin)
        y = random.randint(margin, height - margin)
        return_dict[scatterpoint] = [x,y]

    return return_dict

def render_coordinates(filename, coordinates, edges, image_width, image_height, circle_radius, circle_color, edge_color, background_color, line_width):
    # renders coordinates and edges into an image
    assert isinstance(coordinates, dict)

    im = Image.new('RGBA', (image_width, image_height), background_color)
    surface = ImageDraw.Draw(im)

    # draw nodes
    for node_key in coordinates.keys():
        draw_circle(surface, coordinates[node_key][0], coordinates[node_key][1], circle_radius, circle_color)

    # draw edges
    for edge in edges:
        leftkey = edge[0]
        rightkey = edge[1]
        if leftkey != rightkey:
            x1 = int(coordinates[leftkey][0])
            y1 = int(coordinates[leftkey][1])
            x2 = int(coordinates[rightkey][0])
            y2 = int(coordinates[rightkey][1])
            draw_arrow(surface,x1,y1,x2,y2,"both",edge_color,line_width,5,10)

    im.save(filename)   # write image to file

def draw_circle(surface,x,y,radius,color):
    # wrapper to render circles in PIL
    surface.ellipse([x-radius,y-radius,x+radius,y+radius],color)

def draw_arrow(surface,x1,y1,x2,y2,arrow_ends, arrow_color = (0,0,0), line_width = 1, arrow_width = 5, arrow_height = 10):
    # draws a line with an arrowhead(s) between two points

    assert arrow_ends in ["both","right"]   # arrow ends. Determines which side gets arrows
    assert isinstance(arrow_height,float) or isinstance(arrow_height,int)
    assert arrow_height > 0

    dist = math.hypot(x2 - x1, y2 - y1)     # get distance between two end points

    # do nothing if the distance is the same
    if dist == 0:
        return

    # draw line between end points
    surface.line((x1, y1, x2, y2), arrow_color, width=line_width)

    if arrow_height * 2 <= dist:
        # obtain vectors which determine arrow width perpendicular to the line
        direction = VectorMath.point_direction((x1,y1),(x2,y2))
        left_dir = direction + 90
        left_vect = VectorMath.polar_to_cartesian(left_dir,arrow_width)
        right_dir = direction + 270
        right_vect = VectorMath.polar_to_cartesian(right_dir, arrow_width)

        # obtain coordinate arrow_height of way from left end point to right end point
        midleft_vect = VectorMath.polar_to_cartesian(direction, arrow_height)
        midpoint_left = [x1 + midleft_vect[0], y1 + midleft_vect[1]]

        # obtain coordinate (dist - arrow height) of way from left end point to right end point
        midright_vect = VectorMath.polar_to_cartesian(direction,dist - arrow_height)
        midpoint_right = [x1+midright_vect[0],y1+midright_vect[1]]

        # draw left arrow if needed
        if arrow_ends == "both":
            arrow_left = (midpoint_left[0] + left_vect[0], midpoint_left[1] + left_vect[1]) # add left arrow vector to left coord
            arrow_right = (midpoint_left[0] + right_vect[0], midpoint_left[1] + right_vect[1]) # add right arrow vector to left coord
            surface.polygon([arrow_left, arrow_right, (x1,y1)], fill=arrow_color) # draw triangle for left arrow

        # draw right arrow
        arrow_left = (midpoint_right[0] + left_vect[0], midpoint_right[1] + left_vect[1]) # add left arrow vector to right coord
        arrow_right = (midpoint_right[0] + right_vect[0], midpoint_right[1] + right_vect[1]) # add left arrow vector to right coord
        surface.polygon([arrow_left, arrow_right, (x2, y2)], fill=arrow_color ) # draw triangle for right arrow
