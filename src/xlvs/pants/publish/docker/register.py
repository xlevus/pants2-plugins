from pants.engine.unions import UnionRule
from xlvs.pants.docker.targets import DockerImage
from xlvs.pants.publish.targets import PublishRequest, PublishTargetField

from . import targets, docker_push


def target_types():
    return [targets.DockerRepositoryTarget]


def rules():
    return [
        *docker_push.rules(),
        DockerImage.register_plugin_field(PublishTargetField),
        UnionRule(PublishRequest, targets.DockerPublishRequest),
    ]
