import json
import logging
import os

from fvttmv.path_tools import PathTools

from fvttoptimizer import __constants
from fvttoptimizer.exception import FvttOptimizerException

absolute_path_to_foundry_data_key = __constants.absolute_path_to_foundry_data_key


class ProgramConfig:
    def get_abs_path_to_foundry_data(self) -> str:
        raise NotImplementedError("Not implemented")


class ProgramConfigImpl(ProgramConfig):
    __abs_path_to_foundry_data: str

    def __init__(self,
                 abs_path_to_foundry_data: str):
        self.__abs_path_to_foundry_data = abs_path_to_foundry_data
        ProgramConfigChecker.check_config(self)

    def get_abs_path_to_foundry_data(self):
        return self.__abs_path_to_foundry_data

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class RunConfig(ProgramConfig):
    __program_config: ProgramConfig
    # the quality setting for the webp conversion
    quality: int = 75
    # if the the program should go into sub folders
    recursive: bool = False
    # how much smaller the new file has to be than the old one in percent
    override_percent: int = 25
    # if webp files should be skipped
    skip_webp: bool = False
    # Skip files of which a webp exists
    # For example file1.png would be skipped if a file.webp exists in the same directory
    skip_existing: bool = False

    def __init__(self,
                 program_config: ProgramConfig):
        self.__program_config = program_config

    def get_abs_path_to_foundry_data(self) -> str:
        return self.__program_config.get_abs_path_to_foundry_data()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class ConfigFileReader:

    @staticmethod
    def read_config_file(
            path_to_config_file) -> ProgramConfig:

        logging.debug("Reading config from: %s", path_to_config_file)

        if not os.path.exists(path_to_config_file):
            raise FvttOptimizerException("Missing config file. Could not find {0}".format(path_to_config_file))

        # noinspection PyBroadException
        try:
            with open(path_to_config_file, encoding="utf-8") as config_file:
                config_dict = json.load(config_file)
        except BaseException as ex:
            raise FvttOptimizerException("Exception while reading config file: " + str(ex))

        result = ProgramConfigImpl(config_dict[absolute_path_to_foundry_data_key])

        return result


class ProgramConfigChecker:

    @staticmethod
    def check_config(program_config: ProgramConfig):
        abs_path_to_foundry_data = program_config.get_abs_path_to_foundry_data()

        if not os.path.isabs(abs_path_to_foundry_data) \
                or not PathTools.is_normalized_path(abs_path_to_foundry_data) \
                or not os.path.isdir(abs_path_to_foundry_data):
            raise FvttOptimizerException("Absolute path to foundrydata is not configured correctly.")
