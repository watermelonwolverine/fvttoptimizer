import hashlib
import json
import os
import shutil
import unittest
import urllib.parse
from typing import List

from fvttmv.iterators.directory_walker import DirectoryWalker, DirectoryWalkerCallback
from fvttmv.update.references_updater import ReferencesUpdater

from fvttoptimizer.config import RunConfig, ProgramConfigImpl
from fvttoptimizer.optimizer import Optimizer


def ref(*args):
    result = "/".join(args)
    result = urllib.parse.quote(result)
    return result


class C:
    """
    Constants
    """

    foundrydata = "foundrydata"
    outside_data = "outside_data"
    Data = "Data"
    assets = "assets (with space)"
    images = "images"
    worlds = "worlds"
    some_world = "some_world"
    modules = "modules"
    systems = "systems"

    webp = ".webp"
    jpg = ".jpg"
    png = ".png"

    file1 = "file1"
    file2 = "file2 (with space)"
    file3 = "file3"

    file1_png = file1 + png
    file1_webp = file1 + webp
    file2_jpg = file2 + jpg
    file2_webp = file2 + webp
    file3_webp = file3 + webp

    sub_folder = "sub_folder"


class RelPaths:
    worlds = C.worlds
    some_world = os.path.join(worlds, C.some_world)
    systems = C.systems
    modules = C.modules

    assets = C.assets
    images = os.path.join(assets, C.images)
    sub_folder = os.path.join(images, C.sub_folder)

    file1_png = os.path.join(images, C.file1_png)
    file1_webp = os.path.join(images, C.file1_webp)

    file2_jpg = os.path.join(images, C.file2_jpg)
    file2_webp = os.path.join(images, C.file2_webp)

    file3_webp = os.path.join(sub_folder, C.file3_webp)


class AbsPaths:
    foundrydata = os.path.abspath(C.foundrydata)
    outside_data = os.path.join(foundrydata, C.outside_data)
    Data = os.path.join(foundrydata, C.Data)

    assets = os.path.join(Data, RelPaths.assets)
    modules = os.path.join(Data, RelPaths.modules)
    systems = os.path.join(Data, RelPaths.systems)
    worlds = os.path.join(Data, RelPaths.worlds)
    some_world = os.path.join(Data, RelPaths.some_world)
    images = os.path.join(Data, RelPaths.images)
    sub_folder = os.path.join(images, C.sub_folder)

    file1_png = os.path.join(Data, RelPaths.file1_png)
    file1_webp = os.path.join(Data, RelPaths.file1_webp)

    file2_jpg = os.path.join(Data, RelPaths.file2_jpg)
    file2_webp = os.path.join(Data, RelPaths.file2_webp)

    file3_webp = os.path.join(Data, RelPaths.file3_webp)


class References:
    file3_webp = ref(C.assets, C.images, C.sub_folder, C.file3_webp)

    file1_png = ref(C.assets, C.images, C.file1_png)

    file1_webp = ref(C.assets, C.images, C.file1_webp)

    file2_jpg = ref(C.assets, C.images, C.file2_jpg)

    file2_webp = ref(C.assets, C.images, C.file2_webp)


class Checksums:
    file1_png = "c918b18396387fddf8d1bebfbdbe924e199b2ebfbf24fb149e4f2cf4249a0bd0"
    file2_jpg = "11ffba561b98af8479e28470c153bd62763808fd024b04a2f510bc0159240f9d"
    file3_webp = "2fef97d82f3e57a9b8abd1a8a3b19509bd2ca59442aaf21ef694bf6dae457594"

    file1_webp_75 = "7f0fc9a6efa92a70f846c75cdace950930198f2376f37fa8ce3e67c881e8a1a4"
    file2_webp_75 = "92024d36a4bc527e4b61a7a1b434758a28321fac13074c71ec7fd77e7ed88025"
    file3_webp_75 = "fd88dc6b63167affe16aae924d1dbc62ba97bdcce778c5b553dc0a064925386b"


class Setup:

    @staticmethod
    def setup_working_environment():
        if os.path.exists(C.foundrydata):
            shutil.rmtree(C.foundrydata)

        Setup.__setup_folder_structure()

        Setup.__copy_images()

    @staticmethod
    def __setup_folder_structure():
        os.makedirs(AbsPaths.sub_folder)
        os.makedirs(AbsPaths.some_world)
        os.makedirs(AbsPaths.systems)
        os.makedirs(AbsPaths.modules)

    @staticmethod
    def __copy_images():
        shutil.copy(os.path.join("test_files", "Lichtenstein.png"), AbsPaths.file1_png)
        shutil.copy(os.path.join("test_files", "Lichtenstein.jpg"), AbsPaths.file2_jpg)
        shutil.copy(os.path.join("test_files", "Lichtenstein.webp"), AbsPaths.file3_webp)


class DirectoryWalkerCallbackImpl(DirectoryWalkerCallback):
    result: List

    def __init__(self):
        self.result = []

    def step_into_directory(self, abs_path_to_directory: str) -> None:
        self.result.append(abs_path_to_directory)

    def step_out_of_directory(self, abs_path_to_directory: str) -> None:
        pass

    def process_file(self, abs_path_to_file: str) -> None:
        self.result.append(abs_path_to_file)


class ReplaceReferenceCall:
    old_reference: str
    new_reference: str

    def __init__(self,
                 old_reference: str,
                 new_reference: str) -> None:
        self.old_reference = old_reference
        self.new_reference = new_reference

    def __eq__(self, other):
        if not issubclass(type(other), type(self)):
            return False

        otherCall: ReplaceReferenceCall = other

        return \
            self.old_reference == otherCall.old_reference \
            and self.new_reference == otherCall.new_reference

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class ReferencesUpdaterMock(ReferencesUpdater):
    calls: List[ReplaceReferenceCall]

    # noinspection PyMissingConstructor
    def __init__(self):
        self.calls = []

    def replace_references(self,
                           old_reference: str,
                           new_reference: str):
        call = ReplaceReferenceCall(old_reference,
                                    new_reference)

        self.calls.append(call)


unchanged_directory_tree = \
    [AbsPaths.assets,
     AbsPaths.images,
     AbsPaths.file1_png,
     AbsPaths.file2_jpg,
     AbsPaths.sub_folder,
     AbsPaths.file3_webp,
     AbsPaths.modules,
     AbsPaths.systems,
     AbsPaths.worlds,
     AbsPaths.some_world]


class TestBase(unittest.TestCase):
    run_config: RunConfig
    optimizer: Optimizer
    reference_updater_mock: ReferencesUpdaterMock
    walker_callback: DirectoryWalkerCallbackImpl
    directory_walker: DirectoryWalker

    def setUp(self) -> None:
        Setup.setup_working_environment()
        program_config = ProgramConfigImpl(AbsPaths.Data)
        self.run_config = RunConfig(program_config)
        self.references_updater_mock = ReferencesUpdaterMock()
        self.optimizer = Optimizer(self.run_config,
                                   self.references_updater_mock)
        self.walker_callback = DirectoryWalkerCallbackImpl()
        self.directory_walker = DirectoryWalker(self.walker_callback)

    def assert_reference_updater_calls_equal(self,
                                             expected_reference_updater_calls: List[ReplaceReferenceCall]):
        self.assertEqual(expected_reference_updater_calls,
                         self.references_updater_mock.calls)

    def assert_directory_tree_equals(self,
                                     expected_directory_tree: List[str]):
        self.directory_walker.walk_directory(AbsPaths.Data)

        self.assertEqual(self.walker_callback.result,
                         expected_directory_tree)

    def assert_sha256_hex_equals(self,
                                 path_to_file: str,
                                 sha256_hex: str):
        sha256: str

        with open(path_to_file, "rb") as fin:
            sha256 = str(hashlib.sha256(fin.read()).hexdigest())

        self.assertEqual(sha256, sha256_hex)

    def assert_nothing_changed(self):
        self.assert_directory_tree_equals(unchanged_directory_tree)
        self.assert_reference_updater_calls_equal([])
        self.assert_sha256_hex_equals(AbsPaths.file1_png, Checksums.file1_png)
        self.assert_sha256_hex_equals(AbsPaths.file2_jpg, Checksums.file2_jpg)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp)
