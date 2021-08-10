from . import build_image, targets


def target_types():
    return [targets.DockerImage]


def rules():
    return [*build_image.rules()]
