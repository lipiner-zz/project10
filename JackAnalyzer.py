###########
# imports #
###########
import sys
import os

from CompilationEngine import CompilationEngine

#############
# constants #
#############
PATH_POS = 1  # the arguments position for the file path
VM_SUFFIX = ".vm"
JACK_SUFFIX = ".jack"
WRITING_MODE = "w"
FILE_NAME_POSITION = -1


def translate_file(input_file, output_file):
    """
    Translates the given input jack file to the given output vm file
    :param input_file: the input jack file
    :param output_file: the output vm file
    """
    compilation_engine = CompilationEngine(input_file, output_file)
    compilation_engine.compile()


def translate_single_file(file_name):
    """
    The function gets a JACK file and translates it to vm code. It creates an vm file with the same
    name in the same directory that contains the jack code.
    :param file_name: the name of the jack file to be translated
    """
    # opening the vm file
    with open(file_name) as input_file:
        # figuring the output file name- replacing vm suffix to asm
        output_file_name = file_name.replace(JACK_SUFFIX, VM_SUFFIX)
        # opening the output file in writing mode
        with open(output_file_name, WRITING_MODE) as output_file:
            # translating the file
            translate_file(input_file, output_file)


def translate_directory(directory_full_path):
    """
    The function gets a directory name and translates each jack file in it to a vm file with the name of the.
    :param directory_full_path: the name of the given directory
    """
    files_list = os.listdir(directory_full_path)  # list of all the files' name in the given directory
    for directory_file in files_list:
        if JACK_SUFFIX == directory_file[-len(JACK_SUFFIX):]:  # if the file is a jack file
            jack_file = os.path.join(directory_full_path, directory_file)  # creates a full path of the jack file
            output_file_name = os.path.join(directory_full_path, directory_file[:-len(JACK_SUFFIX)] + VM_SUFFIX)
            with open(jack_file) as input_file:
                with open(output_file_name, WRITING_MODE) as output_file:
                    translate_file(input_file, output_file)

# main part
if __name__ == '__main__':
    if len(sys.argv) < PATH_POS + 1:
        sys.exit()  # There is not an input

    # checks if the given path is a directory or a file
    path = sys.argv[PATH_POS]
    if os.path.isdir(path):
        translate_directory(path)  # translates all vm files in the directory
    else:
        translate_single_file(path)  # translates the given vm file
