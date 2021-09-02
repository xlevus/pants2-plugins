from xlvs.pants.docker.targets import DockerImage

from . import targets, docker_push


def target_types():
    return [targets.DockerRepositoryTarget]


def rules():
    return [
        *docker_push.rules(),
        DockerImage.register_plugin_field(targets.DockerRepositoriesField),
    ]
