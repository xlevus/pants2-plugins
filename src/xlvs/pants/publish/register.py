from pants.core.goals import package

from . import publish_subsystem


def rules():
    return [*package.rules(), *publish_subsystem.rules()]
