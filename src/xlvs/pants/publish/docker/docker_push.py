import re
from pants.engine.console import Console
from pants.engine.rules import collect_rules, rule

from xlvs.pants.publish.publish_subsystem import PublishedPackage

from .targets import DockerPublishRequest


@rule
def publish_docker_image(
    console: Console, request: DockerPublishRequest
) -> PublishedPackage:
    console.print_stdout(
        f"STUB: Docker Push {', '.join(f.relpath for f in request.built_package.artifacts)} to {request.publish_target.address}"
    )
    return PublishedPackage(request.built_package, request.publish_target.address)


def rules():
    return [
        *collect_rules(),
    ]
