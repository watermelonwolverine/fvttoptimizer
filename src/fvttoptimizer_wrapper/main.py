import logging
import os
import sys
import traceback
from os import path
from typing import List

from fvttmv.update.references_updater import ReferencesUpdater

import fvttoptimizer
from fvttoptimizer.config import ProgramConfig, ConfigFileReader, RunConfig
from fvttoptimizer.exception import FvttOptimizerException, FvttOptimizerInternalException
from fvttoptimizer.optimizer import Optimizer
from fvttoptimizer_wrapper.__constants import app_name, config_file_name, path_to_config_file_linux, issues_url
from fvttoptimizer_wrapper.__help_text import help_text
from fvttoptimizer_wrapper.__version_checker import check_package_versions

bug_report_message = "Please file a bug report on %s" % issues_url

version_option = "--version"
verbose_info_option = "--verbose-info"
verbose_debug_option = "--verbose-debug"
recursive_option = "--recursive"
quality_option = "--quality"
override_percent_option = "--override-percent"
skip_existing_option = "--skip-existing"
skip_webp_option = "--skip-webp"
help_option = "--help"

allowed_args = [
    version_option,
    verbose_info_option,
    verbose_debug_option,
    recursive_option,
    quality_option,
    override_percent_option,
    skip_existing_option,
    skip_webp_option,
    help_option
]


def get_path_to_config_file():
    if sys.platform == "linux":
        return path_to_config_file_linux
    elif sys.platform == "win32":
        dir_of_script: str
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # running in a PyInstaller bundle
            # TODO fix: this doesn't work in cmd only in powershell
            dir_of_script = os.path.dirname(sys.argv[0])
        else:
            # running in normal python environment
            dir_of_script = path.abspath(path.dirname(__file__))
        return os.path.join(dir_of_script, config_file_name)
    else:
        raise FvttOptimizerException("Unsupported OS: {0}".format(sys.platform))


def read_config_file() -> ProgramConfig:
    path_to_config_file = get_path_to_config_file()

    return ConfigFileReader.read_config_file(path_to_config_file)


def perform_optimization_with(
        target_path: str,
        run_config: RunConfig) -> None:
    logging.debug("Running with target_path='%s', config='%s'",
                  target_path,
                  run_config)

    # abs_path removes trailing \ and / but doesn't fail on illegal characters
    abs_target_path = path.abspath(target_path)

    references_updater = ReferencesUpdater(run_config.get_abs_path_to_foundry_data())

    optimizer = Optimizer(run_config,
                          references_updater)

    optimizer.optimize(abs_target_path)


def check_for_unknown_arguments(args: List[str]) -> None:
    for arg in args:
        if arg.startswith("-"):
            if arg not in allowed_args:
                raise FvttOptimizerException("Unknown argument: {0}".format(arg))


def check_for_illegal_argument_combos(args: List[str]) -> None:
    combination_error_msg = "Combining '{0}' and '{1}' is not allowed"

    if verbose_debug_option in args and verbose_info_option in args:
        msg = combination_error_msg.format(verbose_info_option, verbose_debug_option)
        raise FvttOptimizerException(msg)


def check_for_duplicate_args(args: List[str]) -> None:
    for allowed_arg in allowed_args:
        if args.count(allowed_arg) > 1:
            raise FvttOptimizerException("Only one occurrence per option is allowed")


def check_option_args(args: List[str]) -> None:
    check_for_unknown_arguments(args)
    check_for_illegal_argument_combos(args)
    check_for_duplicate_args(args)


def add_logging_stream_handler(level: int):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)


def configure_logging(
        args: List[str]) -> None:
    if verbose_debug_option in args:
        add_logging_stream_handler(logging.DEBUG)
        args.remove(verbose_debug_option)
    elif verbose_info_option in args:
        add_logging_stream_handler(logging.INFO)
        args.remove(verbose_info_option)
    else:
        logging.disable(logging.CRITICAL)
        logging.disable(logging.ERROR)


def read_bool_arg(arg: str,
                  args: List[str],
                  default: bool = False):
    if arg in args:
        args.remove(arg)
        return True
    else:
        return default


def read_integer_arg(arg: str,
                     args: List[str],
                     default: int):
    if arg in args:
        index_of_value = args.index(arg) + 1

        if index_of_value >= len(args):
            raise FvttOptimizerException("Missing integer value for {0}".format(arg))

        str_value = args[index_of_value]
        int_value: int
        try:
            int_value = int(str_value)
        except ValueError:
            raise FvttOptimizerException("{0} has to be followed by an integer.".format(arg))

        del args[index_of_value]
        args.remove(arg)

        return int_value
    else:
        return default


def process_and_remove_config_args(
        run_config: RunConfig,
        args: List[str]) -> None:
    """
    Processes all args which affect the run config
    """
    run_config.skip_existing = read_bool_arg(skip_existing_option,
                                             args)
    run_config.skip_webp = read_bool_arg(skip_webp_option,
                                         args)

    run_config.recursive = read_bool_arg(recursive_option,
                                         args)

    run_config.quality = read_integer_arg(quality_option,
                                          args,
                                          run_config.quality)

    run_config.override_percent = read_integer_arg(override_percent_option,
                                                   args,
                                                   run_config.override_percent)


def do_run() -> None:
    check_package_versions()

    src_list: list
    dst: str

    args = sys.argv[1:]

    check_option_args(args)

    configure_logging(args)

    logging.debug("Got arguments %s",
                  sys.argv)

    if help_option in args:
        print(help_text)
        return

    if version_option in args:
        print("{0} version: {1}".format(app_name, fvttoptimizer.__version__))
        return

    run_config = RunConfig(read_config_file())

    process_and_remove_config_args(run_config,
                                   args)

    if len(args) > 1:
        raise FvttOptimizerException("Too many arguments.")
    if len(args) < 1:
        raise FvttOptimizerException("Target argument missing.")

    target_path = args[0]

    perform_optimization_with(target_path,
                              run_config)


def main() -> None:
    try:
        do_run()
    except FvttOptimizerInternalException:
        formatted = traceback.format_exc()
        logging.error(formatted)
        print("An internal error occurred: " + str(formatted))
        print(bug_report_message)
    except FvttOptimizerException as exception:
        logging.error(exception)
        print(str(exception))
    except SystemExit:
        pass
    except BaseException:
        formatted = traceback.format_exc()
        logging.error(formatted)
        print("An internal error occurred: " + str(formatted))
        print(bug_report_message)


if __name__ == "__main__":
    main()
