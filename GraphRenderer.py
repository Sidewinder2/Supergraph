import math
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

def get_circular_graph_coords(x, y, node_keys, radius):
    # Calculates coordinates in a circle
    # returns dictionary containing node keys to coordinates
    return_dict = dict()  # returns coordinates for circle of circles

    assert len(node_keys) > 0
    deg_current = 0
    deg_increment = 2 * math.pi / len(node_keys)

    for circle in node_keys:
        coords = VectorMath.polar_to_cartesian(deg_current, radius)
        coords[0] += x
        coords[1] += y
        return_dict[circle] = (coords)
        deg_current += deg_increment

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
            surface.line((x1, y1, x2, y2), edge_color, line_width)

    im.save(filename)   # write image to file

def draw_circle(surface,x,y,radius,color):
    # wrapper to render circles in PIL
    surface.ellipse([x-radius,y-radius,x+radius,y+radius],color)