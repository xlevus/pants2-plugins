from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from typing import ClassVar, Iterable, List, Tuple, Type, TypeVar, cast

from pants.core.goals.package import BuiltPackage, PackageFieldSet
from pants.engine.console import Console
from pants.engine.fs import Digest, MergeDigests
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.internals.selectors import MultiGet
from pants.engine.rules import Get, collect_rules, goal_rule, rule
from pants.engine.target import FieldSet, Targets
from pants.engine.unions import UnionMembership, union


class PublishSubsystem(GoalSubsystem):
    name = "publish"
    help = "Publish packages."


class Publish(Goal):
    subsystem_cls = PublishSubsystem


class PublishFieldSet(FieldSet):
    pass


_FS = TypeVar("_FS", bound=PublishFieldSet)


@union
@dataclass(frozen=True)
class PublishRequest:
    publish_field_set_type: ClassVar[Type[_FS]]
    package_field_set_type: ClassVar[Type[PackageFieldSet]]

    built_package: BuiltPackage
    publish_field_set: _FS


@dataclass(frozen=True)
class PublishSetup:
    request_type: Type[PublishRequest]
    package_field_set: PackageFieldSet
    publish_field_set: PublishFieldSet


@dataclass(frozen=True)
class PublishedPackage:
    package: BuiltPackage


@dataclass(frozen=True)
class PublishedPackageSet:
    publishes: Tuple[PublishedPackage]


@rule
async def request_publish(setup: PublishSetup) -> PublishedPackageSet:
    built_package = await Get(BuiltPackage, PackageFieldSet, setup.package_field_set)

    published_package = await Get(
        PublishedPackageSet,
        PublishRequest,
        setup.request_type(built_package, setup.publish_field_set),
    )

    return published_package


@goal_rule
async def publish(
    console: Console,
    targets: Targets,
    union_membership: UnionMembership,
) -> Publish:
    publish_request_types = cast(
        Iterable[Type[PublishRequest]], union_membership[PublishRequest]
    )
    package_request_types = cast(
        Iterable[Type[PackageFieldSet]], union_membership[PackageFieldSet]
    )

    setups: List[PublishSetup] = []

    for target in targets:
        for request_type in publish_request_types:
            if request_type.publish_field_set_type.is_applicable(target):
                if request_type.package_field_set_type not in package_request_types:
                    console.print_stderr(
                        f"{target.address} is not a packageable target."
                    )
                    return Publish(exit_code=1)

                setups.append(
                    PublishSetup(
                        request_type,
                        request_type.package_field_set_type.create(target),
                        request_type.publish_field_set_type.create(target),
                    )
                )

    published_packages = await MultiGet(
        Get(
            PublishedPackageSet,
            PublishSetup,
            setup,
        )
        for setup in setups
    )

    return Publish(exit_code=1)


def rules():
    return collect_rules()
