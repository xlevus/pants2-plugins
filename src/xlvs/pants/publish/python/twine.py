from dataclasses import dataclass
from pants.engine.environment import Environment

from pants.backend.python.util_rules.pex import (
    PexRequest,
    PexRequirements,
    VenvPex,
    VenvPexProcess,
)
from pants.engine.environment import Environment
from pants.engine.process import Process, ProcessResult

from pants.engine.rules import collect_rules, rule, Get

from pants.util.frozendict import FrozenDict

from xlvs.pants.core.env_strings import EnvironmentStringRequest

from xlvs.pants.publish.python.subsystem import Twine


from pants.engine.rules import collect_rules, rule
from pants.util.ordered_set import FrozenOrderedSet
from xlvs.pants.core.env_strings import EnvironmentStringRequest

from xlvs.pants.publish.publish_subsystem import PublishedPackage

from xlvs.pants.publish.python.targets import (
    PypiPublishRequest,
    PypiRepositoryName,
    PypiRepositoryPassword,
    PypiRepositoryTarget,
    PypiRepositoryUrl,
    PypiRepositoryUsername,
)


@dataclass(frozen=True)
class TwineCallArgs:
    args: FrozenOrderedSet
    env: FrozenDict[str, str]


@rule
async def twine_call_args(target: PypiRepositoryTarget) -> TwineCallArgs:
    env = await Get(
        Environment,
        EnvironmentStringRequest(
            {
                "TWINE_USERNAME": target[PypiRepositoryUsername].value,
                "TWINE_PASSWORD": target[PypiRepositoryPassword].value,
            }
        ),
    )

    args = ["--non-interactive"]

    repo_name = target[PypiRepositoryName].value
    repo_url = target[PypiRepositoryUrl].value
    if repo_url:
        args += ["--repository-url", repo_url]
    else:
        args += ["-r", repo_name]

    return TwineCallArgs(FrozenOrderedSet(args), env)


@rule
async def publish_pypi(request: PypiPublishRequest, twine: Twine) -> PublishedPackage:
    twine_pex = await Get(
        VenvPex,
        PexRequest(
            output_filename="twine.pex",
            internal_only=True,
            requirements=PexRequirements(twine.all_requirements),
            main=twine.main,
        ),
    )

    call_args = await Get(TwineCallArgs, PypiRepositoryTarget, request.publish_target)
    paths = [artifact.relpath for artifact in request.built_package.artifacts]

    process = await Get(
        Process,
        VenvPexProcess,
        VenvPexProcess(
            twine_pex,
            argv=["upload", *call_args.args, *paths],
            input_digest=request.built_package.digest,
            extra_env=call_args.env,
            description=f"Publishing {', '.join(paths)} to {request.publish_target.address}.",
        ),
    )

    await Get(ProcessResult, Process, process)

    return PublishedPackage(
        package=request.built_package, publish_target=request.publish_target.address
    )


def rules():
    return [
        *collect_rules(),
    ]
