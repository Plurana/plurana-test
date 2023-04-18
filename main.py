import random
import yaml
import svgwrite
from math import cos, sin, pi

# Load parameters from the YAML file
with open("parameters.yaml", "r") as file:
    params = yaml.safe_load(file)


def random_choice(options):
    return random.choice(options)


def parse_canvas_size(size_str):
    width, height = size_str.split("x")
    return int(width), int(height)


def deg2rad(degrees):
    return degrees * pi / 180


def rotate(point, angle, center):
    x, y = point
    cx, cy = center
    angle_rad = deg2rad(angle)

    x_rot = cx + (x - cx) * cos(angle_rad) - (y - cy) * sin(angle_rad)
    y_rot = cy + (x - cx) * sin(angle_rad) + (y - cy) * cos(angle_rad)

    return x_rot, y_rot


class Component:
    def __init__(self, id, style):
        self.id = id
        self.style = style

    def draw(self, dwg, center, size, rotation):
        pass


class Circle(Component):
    def draw(self, dwg, center, size, rotation):
        circle = dwg.circle(
            center=center,
            r=size / 2,
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        return circle


class Rect(Component):
    def draw(self, dwg, center, size, rotation):
        x, y = center
        rect = dwg.rect(
            insert=(x - size / 2, y - size / 2),
            size=(size, size),
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        if rotation != 0:
            rect.rotate(rotation, center)
        return rect


class Ellipse(Component):
    def draw(self, dwg, center, size, rotation):
        x, y = center
        ellipse = dwg.ellipse(
            center=center,
            r=(size / 2, size / 4),
            fill=random_choice(self.style["fill_options"]),
            opacity=random_choice(self.style["opacity_options"])
        )
        if rotation != 0:
            ellipse.rotate(rotation, center)
        return ellipse


# Create instances of the components based on the YAML parameters
def create_component(params):
    component_type = params["type"]
    style = params["style"]

    if component_type == "Circle":
        return Circle(params["id"], style)
    elif component_type == "Rect":
        return Rect(params["id"], style)
    elif component_type == "Ellipse":
        return Ellipse(params["id"], style)
    elif component_type == "GridGroup":
        return GridGroup(
            params["id"],
            style,
            params["horizontal_cell_count"],
            params["vertical_cell_count"],
            params["vertex_elements"],
            params["center_elements"]
        )


# Create a dictionary of component instances
components = {}
for key, value in params["element_defs"].items():
    components[key] = create_component(value)

# Create the SVG drawing
canvas_width, canvas_height = parse_canvas_size(params["canvas_size"])
dwg = svgwrite.Drawing("output.svg", size=(canvas_width, canvas_height))

# Draw the requested components
for component_id in params["component_to_draw"]:
    component = components[component_id]
    center = (canvas_width / 2, canvas_height / 2)
    size = random_choice(component.style["size_options"])
    rotation = random_choice(component.style["rotation_options"])
    element = component.draw(dwg, center, size, rotation)
    dwg.add(element)

# Save the SVG file
dwg.save()
