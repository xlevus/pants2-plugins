from pants.backend.python.target_types import PythonDistribution

from . import targets, twine


def target_types():
    return [targets.PypiRepositoryTarget]


def rules():
    return [
        *twine.rules(),
        PythonDistribution.register_plugin_field(targets.Repositories),
    ]
