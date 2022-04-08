from fvttoptimizer.config import ProgramConfig
from fvttoptimizer.exception import FvttOptimizerException
from test.common import *


class ProgramConfigImplTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_constructor_exceptions(self):
        print("test_constructor_exceptions")
        # not absolute
        try:
            ProgramConfigImpl(C.foundrydata)
            self.fail()
        except FvttOptimizerException:
            pass

        # not normalized
        try:
            ProgramConfigImpl(os.path.join(AbsPaths.Data, "..", C.Data))
            self.fail()
        except FvttOptimizerException:
            pass

        # not a directory
        try:
            ProgramConfigImpl(os.path.abspath(C.Data))
            self.fail()
        except FvttOptimizerException:
            pass

        try:
            ProgramConfigImpl(os.path.abspath("does_not_exist"))
            self.fail()
        except FvttOptimizerException:
            pass

    def test_abs_path_to_foundrydata(self):
        print("test_abs_path_to_foundrydata")

        config = ProgramConfigImpl(AbsPaths.Data)

        self.assertEqual(config.get_abs_path_to_foundry_data(),
                         AbsPaths.Data)

    def test_abstract_functions(self):
        print("test_abstract_functions")

        config = ProgramConfig()
        try:
            config.get_abs_path_to_foundry_data()
            self.fail()
        except NotImplementedError:
            pass
