from pants.backend.python.target_types import PythonDistribution
from pants.engine.unions import UnionRule

from xlvs.pants.publish.targets import PublishRequest, PublishTargetField

from . import targets, s3_upload


def target_types():
    return [targets.S3PublishTarget]


def rules():
    return [
        *s3_upload.rules(),
        PythonDistribution.register_plugin_field(PublishTargetField),
        UnionRule(PublishRequest, targets.S3PublishRequest),
    ]
