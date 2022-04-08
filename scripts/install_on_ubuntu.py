#!/usr/bin/env python3
import json
import os
import shutil
import sys
import zipapp
from os import path

import main

sys.path.append("src")

from fvttoptimizer import config
from main import app_name, path_to_config_file_linux

path_to_executable_file = "/usr/bin/{0}".format(app_name)


def prepare_archive():
    if path.exists("temp"):
        print("temp folder already exists. Please delete it execute the installation somewhere else.")

    os.mkdir("temp")

    shutil.copy("src/main.py",
                "temp/")

    shutil.copy("src/version_checker.py",
                "temp/")

    shutil.copy("src/help_text.py",
                "temp/")

    shutil.copytree("src/{0}".format(main.app_name),
                    "temp/{0}".format(main.app_name))

    zipapp.create_archive("temp",
                          "{0}.pyz".format(app_name),
                          main="main:main",
                          interpreter="python3")

    shutil.rmtree("temp")


def create_executable_file():
    prepare_archive()

    with open(path_to_executable_file,
              "wb") as appf:
        appf.write(bytes("#!/usr/bin/env python3\n", "utf-8"))

        with open("{0}.pyz".format(app_name),
                  'rb') as zipf:
            shutil.copyfileobj(zipf, appf)

    os.remove("{0}.pyz".format(app_name))


def install():
    print("Installing {0}".format(app_name))

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
            config.absolute_path_to_foundry_data_key:
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

        create_executable_file()

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
