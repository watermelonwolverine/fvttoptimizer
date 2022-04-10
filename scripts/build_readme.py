import sys

sys.path.append("src")

# noinspection PyPep8
from cli_wrapper.__help_texts import read_me

with open("README.md", "wt+", encoding="utf-8") as fh:
    fh.write(read_me)
