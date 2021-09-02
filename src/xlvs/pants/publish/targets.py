from dataclasses import dataclass
from typing import Type

from pants.engine.target import COMMON_TARGET_FIELDS, SpecialCasedDependencies, Target


class PublishDestinationTarget(Target):
    pass


class BaseRepositoriesField(SpecialCasedDependencies):
    alias = "repositories"
    help = "Repositories to publish to."

    destination_type: Type[PublishDestinationTarget]
