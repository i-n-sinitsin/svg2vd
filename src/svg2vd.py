from src import svg2vd_reader as RD, svg2vd_writer as WR


def do_work(filename: str):
    input_name = filename + ".svg"
    reader = RD.Reader()
    data = reader.read(input_name)
    output_name = filename + ".xml"
    writer = WR.Writer(data)
    writer.write(output_name)


# do tests
do_work("test_elipse")
do_work("test_pencils")
do_work("test_pero")
do_work("test_rects")
do_work("test_rubber")
do_work("test_spirals")
do_work("test_sprey")
do_work("test_stars_and_polygons")
do_work("test_transforms")
do_work("ttt")
do_work("chip_dail")
do_work("arbelos")
do_work("jerry")
do_work("mickey")
do_work("TUX-G2-SVG")
