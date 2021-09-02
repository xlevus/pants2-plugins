from dataclasses import dataclass

from pants.core.goals.package import BuiltPackage, PackageFieldSet
from pants.core.goals.test import (
    BuildPackageDependenciesRequest,
    BuiltPackageDependencies,
)
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.environment import Environment, EnvironmentRequest
from pants.engine.fs import Digest, MergeDigests
from pants.engine.internals.selectors import Get
from pants.engine.process import BinaryPathRequest, BinaryPaths, Process, ProcessResult
from pants.engine.rules import collect_rules, rule
from pants.engine.target import TransitiveTargets, TransitiveTargetsRequest
from pants.engine.unions import UnionRule
from pants.util.logging import LogLevel


from .targets import (
    DockerDependenciesField,
    DockerImageName,
    DockerImageVersion,
    DockerSources,
)


@dataclass(frozen=True)
class DockerImageFieldSet(PackageFieldSet):
    required_fields = (DockerSources, DockerDependenciesField)

    sources: DockerSources
    dependencies: DockerDependenciesField
    image_name: DockerImageName
    image_version: DockerImageVersion


@dataclass(frozen=True)
class DockerPath:
    path: str
    fingerprint: str


@rule(level=LogLevel.DEBUG)
async def docker_path() -> DockerPath:
    docker_program_paths = await Get(
        BinaryPaths,
        BinaryPathRequest(binary_name="docker", search_path=["/bin", "/usr/bin"]),
    )

    if not docker_program_paths.first_path:
        raise ValueError("Could not find the `docker` program on `/bin` or `/usr/bin`.")

    return DockerPath(
        docker_program_paths.first_path.path,
        docker_program_paths.first_path.fingerprint,
    )


@rule
async def get_built_dependencies(
    field_set: DockerImageFieldSet, docker: DockerPath
) -> BuiltPackage:
    built_packages = await Get(
        BuiltPackageDependencies,
        BuildPackageDependenciesRequest(field=field_set.dependencies),
    )
    pkg_digest = await Get(Digest, MergeDigests(pkg.digest for pkg in built_packages))

    transitive_targets = await Get(
        TransitiveTargets, TransitiveTargetsRequest([field_set.address])
    )

    dockerfile_sources = await Get(
        SourceFiles,
        SourceFilesRequest(
            tgt[DockerSources]
            for tgt in transitive_targets.closure
            if tgt.has_field(DockerSources)
        ),
    )

    digest = await Get(
        Digest, MergeDigests((pkg_digest, dockerfile_sources.snapshot.digest))
    )

    dockerfile, *_ = dockerfile_sources.files

    tag = f"{field_set.image_name.value}:{field_set.image_version.value}"

    env = await Get(Environment, EnvironmentRequest(["DOCKER_HOST"]))

    result = await Get(
        ProcessResult,
        Process(
            argv=[docker.path, "build", "-f", dockerfile, "-t", tag, "."],
            input_digest=digest,
            env=env,
            description=f"Building docker image '{tag}'.",
        ),
    )

    return BuiltPackage(result.output_digest, ())


def rules():
    return [*collect_rules(), UnionRule(PackageFieldSet, DockerImageFieldSet)]
