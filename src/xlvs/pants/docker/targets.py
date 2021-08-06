from pants.core.goals.test import RuntimePackageDependenciesField
from pants.engine.target import COMMON_TARGET_FIELDS, Sources, StringField, Target


class DockerDependenciesField(RuntimePackageDependenciesField):
    alias = "dependencies"
    help = "Addresses to targets that can be built with the ./pants package goal."


class DockerSources(Sources):
    default = ("Dockerfile",)
    expected_num_files = 1
    help = "The Dockerfile to use when building the Docker iamge."


class DockerImageName(StringField):
    alias = "image_name"
    help = "Image tag to apply to built images."


class DockerImageVersion(StringField):
    alias = "image_version"
    default = "latest"
    help = "Image tag to apply to built images."


class DockerImage(Target):
    """A docker image."""

    alias = "docker_image"
    core_fields = (
        *COMMON_TARGET_FIELDS,
        DockerDependenciesField,
        DockerSources,
        DockerImageName,
        DockerImageVersion,
    )
    help = "foo"
