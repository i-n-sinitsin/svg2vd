class SVGData:
    viewport_width: str
    viewport_height: str
    width: str
    height: str

    def __init__(self):
        self.width = ""
        self.height = ""
        self.viewport_width = ""
        self.viewport_height = ""

    def __init__(self, width, height, viewport_width, viewport_height):
        self.width = width
        self.height = height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height


class StyleData:
    fill: str
    fill_opacity: str
    stroke: str
    stroke_opacity: str
    stroke_width: str
    stop_color: str
    stop_opacity: str
    fill_type: str
    stroke_dasharray: str
    stroke_linecap: str
    stroke_linejoin: str
    opacity: str

    def __init__(self):
        self.fill = ""
        self.fill_opacity = ""
        self.stroke = ""
        self.stroke_opacity = ""
        self.stroke_width = ""
        self.stop_color = ""
        self.stop_opacity = ""
        self.fill_type = "nonZero"
        self.stroke_dasharray = ""
        self.stroke_linecap = ""
        self.stroke_linejoin = ""

    def read_from_string(self, input_string: str):
        styles_list = input_string.split(";")
        styles = {}
        for style in styles_list:
            params = style.split(":")
            if len(params) > 1:
                styles[params[0]] = params[1]

        if "fill" in styles:
            self.fill = styles["fill"]
        if "fill-opacity" in styles:
            self.fill_opacity = styles["fill-opacity"]
        if "stroke" in styles:
            self.stroke = styles["stroke"]
        if "stroke-opacity" in styles:
            self.stroke_opacity = styles["stroke-opacity"]
        if "stroke-width" in styles:
            self.stroke_width = styles["stroke-width"]
        if "stop-color" in styles:
            self.stop_color = styles["stop-color"]
        if "stop-opacity" in styles:
            self.stop_opacity = styles["stop-opacity"]
        if "fill-rule" in styles:
            if styles["fill-rule"].lower() == "evenodd":
                self.fill_type = "evenOdd"
            elif styles["fill-rule"].lower() == "nonzero":
                self.fill_type = "nonZero"

        # todo:
        # stroke-linecap
        # stroke-linejoin


class LinearGradientStopData:
    style: StyleData
    offset: str

    def __init__(self):
        self.style = StyleData()
        self.offset = ""


class LinearGradientData:
    x1: str
    y1: str
    x2: str
    y2: str
    ref: str
    stops = {}

    def __init__(self):
        self.x1 = ""
        self.y1 = ""
        self.x2 = ""
        self.y2 = ""
        self.ref = ""
        self.stops = {}


class DefsData:
    linear_gradients = {}

    def __init__(self):
        self.linear_gradients = {}


class Matrix:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float

    def __init__(self):
        self.a = 1
        self.b = 0
        self.c = 0
        self.d = 1
        self.e = 0
        self.f = 0


class TransformData:
    matrix: Matrix
    rotation: str
    pivotX: str
    pivotY: str
    scaleX: str
    scaleY: str
    translateX: str
    translateY: str

    def __init__(self):
        self.matrix = Matrix()
        self.rotation = ""
        self.pivotX = ""
        self.pivotY = ""
        self.scaleX = ""
        self.scaleY = ""
        self.translateX = ""
        self.translateY = ""

    def empty(self):
        if self.rotation + self.pivotX + self.pivotY + self.scaleX + self.scaleY + self.translateX \
                + self.translateY == "":
            return True
        else:
            return False


class PathData:
    id: str
    d: str
    style: StyleData
    transform: TransformData

    def __init__(self):
        self.id = ""
        self.d = ""
        self.style = StyleData()
        self.transform = TransformData()


class RectData:
    id: str
    rx: str
    ry: str
    x: str
    y: str
    width: str
    height: str
    style: StyleData
    transform: TransformData

    def __init__(self):
        self.id = ""
        self.rx = "0"
        self.ry = "0"
        self.x = "0"
        self.y = "0"
        self.width = "0"
        self.height = "0"
        self.style = StyleData()
        self.transform = TransformData()


class EllipseData:
    id: str
    rx: str
    ry: str
    cx: str
    cy: str
    style: StyleData
    transform: TransformData

    def __init__(self):
        self.id = ""
        self.rx = "0"
        self.ry = "0"
        self.cx = "0"
        self.cy = "0"
        self.style = StyleData()
        self.transform = TransformData()


class CircleData:
    id: str
    r: str
    cx: str
    cy: str
    style: StyleData
    transform: TransformData

    def __init__(self):
        self.id = ""
        self.r = "0"
        self.cx = "0"
        self.cy = "0"
        self.style = StyleData()
        self.transform = TransformData()


class LineData:
    id: str
    x1: str
    y1: str
    x2: str
    y2: str
    style: StyleData
    transform: TransformData

    def __init__(self):
        self.id = ""
        self.x1 = "0"
        self.y1 = "0"
        self.x2 = "0"
        self.y2 = "0"
        self.style = StyleData()
        self.transform = TransformData()


class PolyLineData:
    id: str
    points: []
    style: StyleData
    transform: TransformData

    def __init__(self):
        self.id = ""
        self.points = []
        self.style = StyleData()
        self.transform = TransformData()


class GroupData:
    id: str
    transform: TransformData
    items = []

    def __init__(self):
        self.id = ""
        self.items = []
        self.transform = TransformData()

    def append(self, item):
        self.items.append(item)


class Data:
    svg_data: SVGData
    defs_data: DefsData
    groups_data = []

    def __init__(self):
        self.svg_data = SVGData("", "", "", "")
        self.defs_data = DefsData()
        self.groups_data = []
