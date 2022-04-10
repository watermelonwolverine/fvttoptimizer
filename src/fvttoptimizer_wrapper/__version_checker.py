import PIL
import fvttmv

from fvttoptimizer.exception import FvttOptimizerException

required_pillow_version_str = "9.1.0"
required_fvttmv_version_str = "0.2.4"
required_pyinstaller_version_str = "4.10"


class Version:

    def __init__(self,
                 major: int,
                 minor: int,
                 bugfix: int):
        self.major = major
        self.minor = minor
        self.bugfix = bugfix

    @staticmethod
    def from_string(version_str: str):
        splits = version_str.split(".")

        if len(splits) != 3:
            raise Exception()

        major = int(splits[0])
        minor = int(splits[1])
        bugfix = int(splits[2])

        return Version(major, minor, bugfix)

    def __gt__(self, other):

        if type(other) is not Version:
            raise Exception

        other_version: Version = other

        if self.major > other_version.major:
            return True
        if self.minor > other_version.minor:
            return True
        if self.bugfix > other_version.bugfix:
            return True

        return False

    def __eq__(self, other):
        if type(other) is not Version:
            raise Exception

        other_version: Version = other

        return other_version.major == self.major \
               and other_version.minor == self.minor \
               and other_version.bugfix == self.bugfix

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return other >= self

    def __lt__(self, other):
        return other > self

    def __str__(self):
        return "{0}.{1}.{2}".format(self.major, self.minor, self.bugfix)


def check_package_versions():
    pillow_version = Version.from_string(PIL.__version__)
    required_pillow_version = Version.from_string(required_pillow_version_str)

    fvttmv_version = Version.from_string(fvttmv.__version__)
    required_fvttmv_version = Version.from_string(required_fvttmv_version_str)

    if not pillow_version == required_pillow_version:
        raise FvttOptimizerException("Requirement not met: Pillow version == {0}".format(required_pillow_version))

    if not fvttmv_version == required_fvttmv_version:
        raise FvttOptimizerException("Requirement not met: fvttmv version == {0}".format(required_fvttmv_version))
