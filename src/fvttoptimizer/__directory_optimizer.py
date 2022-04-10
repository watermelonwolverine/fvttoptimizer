import logging
import os

from fvttmv.path_tools import PathTools

from fvttoptimizer.__file_optimizer import FileOptimizer
from fvttoptimizer.config import RunConfig


class DirectoryOptimizer:
    __run_config: RunConfig
    __path_tools: PathTools
    __file_optimizer: FileOptimizer

    def __init__(self,
                 run_config: RunConfig,
                 path_tools: PathTools,
                 file_optimizer: FileOptimizer):
        self.__run_config = run_config
        self.__path_tools = path_tools
        self.__file_optimizer = file_optimizer

    def optimize(self,
                 abs_path_to_dir):

        logging.info("Optimizing directory '%s'" % abs_path_to_dir)

        contents = os.listdir(abs_path_to_dir)

        for element in contents:

            abs_path_to_element = os.path.join(abs_path_to_dir, element)

            if os.path.isfile(abs_path_to_element):
                self.__file_optimizer.maybe_optimize(abs_path_to_element)

            if os.path.isdir(abs_path_to_element) and self.__run_config.recursive:
                self.optimize(abs_path_to_element)
