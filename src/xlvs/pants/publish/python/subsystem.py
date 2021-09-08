from pants.backend.python.target_types import ConsoleScript
from pants.backend.python.subsystems.python_tool_base import PythonToolBase


class Twine(PythonToolBase):
    options_scope = "twine"
    help = "The utility for publishing Python pakcages to PyPi and other repositories."
    default_version = "twine==3.4.2"
    default_main = ConsoleScript("twine")
    register_interpreter_constraints = True
    default_interpreter_constraints = ["CPython>=3.6"]
