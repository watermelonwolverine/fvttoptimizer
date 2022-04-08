import glob
import io
import logging
import os
import sys

from PIL import Image
from fvttmv.path_tools import PathTools
from fvttmv.update.references_updater import ReferencesUpdater

from fvttoptimizer.config import RunConfig
from fvttoptimizer.exception import FvttOptimizerException

file_extensions = ["png", "jpg", "jpeg", "webp"]


class FileOptimizer:
    __run_config: RunConfig
    __references_updater: ReferencesUpdater
    __path_tools: PathTools

    def __init__(self,
                 run_config: RunConfig,
                 path_tools: PathTools,
                 references_updater: ReferencesUpdater):
        self.__run_config = run_config
        self.__path_tools = path_tools
        self.__references_updater = references_updater

    def maybe_optimize(self,
                       abs_path_to_file: str) -> None:

        extension = abs_path_to_file.split(".")[-1]

        if extension.lower() in file_extensions:
            case_correct_abs_path = self.__get_correctly_cased_path(abs_path_to_file)
            self.__maybe_optimize2(case_correct_abs_path)

    def __maybe_optimize2(self,
                          abs_path_to_file: str) -> None:

        new_path = self.__get_new_filename(abs_path_to_file)

        if new_path != abs_path_to_file and os.path.exists(new_path):
            if self.__run_config.skip_existing:
                logging.info("Skipping %s, %s already exists", abs_path_to_file, new_path)
            else:
                raise FvttOptimizerException(
                    "Cannot convert {0}. {1} already exists.".format(abs_path_to_file, new_path))
        else:
            self.__optimize(abs_path_to_file)

    def __optimize(self,
                   abs_path_to_file: str) -> None:

        converted_bytes = self.__encode_as_webp(abs_path_to_file)

        old_size = os.path.getsize(abs_path_to_file)
        new_size = len(converted_bytes)

        if 100 - (new_size / old_size) * 100 < self.__run_config.override_percent:
            logging.info(
                "Skipping %s. Conversion does not result in a significant file size decrease.",
                abs_path_to_file)
            return

        self.__replace_file_with_webp(abs_path_to_file,
                                      converted_bytes)

    def __encode_as_webp(self,
                         abs_path_to_file) -> bytes:

        image: Image.Image = Image.open(abs_path_to_file)

        result: bytes

        with io.BytesIO() as byte_io:
            image.save(byte_io, format="webp", quality=self.__run_config.quality)

            result = byte_io.getvalue()

        return result

    def __replace_file_with_webp(self,
                                 abs_path_to_file,
                                 webp_bytes) -> None:

        new_path = self.__get_new_filename(abs_path_to_file)

        with open(new_path, "wb+") as fout:
            fout.write(webp_bytes)

        if abs_path_to_file == new_path:
            return

        old_reference = self.__path_tools.create_reference_from_absolute_path(abs_path_to_file)
        new_reference = self.__path_tools.create_reference_from_absolute_path(new_path)

        self.__references_updater.replace_references(old_reference,
                                                     new_reference)

        os.remove(abs_path_to_file)

    @staticmethod
    def __get_new_filename(abs_path_to_file):
        abs_path_to_parent_dir, old_filename = os.path.split(abs_path_to_file)

        filename_splits = old_filename.split(".")

        old_extension = filename_splits[-1]

        new_filename: str

        if old_extension.lower() == "webp":
            new_filename = old_filename
        else:
            filename_without_extension = filename_splits[0:-1]
            new_filename = ".".join(filename_without_extension) + ".webp"

        result = os.path.join(abs_path_to_parent_dir, new_filename)

        return result

    @staticmethod
    def __get_correctly_cased_path(abs_path_to_file):

        if sys.platform == "linux":
            return abs_path_to_file
        if sys.platform == "win32":
            dirs = abs_path_to_file.split('\\')
            # disk letter
            test_name = [dirs[0].upper()]
            for d in dirs[1:]:
                test_name += ["%s[%s]" % (d[:-1], d[-1])]
            res = glob.glob('\\'.join(test_name))
            if not res:
                # File not found
                return None
            return res[0]
