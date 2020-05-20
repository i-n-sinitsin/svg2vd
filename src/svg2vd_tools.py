from src import svg2vd_types as types


def remove_link_from_string(str):
    strs = str.split("}")
    return strs[-1]


def get_url(full_str: str):
    # "url(#testlink)" -> "#testlink"
    url = full_str[4:-1]
    return url


def split_by_commands(string_to_parse: str):
    commands = ["M", "m", "Z", "z", "H", "h", "V", "v", "L", "l", "A", "a", "T", "t", "Q", "q", "S", "s", "C", "c"]
    output = []
    current_command = []
    current_str = ""
    for char in string_to_parse:
        if char in commands:
            if len(current_str) > 0:
                current_command.append(current_str.strip(" ").split(" "))
                output.append(current_command.copy())
                current_command.clear()
                current_command.append(char.strip(" "))
                current_str = ""
            else:
                current_command.clear()
                current_command.append(char)
                current_str = ""
        else:
            current_str = current_str + char

    current_command.append(current_str.strip(" ").split(" "))
    output.append(current_command)

    return output


def join_command_m(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        current_parameter = current_parameter + 2
    return result


def join_command_h(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + " "
        current_parameter = current_parameter + 1
    return result


def join_command_v(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + " "
        current_parameter = current_parameter + 1
    return result


def join_command_l(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        current_parameter = current_parameter + 2
    return result


def join_command_a(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        result = result + parameters[current_parameter + 2] + " "
        result = result + parameters[current_parameter + 3] + "," + parameters[current_parameter + 4] + " "
        result = result + parameters[current_parameter + 5] + "," + parameters[current_parameter + 6] + " "
        current_parameter = current_parameter + 7
    return result


def join_command_t(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        current_parameter = current_parameter + 2
    return result


def join_command_q(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        result = result + parameters[current_parameter + 2] + "," + parameters[current_parameter + 3] + " "
        current_parameter = current_parameter + 4
    return result


def join_command_s(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        result = result + parameters[current_parameter + 2] + "," + parameters[current_parameter + 3] + " "
        current_parameter = current_parameter + 4
    return result


def join_command_c(parameters: list):
    result = ""
    current_parameter = 0
    while current_parameter < len(parameters):
        result = result + parameters[current_parameter] + "," + parameters[current_parameter + 1] + " "
        result = result + parameters[current_parameter + 2] + "," + parameters[current_parameter + 3] + " "
        result = result + parameters[current_parameter + 4] + "," + parameters[current_parameter + 5] + " "
        current_parameter = current_parameter + 6
    return result


def join_d_parameter(commands: list):
    result = ""

    for cmd in commands:
        result = result + cmd[0] + " "
        if str(cmd[0]).lower() == "m":
            result = result + join_command_m(cmd[1])
        elif str(cmd[0]).lower() == "v":
            result = result + join_command_v(cmd[1])
        elif str(cmd[0]).lower() == "h":
            result = result + join_command_h(cmd[1])
        elif str(cmd[0]).lower() == "l":
            result = result + join_command_l(cmd[1])
        elif str(cmd[0]).lower() == "a":
            result = result + join_command_a(cmd[1])
        elif str(cmd[0]).lower() == "t":
            result = result + join_command_t(cmd[1])
        elif str(cmd[0]).lower() == "q":
            result = result + join_command_q(cmd[1])
        elif str(cmd[0]).lower() == "s":
            result = result + join_command_s(cmd[1])
        elif str(cmd[0]).lower() == "c":
            result = result + join_command_c(cmd[1])
        elif str(cmd[0]).lower() == "z":
            result = result + " "
    return result


def split_d_parameter(string_to_parse: str):
    # replace all separators to space
    for char in ["\t", "\n", "\f", "\r", ","]:
        string_to_parse = string_to_parse.replace(char, " ")
    string_to_parse = string_to_parse.strip(" ")
    # divide into commands
    commands = split_by_commands(string_to_parse)

    return commands


def mult_matrix(m1: types.Matrix, m2: types.Matrix):
    result = types.Matrix()
    result.a = m1.a * m2.a + m1.c * m2.b
    result.b = m1.b * m2.a + m1.d * m2.b
    result.c = m1.a * m2.c + m1.c * m2.d
    result.d = m1.b * m2.c + m1.d * m2.d
    result.e = m1.a * m2.e + m1.c * m2.f + m1.e
    result.f = m1.b * m2.e + m1.d * m2.f + m1.f
    return result


def calculate_new_coords(m: types.Matrix, x_old: str, y_old: str):
    x_new = m.a * float(x_old) + m.c * float(y_old) + m.e
    y_new = m.b * float(x_old) + m.d * float(y_old) + m.f
    return str(x_new), str(y_new)


def apply_matrix_command_m(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[
            current_parameter], parameters[current_parameter + 1])
        current_parameter = current_parameter + 2


def apply_matrix_command_l(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[current_parameter], parameters[current_parameter + 1])
        current_parameter = current_parameter + 2


def apply_matrix_command_a(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[
            current_parameter], parameters[current_parameter + 1])
        [parameters[current_parameter + 3], parameters[current_parameter + 4]] = calculate_new_coords(m, parameters[
            current_parameter + 3], parameters[current_parameter + 4])
        [parameters[current_parameter + 5], parameters[current_parameter + 6]] = calculate_new_coords(m, parameters[
            current_parameter + 5], parameters[current_parameter + 6])
        current_parameter = current_parameter + 7

def apply_matrix_command_t(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[current_parameter], parameters[current_parameter + 1])
        current_parameter = current_parameter + 2


def apply_matrix_command_q(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[current_parameter], parameters[current_parameter + 1])
        current_parameter = current_parameter + 2


def apply_matrix_command_s(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[current_parameter], parameters[current_parameter + 1])
        current_parameter = current_parameter + 2


def apply_matrix_command_c(m: types.Matrix, parameters: list):
    current_parameter = 0
    while current_parameter < len(parameters):
        [parameters[current_parameter], parameters[current_parameter + 1]] = calculate_new_coords(m, parameters[current_parameter], parameters[current_parameter + 1])
        current_parameter = current_parameter + 2


def apply_matrix_to_commands(matrix: types.Matrix, commands: list):
    result = ""

    for cmd in commands:
        result = result + cmd[0] + " "
        if str(cmd[0]).lower() == "m":
            apply_matrix_command_m(matrix, cmd[1])
        # elif str(cmd[0]).lower() == "v":
        #    apply_matrix_command_v(matrix, cmd[1])
        # elif str(cmd[0]).lower() == "h":
        #    apply_matrix_command_h(matrix, cmd[1])
        elif str(cmd[0]).lower() == "l":
            apply_matrix_command_l(matrix, cmd[1])
        elif str(cmd[0]).lower() == "a":
            apply_matrix_command_a(matrix, cmd[1])
        elif str(cmd[0]).lower() == "t":
            apply_matrix_command_t(matrix, cmd[1])
        elif str(cmd[0]).lower() == "q":
            apply_matrix_command_q(matrix, cmd[1])
        elif str(cmd[0]).lower() == "s":
            apply_matrix_command_s(matrix, cmd[1])
        elif str(cmd[0]).lower() == "c":
            apply_matrix_command_c(matrix, cmd[1])
    return result


def modify_vh_to_l(commands: list):
    for cmd in commands:
        if cmd[0] == "V":
            cmd[0] = "L"
            new_values = []
            for value in cmd[1]:
                new_values.append(0)
                new_values.append(value)
            cmd[1] = new_values
        elif cmd[0] == "v":
            cmd[0] = "l"
            new_values = []
            for value in cmd[1]:
                new_values.append(0)
                new_values.append(value)
            cmd[1] = new_values
        elif cmd[0] == "H":
            cmd[0] = "L"
            new_values = []
            for value in cmd[1]:
                new_values.append(value)
                new_values.append(0)
            cmd[1] = new_values
        elif cmd[0] == "h":
            cmd[0] = "l"
            new_values = []
            for value in cmd[1]:
                new_values.append(value)
                new_values.append(0)
            cmd[1] = new_values


def apply_matrix_transformation(matrix: types.Matrix, input_data: str):
    commands = split_d_parameter(input_data)
    modify_vh_to_l(commands)
    apply_matrix_to_commands(matrix, commands)
    result = join_d_parameter(commands)
    return result
