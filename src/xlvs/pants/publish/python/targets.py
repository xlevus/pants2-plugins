from pants.engine.target import COMMON_TARGET_FIELDS, StringField

from xlvs.pants.publish.targets import (
    PublishRequest,
    PublishTarget,
)


class PypiRepositoryName(StringField):
    alias = "repository"
    help = "The pypi repository to upload the package to."
    default = "pypi"


class PypiRepositoryUrl(StringField):
    alias = "repository_url"
    help = (
        "The pypi repository url to upload the package to."
        "Takes priority over `repository`."
    )


class PypiRepositoryUsername(StringField):
    alias = "username"
    help = (
        "The username for this repository."
        "Suppirting ${BASH_STYLE} environment interpolation."
    )
    default = "${TWINE_USERNAME}"


class PypiRepositoryPassword(StringField):
    alias = "password"
    help = (
        "The password for this repository. "
        "Supporting ${BASH_STYLE} environment interpolation."
    )
    default = "${TWINE_PASSWORD}"


class PypiPublishRequest(PublishRequest):
    pass


class PypiRepositoryTarget(PublishTarget):
    alias = "pypi_repository"
    help = "A pypi repository."

    core_fields = (
        *PublishTarget.core_fields,
        PypiRepositoryName,
        PypiRepositoryUrl,
        PypiRepositoryUsername,
        PypiRepositoryPassword,
    )
    publish_request_type = PypiPublishRequest
