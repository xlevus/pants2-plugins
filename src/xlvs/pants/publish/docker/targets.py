from pants.engine.target import COMMON_TARGET_FIELDS, StringField

from xlvs.pants.publish.targets import BaseRepositoriesField, PublishDestinationTarget


class DockerRepositoryUrl(StringField):
    alias = "registry"
    help = "URL of container registry."


class DockerRepositoryTarget(PublishDestinationTarget):
    alias = "container_registry"
    help = "A docker container registry."

    core_fields = (
        *COMMON_TARGET_FIELDS,
        DockerRepositoryUrl,
    )


class DockerRepositoriesField(BaseRepositoriesField):
    destination_target = DockerRepositoryTarget
