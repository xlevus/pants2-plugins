from pants.engine.console import Console
from pants.engine.rules import collect_rules, rule

from xlvs.pants.publish.publish_subsystem import PublishedPackage

from xlvs.pants.publish.aws_s3.targets import S3PublishRequest


@rule
async def upload_s3(console: Console, request: S3PublishRequest) -> PublishedPackage:
    # Stub implementation
    console.print_stdout(
        f"STUB: S3 Upload {', '.join(f.relpath for f in request.built_package.artifacts)} to {request.publish_target.address}"
    )
    return PublishedPackage(request.built_package, request.publish_target.address)


def rules():
    return [
        *collect_rules(),
    ]
