import xml.etree.ElementTree as ET
import svg2vd_types as types
import svg2vd_tools as tools

class Writer:
    data: types.Data

    def __init__(self, data: types.Data):
        self.data = data

    def write(self, filename: str):
        ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
        ET.register_namespace("aapt", "http://schemas.android.com/aapt")
        root = ET.fromstring("<vector></vector>")

        # fill main data
        root.attrib["xmlns:android"] = "http://schemas.android.com/apk/res/android"
        root.attrib["xmlns:aapt"] = "http://schemas.android.com/aapt"
        root.attrib["android:viewportWidth"] = self.data.svg_data.viewport_width
        root.attrib["android:viewportHeight"] = self.data.svg_data.viewport_height
        root.attrib["android:width"] = self.data.svg_data.width + "dp"
        root.attrib["android:height"] = self.data.svg_data.height + "dp"

        # default
        # root.attrib["android:tint"] = data.svg_data.height + "dp"
        # root.attrib["android:tintMode"] = data.svg_data.height + "dp"
        # root.attrib["android:autoMirrored"] = data.svg_data.height + "dp"
        # root.attrib["android:alpha"] = data.svg_data.height + "dp"

        # fill childs
        for item in self.data.groups_data:
            if type(item) == types.GroupData:
                root.append(self.write_group(self.data.defs_data, item, types.Matrix()))
            elif type(item) == types.PathData:
                root.append(self.write_path(self.data.defs_data, item, types.Matrix()))
            elif type(item) == types.RectData:
                root.append(self.write_rect(self.data.defs_data, item, types.Matrix()))
            elif type(item) == types.EllipseData:
                root.append(self.write_ellipse(self.data.defs_data, item, types.Matrix()))
            elif type(item) == types.CircleData:
                root.append(self.write_circle(self.data.defs_data, item, types.Matrix()))
            elif type(item) == types.LineData:
                root.append(self.write_line(self.data.defs_data, item, types.Matrix()))
            elif type(item) == types.PolyLineData:
                root.append(self.write_polyline(self.data.defs_data, item, types.Matrix()))

        output_tree = ET.ElementTree(root)
        output_tree.write(filename, "utf-8", True, None, "xml")

    def write_group(self, defs_data: types.DefsData, group_data: types.GroupData, parent_matrix: types.Matrix):
        group = ET.fromstring("<group></group>")

        # fill attributes
        group.attrib["android:name"] = group_data.id

        # write transform
        self.write_transform(group_data.transform, group)
        cur_matrix = tools.mult_matrix(parent_matrix, group_data.transform.matrix)
        # fill children
        for item in group_data.items:
            if type(item) == types.GroupData:
                group.append(self.write_group(defs_data, item, cur_matrix))
            elif type(item) == types.PathData:
                group.append(self.write_path(defs_data, item, cur_matrix))
            elif type(item) == types.RectData:
                group.append(self.write_rect(defs_data, item, cur_matrix))
            elif type(item) == types.EllipseData:
                group.append(self.write_ellipse(defs_data, item, cur_matrix))
            elif type(item) == types.CircleData:
                group.append(self.write_circle(defs_data, item, cur_matrix))
            elif type(item) == types.LineData:
                group.append(self.write_line(defs_data, item, cur_matrix))
            elif type(item) == types.PolyLineData:
                group.append(self.write_polyline(defs_data, item, cur_matrix))

        return group

    def write_ellipse(self, defs_data: types.DefsData, ellipse_data: types.EllipseData, parent_matrix: types.Matrix):
        path_data = types.PathData()

        path_data.id = ellipse_data.id
        path_data.style = ellipse_data.style
        path_data.transform = ellipse_data.transform

        # build d parameter
        rx = float(ellipse_data.rx)
        ry = float(ellipse_data.ry)
        cx = float(ellipse_data.cx)
        cy = float(ellipse_data.cy)

        path_data.d = f"M {cx + rx},{cy} " \
                      f"A {rx},{ry} 0 0 1 {cx},{cy + ry} " \
                      f"{rx},{ry} 0 0 1 {cx - rx},{cy} " \
                      f"{rx},{ry} 0 0 1 {cx},{cy - ry} " \
                      f"{rx},{ry} 0 0 1 {cx + rx},{cy} " \
                      f"Z"

        return self.write_path(defs_data, path_data, parent_matrix)

    def write_circle(self, defs_data: types.DefsData, circle_data: types.CircleData, parent_matrix: types.Matrix):
        path_data = types.PathData()

        path_data.id = circle_data.id
        path_data.style = circle_data.style
        path_data.transform = circle_data.transform

        # build d parameter
        r = float(circle_data.r)
        cx = float(circle_data.cx)
        cy = float(circle_data.cy)

        path_data.d = f"M {cx + r},{cy} " \
                      f"A {r},{r} 0 0 1 {cx},{cy + r} " \
                      f"{r},{r} 0 0 1 {cx - r},{cy} " \
                      f"{r},{r} 0 0 1 {cx},{cy - r} " \
                      f"{r},{r} 0 0 1 {cx + r},{cy} " \
                      f"Z"

        return self.write_path(defs_data, path_data, parent_matrix)

    def write_polyline(self, defs_data: types.DefsData, polyline_data: types.PolyLineData, parent_matrix: types.Matrix):
        path_data = types.PathData()

        path_data.id = polyline_data.id
        path_data.style = polyline_data.style
        path_data.transform = polyline_data.transform

        # build d parameter
        for index in range(len(polyline_data.points)):
            if index == 0:
                path_data.d = path_data.d + "M "
            else:
                path_data.d = path_data.d + "L "
            path_data.d = path_data.d + f"{polyline_data.points[index]} "

        path_data.d = path_data.d + " Z"

        return self.write_path(defs_data, path_data, parent_matrix)

    def write_line(self, defs_data: types.DefsData, line_data: types.LineData, parent_matrix: types.Matrix):
        path_data = types.PathData()

        path_data.id = line_data.id
        path_data.style = line_data.style
        path_data.transform = line_data.transform

        # build d parameter
        x1 = float(line_data.x1)
        y1 = float(line_data.y1)
        x2 = float(line_data.x2)
        y2 = float(line_data.y2)

        path_data.d = f"M {x1},{y1} L {x2},{y2} Z"

        return self.write_path(defs_data, path_data, parent_matrix)

    def write_rect(self, defs_data: types.DefsData, rect_data: types.RectData, parent_matrix: types.Matrix):
        path_data = types.PathData()

        path_data.id = rect_data.id
        path_data.style = rect_data.style
        path_data.transform = rect_data.transform

        # build d parameter
        x = float(rect_data.x)
        y = float(rect_data.y)
        w = float(rect_data.width)
        h = float(rect_data.height)
        rx = float(rect_data.rx)
        ry = float(rect_data.ry)

        if rx + ry == 0:
            # simple path
            path_data.d = f"M {x},{y} h {w} v {h} h {-w} Z"
        else:
            if rx == 0:
                rx = ry
            if ry == 0:
                ry = rx

            if 2 * rx > w:
                rx = w / 2.0
            if 2 * ry > h:
                ry = h / 2.0

            path_data.d = f"M {x + rx},{y} " \
                          f"h {w - rx} " \
                          f"c {0},{0} {rx},{0} {rx},{ry} " \
                          f"v {h - 2 * ry} " \
                          f"c {0},{0} {0},{ry} {-rx},{ry} " \
                          f"h {-w + rx} " \
                          f"c {0},{0} {-rx},{0} {-rx},{-ry} " \
                          f"v {-h + 2 * ry} " \
                          f"c {0},{0} {0},{-ry} {rx},{-ry} " \
                          f"z"

        return self.write_path(defs_data, path_data, parent_matrix)

    def write_path(self, defs_data: types.DefsData, path_data: types.PathData, parent_matrix: types.Matrix):
        path = ET.fromstring("<path></path>")

        # fill attributes
        if path_data.id != "":
            path.attrib["android:name"] = path_data.id
        if path_data.d != "":
            # write transform
            cur_matrix = tools.mult_matrix(parent_matrix, path_data.transform.matrix)
            path.attrib["android:pathData"] = tools.apply_matrix_transformation(cur_matrix, path_data.d)
        if path_data.style.stroke_width != "":
            # delete px|mm from end of string
            if path_data.style.stroke_width.endswith("px") or path_data.style.stroke_width.endswith("mm"):
                path.attrib["android:strokeWidth"] = path_data.style.stroke_width[:-2]
            else:
                path.attrib["android:strokeWidth"] = path_data.style.stroke_width

        if not path_data.style.fill.startswith("url"):
            path.attrib["android:fillColor"] = path_data.style.fill
        if path_data.style.fill_opacity != "":
            path.attrib["android:fillAlpha"] = path_data.style.fill_opacity

        if not path_data.style.stroke.startswith("url"):
            path.attrib["android:strokeColor"] = path_data.style.stroke
        if path_data.style.stroke_opacity != "":
            path.attrib["android:strokeAlpha"] = path_data.style.stroke_opacity
        if path_data.style.fill_type != "":
            path.attrib["android:fillType"] = path_data.style.fill_type

        # default
        # path.attrib["android:trimPathStart"] = path_data.d
        # path.attrib["android:trimPathEnd"] = path_data.d
        # path.attrib["android:trimPathOffset"] = path_data.d

        # path.attrib["android:strokeLineCap"] = path_data.d
        # path.attrib["android:strokeLineJoin"] = path_data.d
        # path.attrib["android:strokeMiterLimit"] = path_data.d

        # fill children
        if path_data.style.fill.startswith("url"):
            url = tools.get_url(path_data.style.fill)[1:]
            if url in defs_data.linear_gradients:
                attr = self.write_aapt_attr("android:fillColor")
                attr.append(self.write_linear_gradient(defs_data, url))
                path.append(attr)
            else:
                print(f"Can`t find url -> {url}")

        if path_data.style.stroke.startswith("url"):
            url = tools.get_url(path_data.style.stroke)[1:]
            if url in defs_data.linear_gradients:
                attr = self.write_aapt_attr("android:strokeColor")
                attr.append(self.write_linear_gradient(defs_data, url))
                path.append(attr)
            else:
                print(f"Can`t find url -> {url}")

        if not path_data.transform.empty():
            # fake group for transformation
            fake_group_data = types.GroupData()
            fake_group_data.id = "fg_" + path_data.id
            fake_group_data.transform = path_data.transform
            fake_group = self.write_group(defs_data, fake_group_data, parent_matrix)
            fake_group.append(path)
            return fake_group
        else:
            return path

    def write_clip_path(self, defs_data: types.DefsData, path_data: types.PathData):
        clip_path = ET.fromstring("<clip_path></clip_path>")

        # fill attributes
        # clip_path.attrib["android:name"] = path_data.id
        # clip_path.attrib["android:pathData"] = path_data.d

        # fill children

        return clip_path

    def write_transform(self, transform_data: types.TransformData, element: ET.Element):
        if transform_data.pivotX != "":
            element.attrib["android:pivotX"] = transform_data.pivotX
        if transform_data.pivotY != "":
            element.attrib["android:pivotY"] = transform_data.pivotY
        if transform_data.rotation != "":
            element.attrib["android:rotation"] = transform_data.rotation
        if transform_data.translateX != "":
            element.attrib["android:translateX"] = transform_data.translateX
        if transform_data.translateY != "":
            element.attrib["android:translateY"] = transform_data.translateY
        if transform_data.scaleX != "":
            element.attrib["android:scaleX"] = transform_data.scaleX
        if transform_data.scaleY != "":
            element.attrib["android:scaleY"] = transform_data.scaleY

    def write_aapt_attr(self, attr_name: str):
        aapt_attr = ET.fromstring("<test></test>")
        aapt_attr.tag = "aapt:attr"
        aapt_attr.attrib["name"] = attr_name
        return aapt_attr

    def write_linear_gradient(self, defs_data: types.DefsData, url: str):
        linear_gradient = ET.fromstring("<gradient></gradient>")
        self.write_linear_gradient_from_defs(defs_data, url, linear_gradient)
        return linear_gradient

    def write_linear_gradient_from_defs(self, defs_data: types.DefsData, url: str, linear_gradient: ET.Element):
        if defs_data.linear_gradients[url].x1 != "":
            linear_gradient.attrib["android:startX"] = defs_data.linear_gradients[url].x1
        if defs_data.linear_gradients[url].y1 != "":
            linear_gradient.attrib["android:startY"] = defs_data.linear_gradients[url].y1
        if defs_data.linear_gradients[url].x2 != "":
            linear_gradient.attrib["android:endX"] = defs_data.linear_gradients[url].x2
        if defs_data.linear_gradients[url].y2 != "":
            linear_gradient.attrib["android:endY"] = defs_data.linear_gradients[url].y2
        # linear_gradient.attrib[" android:tileMode"] = clamp

        for stop in defs_data.linear_gradients[url].stops:
            linear_gradient.append(self.write_gradient_item(defs_data.linear_gradients[url].stops[stop]))

        if defs_data.linear_gradients[url].ref != "":
            self.write_linear_gradient_from_defs(defs_data, defs_data.linear_gradients[url].ref[1:], linear_gradient)

    def write_gradient_item(self, stop_data: types.LinearGradientStopData):
        gradient_stop = ET.fromstring("<item></item>")

        alpha_value = ""
        if stop_data.style.stop_opacity != "":
            alpha_value = "%0.2X" % int(float(stop_data.style.stop_opacity) * 255.0)
        if stop_data.style.stop_color != "":
            gradient_stop.attrib["android:color"] = "#" + alpha_value.lower() + stop_data.style.stop_color[1:]
        if stop_data.offset != "":
            gradient_stop.attrib["android:offset"] = stop_data.offset

        return gradient_stop























