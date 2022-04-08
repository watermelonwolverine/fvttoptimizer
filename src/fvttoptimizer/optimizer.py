import os

from fvttmv.path_tools import PathTools
from fvttmv.update.references_updater import ReferencesUpdater

from fvttoptimizer.config import RunConfig
from fvttoptimizer.directory_optimizer import DirectoryOptimizer
from fvttoptimizer.exception import FvttOptimizerException
from fvttoptimizer.file_optimizer import FileOptimizer

taboo_dirs = ["worlds", "modules", "systems"]


class Optimizer:
    __run_config: RunConfig
    __path_tools: PathTools
    __file_optimizer: FileOptimizer
    __directory_optimizer: DirectoryOptimizer

    def __init__(self,
                 run_config: RunConfig,
                 references_updater: ReferencesUpdater):
        self.__run_config = run_config
        self.__path_tools = PathTools(run_config.get_abs_path_to_foundry_data())

        self.__file_optimizer = FileOptimizer(run_config,
                                              self.__path_tools,
                                              references_updater)
        self.__directory_optimizer = DirectoryOptimizer(run_config,
                                                        self.__path_tools,
                                                        self.__file_optimizer)

    def optimize(self,
                 abs_path: str):
        self.__assert_path_is_ok(abs_path)

        if os.path.isdir(abs_path):
            self.__directory_optimizer.optimize(abs_path)
        elif os.path.isfile(abs_path):
            self.__file_optimizer.maybe_optimize(abs_path)

    def __assert_path_is_ok(self,
                            path: str):
        if not self.__path_tools.is_in_foundry_data(path):
            raise FvttOptimizerException("{0} is not in the configured foundry Data folder.".format(path))
        if not os.path.exists(path):
            raise FvttOptimizerException("{0} does not exist.".format(path))
        if not os.path.isdir(path) and not os.path.isfile(path):
            raise FvttOptimizerException("{0} is neither a file nor a folder.".format(path))

        for taboo_dir in taboo_dirs:

            abs_path_to_taboo_dir = os.path.join(self.__run_config.get_abs_path_to_foundry_data(), taboo_dir)

            if self.__path_tools.is_parent_dir(path, abs_path_to_taboo_dir) and self.__run_config.recursive:
                raise FvttOptimizerException("Going into {0} is not allowed.".format(taboo_dir))
            if self.__path_tools.is_parent_dir(abs_path_to_taboo_dir, path):
                raise FvttOptimizerException("Going into {0} is not allowed.".format(taboo_dir))
