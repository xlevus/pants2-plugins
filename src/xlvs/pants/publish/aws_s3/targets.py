from xlvs.pants.publish.targets import (
    PublishRequest,
    PublishTarget,
)


class S3PublishRequest(PublishRequest):
    pass


class S3PublishTarget(PublishTarget):
    alias = "aws_s3_bucket"
    help = "An AWS S3 Bucket"

    core_fields = (*PublishTarget.core_fields,)
    publish_request_type = S3PublishRequest
