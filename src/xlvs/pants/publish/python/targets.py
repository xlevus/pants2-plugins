from pants.engine.target import COMMON_TARGET_FIELDS, StringField

from xlvs.pants.publish.targets import BaseRepositoriesField, PublishDestinationTarget


class PypiRepositoryName(StringField):
    alias = "repository"
    help = "The pypi repository to upload the package to."
    default = "pypi"


class PypiRepositoryUrl(StringField):
    alias = "repository_url"
    help = "The pypi repository url to upload the package to."


class PypiRepositoryUsernameVar(StringField):
    alias = "username"
    help = (
        "The username for this repository."
        "Suppirting ${BASH_STYLE} environment interpolation."
    )
    default = "${TWINE_USERNAME}"


class PypiRepositoryPasswordVar(StringField):
    alias = "password"
    help = (
        "The password for this repository. "
        "Supporting ${BASH_STYLE} environment interpolation."
    )
    default = "${TWINE_PASSWORD}"


class PypiRepositoryTarget(PublishDestinationTarget):
    alias = "pypi_repository"
    help = "A pypi repository."

    core_fields = (
        *COMMON_TARGET_FIELDS,
        PypiRepositoryName,
        PypiRepositoryUrl,
        PypiRepositoryUsernameVar,
        PypiRepositoryPasswordVar,
    )


class Repositories(BaseRepositoriesField):
    destination_type = PypiRepositoryTarget
