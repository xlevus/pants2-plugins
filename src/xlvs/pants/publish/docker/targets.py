from pants.engine.target import COMMON_TARGET_FIELDS, StringField
from xlvs.pants.docker.targets import DockerImageName, DockerImageVersion

from xlvs.pants.publish.targets import (
    PublishRequest,
    PublishTargetField,
    PublishTarget,
    PublishTargetFieldSet,
)


class DockerRepositoryUrl(StringField):
    alias = "registry"
    help = "URL of container registry."


class DockerPublishFieldSet(PublishTargetFieldSet):
    required_fields = (
        *PublishTargetFieldSet.required_fields,
        DockerImageName,
        DockerImageVersion,
    )


class DockerPublishRequest(PublishRequest):
    pass


class DockerRepositoryTarget(PublishTarget):
    alias = "container_registry"
    help = "A docker container registry."

    core_fields = (
        *COMMON_TARGET_FIELDS,
        DockerRepositoryUrl,
    )
    publish_request_type = DockerPublishRequest
    publishee_fieldset_type = DockerPublishFieldSet
