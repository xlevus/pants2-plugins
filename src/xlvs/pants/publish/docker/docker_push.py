from dataclasses import dataclass
from pants.engine.rules import collect_rules, rule
from pants.engine.target import FieldSet
from pants.engine.unions import UnionRule
from xlvs.pants.docker.build_image import DockerImageFieldSet, rules

from xlvs.pants.publish.docker.targets import DockerRepositoriesField
from xlvs.pants.publish.publish_subsystem import PublishRequest, PublishedPackageSet


@dataclass(frozen=True)
class DockerPushFieldSet(FieldSet):
    required_fields = (DockerRepositoriesField,)


class DockerPushRequest(PublishRequest):
    publish_field_set_type = DockerPushFieldSet
    package_field_set_type = DockerImageFieldSet


@rule
def publish_docker_image(request: DockerPushRequest) -> PublishedPackageSet:
    print("DOCKER", request)
    return PublishedPackageSet(())


def rules():
    return [
        *collect_rules(),
        UnionRule(PublishRequest, DockerPushRequest),
    ]
