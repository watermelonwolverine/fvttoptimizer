import os
import shutil
import sys

from fvttoptimizer.exception import FvttOptimizerException
from test.common import AbsPaths, References, TestBase, ReplaceReferenceCall, Checksums, unchanged_directory_tree, C


class OptimizerTest(TestBase):

    def test_optimize_png(self):
        print("test_optimize_png")

        self.optimizer.optimize(AbsPaths.file1_png)

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_png,
                                     References.file1_webp)
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        expected_directory_tree = \
            [AbsPaths.assets,
             AbsPaths.images,
             AbsPaths.file1_webp,
             AbsPaths.file2_jpg,
             AbsPaths.sub_folder,
             AbsPaths.file3_webp,
             AbsPaths.modules,
             AbsPaths.systems,
             AbsPaths.worlds,
             AbsPaths.some_world
             ]

        self.assert_directory_tree_equals(expected_directory_tree)

        self.assert_sha256_hex_equals(AbsPaths.file1_webp, Checksums.file1_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file2_jpg, Checksums.file2_jpg)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp)

    def test_optimize_jpg(self):
        print("test_optimize_jpg")

        self.optimizer.optimize(AbsPaths.file2_jpg)

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file2_jpg,
                                     References.file2_webp)
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        expected_directory_tree = \
            [AbsPaths.assets,
             AbsPaths.images,
             AbsPaths.file1_png,
             AbsPaths.file2_webp,
             AbsPaths.sub_folder,
             AbsPaths.file3_webp,
             AbsPaths.modules,
             AbsPaths.systems,
             AbsPaths.worlds,
             AbsPaths.some_world
             ]

        self.assert_directory_tree_equals(expected_directory_tree)

        self.assert_sha256_hex_equals(AbsPaths.file1_png, Checksums.file1_png)
        self.assert_sha256_hex_equals(AbsPaths.file2_webp, Checksums.file2_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp)

    def test_optimize_webp(self):
        print("test_optimize_webp")

        self.optimizer.optimize(AbsPaths.file3_webp)

        expected_update_reference_call = []

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        expected_directory_tree = unchanged_directory_tree

        self.assert_directory_tree_equals(expected_directory_tree)

        self.assert_sha256_hex_equals(AbsPaths.file1_png, Checksums.file1_png)
        self.assert_sha256_hex_equals(AbsPaths.file2_jpg, Checksums.file2_jpg)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp_75)

    def test_optimize_folder_non_recursive(self):
        print("test_optimize_folder_non_recursive")

        self.optimizer.optimize(AbsPaths.images)

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_png, References.file1_webp),
                ReplaceReferenceCall(References.file2_jpg, References.file2_webp)
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        expected_directory_tree = \
            [AbsPaths.assets,
             AbsPaths.images,
             AbsPaths.file1_webp,
             AbsPaths.file2_webp,
             AbsPaths.sub_folder,
             AbsPaths.file3_webp,
             AbsPaths.modules,
             AbsPaths.systems,
             AbsPaths.worlds,
             AbsPaths.some_world
             ]

        self.assert_directory_tree_equals(expected_directory_tree)

        self.assert_sha256_hex_equals(AbsPaths.file1_webp, Checksums.file1_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file2_webp, Checksums.file2_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp)

    def test_optimize_folder_recursive(self):
        print("test_optimize_folder_recursive")

        self.run_config.recursive = True
        self.optimizer.optimize(AbsPaths.images)

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_png, References.file1_webp),
                ReplaceReferenceCall(References.file2_jpg, References.file2_webp)
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        expected_directory_tree = \
            [AbsPaths.assets,
             AbsPaths.images,
             AbsPaths.file1_webp,
             AbsPaths.file2_webp,
             AbsPaths.sub_folder,
             AbsPaths.file3_webp,
             AbsPaths.modules,
             AbsPaths.systems,
             AbsPaths.worlds,
             AbsPaths.some_world
             ]

        self.assert_directory_tree_equals(expected_directory_tree)

        self.assert_sha256_hex_equals(AbsPaths.file1_webp, Checksums.file1_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file2_webp, Checksums.file2_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp_75)

    def test_optimize_folder_outside_foundry_data(self):
        print("test_optimize_folder_outside_foundry_data")

        try:
            self.optimizer.optimize(AbsPaths.outside_data)
            self.fail()
        except FvttOptimizerException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_optimize_Data(self):
        print("test_optimize_Data")

        try:
            self.optimizer.optimize(AbsPaths.Data)
            self.fail()
        except FvttOptimizerException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_optimize_taboo_directory1(self):
        print("test_optimize_taboo_directory1")

        for taboo_dir in [AbsPaths.systems, AbsPaths.modules]:

            try:
                self.optimizer.optimize(os.path.join(AbsPaths.Data, taboo_dir))
                self.fail()
            except FvttOptimizerException as ex:
                print("Got exception: " + str(ex))

            self.assert_nothing_changed()

            self.references_updater_mock.calls.clear()
            self.walker_callback.result.clear()

    def test_optimize_avoid_override1(self):
        print("test_optimize_avoid_override1")

        shutil.copy(AbsPaths.file1_png, AbsPaths.file1_webp)

        try:
            self.optimizer.optimize(AbsPaths.file1_png)
            self.fail()
        except FvttOptimizerException as ex:
            print("Got exception: " + str(ex))
            os.remove(AbsPaths.file1_webp)

        self.assert_nothing_changed()

    def test_optimize_avoid_override2(self):
        print("test_optimize_avoid_override2")

        self.run_config.skip_existing = True
        shutil.copy(AbsPaths.file1_png, AbsPaths.file1_webp)

        self.optimizer.optimize(AbsPaths.file1_png)

        os.remove(AbsPaths.file1_webp)

        self.assert_nothing_changed()

    def test_optimize_override_percent(self):
        print("test_optimize_override_percent")

        self.run_config.override_percent = 99

        self.optimizer.optimize(AbsPaths.file1_png)

        self.assert_nothing_changed()

    def test_optimize_wrongly_cased_file(self):

        print("test_optimize_wrongly_cased_file")

        if sys.platform == "linux":
            print("SKIPPED")
            return

        self.optimizer.optimize(os.path.join(AbsPaths.images, C.file1_png.upper()))

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_png,
                                     References.file1_webp)
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        expected_directory_tree = \
            [AbsPaths.assets,
             AbsPaths.images,
             AbsPaths.file1_webp,
             AbsPaths.file2_jpg,
             AbsPaths.sub_folder,
             AbsPaths.file3_webp,
             AbsPaths.modules,
             AbsPaths.systems,
             AbsPaths.worlds,
             AbsPaths.some_world
             ]

        self.assert_directory_tree_equals(expected_directory_tree)

        self.assert_sha256_hex_equals(AbsPaths.file1_webp, Checksums.file1_webp_75)
        self.assert_sha256_hex_equals(AbsPaths.file2_jpg, Checksums.file2_jpg)
        self.assert_sha256_hex_equals(AbsPaths.file3_webp, Checksums.file3_webp)
