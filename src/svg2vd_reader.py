import xml.etree.ElementTree as ET
from src import svg2vd_tools as tools, svg2vd_types as types


class Reader:
    data: types.Data

    def __init__(self):
        self.data = types.Data()

    def read(self, filename: str):
        tree = ET.parse(filename)
        root = tree.getroot()
        # collect root elemnt if it is equal to svg
        root_name = tools.remove_link_from_string(root.tag)
        if root_name == "svg":
            self.collect_svg(root)
        else:
            print(f"root with name={root_name} not supported. Must be svg")

        return self.data

    def collect_svg(self, element: ET.Element):
        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "viewBox":
                values = attrib_value.split(" ")
                self.data.svg_data = types.SVGData(values[2], values[3], values[2], values[3])
            elif attrib_name == "height":
                self.data.svg_data.height = attrib_value
                self.data.svg_data.viewport_height = attrib_value
            elif attrib_name == "width":
                self.data.svg_data.width = attrib_value
                self.data.svg_data.viewport_width = attrib_value
            elif attrib_name in ("id", "version"):
                # not used in convert
                pass
            else:
                print(f"collect_svg: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            if child_name == "defs":
                self.collect_defs(child)
            elif child_name == "g":
                self.data.groups_data.append(self.collect_group(child))
            elif child_name == "path":
                self.data.groups_data.append(self.collect_path(child))
            elif child_name == "rect":
                self.data.groups_data.append(self.collect_rect(child))
            elif child_name == "ellipse":
                self.data.groups_data.append(self.collect_ellipse(child))
            elif child_name == "circle":
                self.data.groups_data.append(self.collect_circle(child))
            elif child_name == "line":
                self.data.groups_data.append(self.collect_line(child))
            elif child_name == "polyline":
                self.data.groups_data.append(self.collect_polyline(child))
            elif child_name in ("use"):
                print(f"Need realization child -> {child_name}")
                pass
            elif child_name in ("metadata"):
                # not used in convert
                pass
            else:
                print(f"collect_svg: child with name={child_name} not supported")

    def collect_defs(self, element: ET.Element):
        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name in ("id"):
                # not used in convert
                pass
            else:
                print(f"collect_defs: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            if child_name == "linearGradient":
                self.collect_linear_gradient(child)
            elif child_name in ("radialGradient", "meshgradient"):
                print(f"Need realization child -> {child_name}")
                pass
            else:
                print(f"collect_defs: child with name={child_name} not supported")

    def collect_linear_gradient(self, element: ET.Element):
        # read attrib

        if "id" in element.attrib:
            saved_id = element.attrib["id"]
        else:
            saved_id = "stop_" + str(len(self.data.defs_data.linear_gradients))

        self.data.defs_data.linear_gradients[saved_id] = types.LinearGradientData()

        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                # nothing to do
                pass
            elif attrib_name == "x1":
                self.data.defs_data.linear_gradients[saved_id].x1 = attrib_value
            elif attrib_name == "y1":
                self.data.defs_data.linear_gradients[saved_id].y1 = attrib_value
            elif attrib_name == "x2":
                self.data.defs_data.linear_gradients[saved_id].x2 = attrib_value
            elif attrib_name == "y2":
                self.data.defs_data.linear_gradients[saved_id].y2 = attrib_value
            elif attrib_name == "href":
                self.data.defs_data.linear_gradients[saved_id].ref = attrib_value
            elif attrib_name in ("gradientUnits"):
                # not used in convert
                pass
            else:
                print(f"collect_linear_gradient: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            if child_name == "stop":
                self.collect_linear_gradient_stop(child, saved_id)
            else:
                print(f"collect_linear_gradient: child with name={child_name} not supported")

    def collect_linear_gradient_stop(self, element: ET.Element, gradient_id: str):
        # read attrib

        if "id" in element.attrib:
            saved_id = element.attrib["id"]
        else:
            saved_id = "stop_" + str(len(self.data.defs_data.linear_gradients[gradient_id].stops))

        self.data.defs_data.linear_gradients[gradient_id].stops[saved_id] = types.LinearGradientStopData()

        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                # nothing to do
                pass
            elif attrib_name in types.StyleData().supportedAttrib:
                self.data.defs_data.linear_gradients[gradient_id].stops[saved_id].style.set_value(attrib_name, attrib_value)
            elif attrib_name == "offset":
                self.data.defs_data.linear_gradients[gradient_id].stops[saved_id].offset = attrib_value
            else:
                print(f"collect_linear_gradient_stop: attribute {attrib_name} not supported value={attrib_value}")

    def read_transform(self, transform_str: str):
        transform_data = types.TransformData()
        # description name(params)
        param_name = transform_str.split("(")[0]
        param_value = transform_str.split("(")[1].split(")")[0]

        values = param_value.split(",")
        if param_name == "scale":
            transform_data.scaleX = values[0]
            if len(values) == 2:
                transform_data.scaleY = values[1]
            else:
                transform_data.scaleY = transform_data.scaleX
        elif param_name == "translate":
            transform_data.translateX = values[0]
            if len(values) == 2:
                transform_data.translateY = values[1]
            pass
        elif param_name == "rotate":
            transform_data.rotation = values[0]
            if len(values) == 3:
                transform_data.pivotX = values[1]
                transform_data.pivotY = values[2]
            pass
        elif param_name == "matrix":
            transform_data.matrix.a = float(values[0])
            transform_data.matrix.b = float(values[1])
            transform_data.matrix.c = float(values[2])
            transform_data.matrix.d = float(values[3])
            transform_data.matrix.e = float(values[4])
            transform_data.matrix.f = float(values[5])
            pass
        else:
            print(f"transform -> {param_name} not supported")

        return transform_data

    def collect_group(self, element: ET.Element):

        group = types.GroupData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                group.id = attrib_value
            elif attrib_name == "transform":
                group.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_group: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            if child_name == "g":
                group.append(self.collect_group(child))
            elif child_name == "path":
                group.append(self.collect_path(child))
            elif child_name == "rect":
                group.append(self.collect_rect(child))
            elif child_name == "ellipse":
                group.append(self.collect_ellipse(child))
            elif child_name == "circle":
                group.append(self.collect_circle(child))
            elif child_name == "line":
                group.append(self.collect_line(child))
            elif child_name == "polyline":
                group.append(self.collect_polyline(child))
            elif child_name in ("use"):
                print(f"Need realization child -> {child_name}")
                pass
            else:
                print(f"collect_group: child with name={child_name} not supported")

        return group

    def collect_path(self, element: ET.Element):

        path = types.PathData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                path.id = attrib_value
            elif attrib_name == "d":
                path.d = attrib_value
            elif attrib_name in types.StyleData().supportedAttrib:
                path.style.set_value(attrib_name, attrib_value)
            elif attrib_name == "transform":
                path.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_path: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            print(f"collect_path: child with name={child_name} not supported")

        return path

    def collect_rect(self, element: ET.Element):

        rect = types.RectData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                rect.id = attrib_value
            elif attrib_name == "rx":
                rect.rx = attrib_value
            elif attrib_name == "ry":
                rect.ry = attrib_value
            elif attrib_name == "x":
                rect.x = attrib_value
            elif attrib_name == "y":
                rect.y = attrib_value
            elif attrib_name == "width":
                rect.width = attrib_value
            elif attrib_name == "height":
                rect.height = attrib_value
            elif attrib_name in types.StyleData().supportedAttrib:
                rect.style.set_value(attrib_name, attrib_value)
            elif attrib_name == "transform":
                rect.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_rect: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            print(f"collect_rect: child with name={child_name} not supported")

        return rect

    def collect_ellipse(self, element: ET.Element):

        ellipse = types.EllipseData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                ellipse.id = attrib_value
            elif attrib_name == "rx":
                ellipse.rx = attrib_value
            elif attrib_name == "ry":
                ellipse.ry = attrib_value
            elif attrib_name == "cx":
                ellipse.cx = attrib_value
            elif attrib_name == "cy":
                ellipse.cy = attrib_value
            elif attrib_name in types.StyleData().supportedAttrib:
                ellipse.style.set_value(attrib_name, attrib_value)
            elif attrib_name == "transform":
                ellipse.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_ellipse: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            print(f"collect_ellipse: child with name={child_name} not supported")

        return ellipse

    def collect_circle(self, element: ET.Element):

        circle = types.CircleData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                circle.id = attrib_value
            elif attrib_name == "r":
                circle.r = attrib_value
            elif attrib_name == "cx":
                circle.cx = attrib_value
            elif attrib_name == "cy":
                circle.cy = attrib_value
            elif attrib_name in types.StyleData().supportedAttrib:
                circle.style.set_value(attrib_name, attrib_value)
            elif attrib_name == "transform":
                circle.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_circle: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            print(f"collect_circle: child with name={child_name} not supported")

        return circle

    def collect_line(self, element: ET.Element):

        line = types.LineData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                line.id = attrib_value
            elif attrib_name == "x1":
                line.x1 = attrib_value
            elif attrib_name == "y1":
                line.y1 = attrib_value
            elif attrib_name == "x2":
                line.x2 = attrib_value
            elif attrib_name == "y2":
                line.y2 = attrib_value
            elif attrib_name in types.StyleData().supportedAttrib:
                line.style.set_value(attrib_name, attrib_value)
            elif attrib_name == "transform":
                line.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_line: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            print(f"collect_line: child with name={child_name} not supported")

        return line

    def collect_polyline(self, element: ET.Element):

        polyline = types.PolyLineData()

        # read attrib
        for attrib_name, attrib_value in element.attrib.items():
            attrib_name = tools.remove_link_from_string(attrib_name)
            if attrib_name == "id":
                polyline.id = attrib_value
            elif attrib_name == "points":
                polyline.points = attrib_value.split(" ")
            elif attrib_name in types.StyleData().supportedAttrib:
                polyline.style.set_value(attrib_name, attrib_value)
            elif attrib_name == "transform":
                polyline.transform = self.read_transform(attrib_value)
            else:
                print(f"collect_polyline: attribute {attrib_name} not supported value={attrib_value}")

        # parse childs
        for child in element:
            child_name = tools.remove_link_from_string(child.tag)
            print(f"collect_polyline: child with name={child_name} not supported")

        return polyline
