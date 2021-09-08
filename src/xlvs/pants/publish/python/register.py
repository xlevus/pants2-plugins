from typing import Union
from pants.backend.python.target_types import PythonDistribution
from pants.engine.unions import UnionRule

from xlvs.pants.publish.targets import PublishRequest, PublishTargetField

from . import targets, twine


def target_types():
    return [targets.PypiRepositoryTarget]


def rules():
    return [
        *twine.rules(),
        PythonDistribution.register_plugin_field(PublishTargetField),
        UnionRule(PublishRequest, targets.PypiPublishRequest),
    ]
