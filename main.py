###########
# imports #
###########
import sys
import os

from JackTokenizer import JackTokenizer

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
    translates the given input vm file to the given output asm file
    :param input_file: the input vm file
    :param output_file: the output asm file
    """
    jack_tokenizer = JackTokenizer(input_file)
    while jack_tokenizer.has_more_tokens():
        jack_tokenizer.advance()
        print(jack_tokenizer.get_token_string())


def translate_single_file(file_name):
    """
    The function gets a file name from vm type and translates it to asm code. It creates an asm file with he same
    name in the same directory that contains the asm code.
    :param file_name: the name of the vm file to be translated
    """
    # opening the vm file
    with open(file_name) as input_file:
        # figuring the output file name- replacing vm suffix to asm
        output_file_name = file_name.replace(JACK_SUFFIX, VM_SUFFIX)
        # opening the output file in writing mode
        with open(output_file_name, WRITING_MODE) as output_file:
            # translating the file
            translate_file(input_file, output_file)


# def translate_directory(directory_full_path):
#     """
#     The function gets a directory name and translates all the vm files in it to one asm file with the name of the
#     given directory.
#     :param directory_full_path: the name of the given directory
#     """
#     files_list = os.listdir(directory_full_path)  # list of all the files' name in the given directory
#     directory_full_dirs = directory_full_path.split(os.path.sep)  # split the path to its directories and the file name
#     directory_name = directory_full_dirs[FILE_NAME_POSITION]  # gets the file name only
#     output_file_name = os.path.join(directory_full_path, directory_name + "." + VM_SUFFIX)
#     with open(output_file_name, WRITING_MODE) as output_file:
#         file_counter = 0  # counts how many files have been translated in the directory
#         for directory_file in files_list:
#             if JACK_SUFFIX == directory_file[-len(JACK_SUFFIX):]:  # if the file is a vm file
#                 file_counter += 1
#                 vm_file_name = os.path.join(directory_full_path, directory_file)  # creates a full path of the file name
#                 with open(vm_file_name) as input_file:
#                     translate_file(input_file, vm_file_name, output_file, file_counter == 1)

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
