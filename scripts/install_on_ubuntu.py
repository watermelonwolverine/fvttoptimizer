#!/usr/bin/env python3
import json
import os
import shutil
import sys
from os import path

sys.path.append("src")

from fvttoptimizer_wrapper.__constants import app_name, path_to_config_file_linux
from fvttoptimizer.__constants import absolute_path_to_foundry_data_key

path_to_executable_file = "/usr/bin/{0}".format(app_name)


def install():
    print("Installing {0}".format(app_name))

    if not os.path.exists("dist/{0}".format(app_name)):
        raise Exception("No fvttoptimizer found under dist/. Did you successfully build the project?")

    path_to_foundry_data = input("Enter path to the 'Data' folder of your foundry data (for example "
                                 "/home/user/foundrydata/Data): ")

    if not path_to_foundry_data.endswith("Data"):

        should_continue_str = input("The entered path does end with Data. Make sure you entered the right one. "
                                    "Do you want to continue (y,n): ")

        if not should_continue_str.lower() == "y":
            print("Cancelling installation...")
            exit()

    if not path.exists(path_to_foundry_data):

        should_continue_str = input("The entered path does not exist. "
                                    "Do you want to continue (y,n): ")

        if not should_continue_str.lower() == "y":
            print("Cancelling installation...")
            exit()

    config_dict = \
        {
            absolute_path_to_foundry_data_key:
                path.abspath(path_to_foundry_data)
        }

    try:

        with open(path_to_config_file_linux, "w+", encoding="utf-8") as config_fout:
            json.dump(config_dict, config_fout)
            print("Created config file {0}".format(path_to_config_file_linux))
    except BaseException as error:
        print(error)
        print("Unable to write config file to {0}. Cancelling installation...".format(path_to_config_file_linux))
        exit()

    try:

        shutil.copy("dist/{0}".format(app_name),
                    path_to_executable_file)

    except BaseException as error:
        print(error)
        print("Unable to copy {0} to /usr/bin/. "
              "Try running installer with sudo. "
              "Cancelling installation...".format(app_name))
        os.remove(path_to_config_file_linux)
        exit()

    try:
        os.chmod(path_to_executable_file, 0o555)
    except BaseException as error:
        print(error)
        print("Unable to make {0} executable. "
              "Try running installer with sudo. "
              "Cancelling installation...".format(path_to_executable_file))
        os.remove(path_to_config_file_linux)
        os.remove(path_to_executable_file)
        exit()

    print("Successfully installed {0}".format(app_name))


if __name__ == "__main__":
    install()
