program_file = "program"
file_extension_separator = "."
extension = "txt"

if __name__ == "__main__":
    full_file = "{}{}".format("{}".format("{"), "{}".format("}")).format("{}{}".format(program_file, "{}{}".format(file_extension_separator, extension)))
    with open(full_file, "r") as file:
        exec("prog = \"{}\"".format(file.read()))
        exec("exec(prog)")