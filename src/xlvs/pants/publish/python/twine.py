from dataclasses import dataclass
from typing import Optional, Tuple

from pants.core.goals.package import BuiltPackage
from pants.backend.python.util_rules.pex import (
    PexRequest,
    PexRequirements,
    VenvPex,
    VenvPexProcess,
)
from pants.engine.addresses import Addresses, UnparsedAddressInputs
from pants.engine.environment import Environment, EnvironmentRequest
from pants.engine.internals.selectors import MultiGet
from pants.engine.process import Process, ProcessResult
from pants.engine.target import (
    FieldSet,
    Targets,
)
from pants.engine.rules import collect_rules, rule, Get
from pants.engine.unions import UnionRule
from pants.backend.python.goals.setup_py import PythonDistributionFieldSet
from pants.python.python_setup import PythonSetup
from pants.util.frozendict import FrozenDict
from xlvs.pants.core.env_strings import EnvironmentStringRequest

from xlvs.pants.publish.python.subsystem import Twine

from ..publish_subsystem import PublishRequest, PublishedPackage, PublishedPackageSet
from .targets import (
    PypiRepositoryName,
    PypiRepositoryPasswordVar,
    PypiRepositoryTarget,
    PypiRepositoryUrl,
    PypiRepositoryUsernameVar,
    Repositories,
)


@dataclass(frozen=True)
class TwineFieldSet(FieldSet):
    required_fields = (Repositories,)


class TwineRequest(PublishRequest):
    publish_field_set_type = TwineFieldSet
    package_field_set_type = PythonDistributionFieldSet


@dataclass(frozen=True)
class PypiRepository:
    username: str
    password: str
    repository: Optional[str] = None
    url: Optional[str] = None

    def __str__(self):
        if self.url:
            return self.url
        return self.repository


@dataclass(frozen=True)
class PypiRepositorySet:
    repositories: Tuple[PypiRepository]

    def __iter__(self):
        return iter(self.repositories)


@dataclass(frozen=True)
class PublishCall:
    built_package: BuiltPackage
    repository: PypiRepository


@rule
async def get_repository(target: PypiRepositoryTarget) -> PypiRepository:
    env = await Get(
        Environment,
        EnvironmentStringRequest(
            {
                "username": target[PypiRepositoryUsernameVar].value,
                "password": target[PypiRepositoryPasswordVar].value,
            }
        ),
    )
    return PypiRepository(
        env.get("username"),
        env.get("password"),
        target[PypiRepositoryName].value,
        target[PypiRepositoryUrl].value,
    )


@rule
async def get_repositories(field_set: TwineFieldSet) -> PypiRepositorySet:
    (publish_target,) = await Get(Targets, Addresses([field_set.address]))

    repository_targets = await Get(
        Targets,
        UnparsedAddressInputs,
        publish_target[Repositories].to_unparsed_address_inputs(),
    )

    return PypiRepositorySet(
        await MultiGet(
            Get(PypiRepository, PypiRepositoryTarget, target)
            for target in repository_targets
        )
    )


@rule
async def publish(twine: Twine, call: PublishCall) -> PublishedPackage:
    twine_pex = await Get(
        VenvPex,
        PexRequest(
            output_filename="twine.pex",
            internal_only=True,
            requirements=PexRequirements(twine.all_requirements),
            main=twine.main,
        ),
    )

    paths = [artifact.relpath for artifact in call.built_package.artifacts]

    argv = ["upload"]

    if call.repository.url:
        argv.extend(["--repository-url", call.repository.url])
    elif call.repository.repository:
        argv.extend(["-r", call.repository.repository])

    process = await Get(
        Process,
        VenvPexProcess,
        VenvPexProcess(
            twine_pex,
            argv=argv + paths,
            input_digest=call.built_package.digest,
            extra_env=FrozenDict(
                {
                    "TWINE_NON_INTERACTIVE": "true",
                    "TWINE_USERNAME": call.repository.username,
                    "TWINE_PASSWORD": call.repository.password,
                }
            ),
            description=f"Publishing {', '.join(paths)} to {call.repository}.",
        ),
    )

    await Get(ProcessResult, Process, process)

    return PublishedPackage(call.built_package)


@rule
async def publish_twine(request: TwineRequest) -> PublishedPackageSet:
    print("TWINE", request)

    repositories = await Get(
        PypiRepositorySet, TwineFieldSet, request.publish_field_set
    )

    return PublishedPackageSet(
        await MultiGet(
            Get(PublishedPackage, PublishCall(request.built_package, repository))
            for repository in repositories
        )
    )


def rules():
    return [
        *collect_rules(),
        UnionRule(PublishRequest, TwineRequest),
    ]
