from dataclasses import dataclass
from typing import ClassVar, Type

from pants.core.goals.package import BuiltPackage
from pants.engine.target import (
    COMMON_TARGET_FIELDS,
    FieldSet,
    SpecialCasedDependencies,
    Target,
)
from pants.engine.unions import union


class PublishTargetField(SpecialCasedDependencies):
    alias = "publish_targets"
    help = "Repositories to publish to."


@dataclass(frozen=True)
class PublishTargetFieldSet(FieldSet):
    required_fields = (PublishTargetField,)


@union
@dataclass(frozen=True)
class PublishRequest:
    built_package: BuiltPackage
    fieldset: PublishTargetFieldSet
    publish_target: "PublishTarget"


class PublishTarget(Target):
    core_fields = (*COMMON_TARGET_FIELDS,)

    publish_request_type: ClassVar[Type[PublishRequest]]
    publishee_fieldset_type: ClassVar[
        Type[PublishTargetFieldSet]
    ] = PublishTargetFieldSet
