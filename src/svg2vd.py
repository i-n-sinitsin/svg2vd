from src import svg2vd_reader as RD, svg2vd_writer as WR


def do_work(filename: str):
    input_name = filename + ".svg"
    reader = RD.Reader()
    data = reader.read(input_name)
    output_name = filename + ".xml"
    writer = WR.Writer(data)
    writer.write(output_name)


# do tests
do_work("svg/test_elipse")
do_work("svg/test_pencils")
do_work("svg/test_pero")
do_work("svg/test_rects")
do_work("svg/test_rubber")
do_work("svg/test_spirals")
do_work("svg/test_sprey")
do_work("svg/test_stars_and_polygons")
do_work("svg/test_transforms")
do_work("svg/ttt")
do_work("svg/chip_dail")
do_work("svg/arbelos")
do_work("svg/jerry")
do_work("svg/mickey")
do_work("svg/TUX-G2-SVG")
