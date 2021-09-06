import re
from dataclasses import dataclass
from typing import Dict, OrderedDict

from pants.engine.environment import Environment, EnvironmentRequest
from pants.engine.rules import Get, collect_rules, goal_rule, rule
from pants.util.frozendict import FrozenDict
from pants.util.meta import frozen_after_init

ENV_STRING_RE = re.compile(r"^\$\{([A-Za-z_]{1,}[A-Za-z0-9]{0,})\}$")


@frozen_after_init
@dataclass(unsafe_hash=True)
class EnvironmentStringRequest:
    """Request string values w/ simple environment variable interpolation.

    ${FOO_BAR} == os.environ("FOO_BAR")
    FOO_BAR == "FOO_BAR"
    """

    requested: FrozenDict[str, str]

    def __init__(self, requested: Dict[str, str]):
        self.requested = FrozenDict(requested)


class EnvironmentStringSet(FrozenDict[str, str]):
    pass


@rule
async def environment_string(request: EnvironmentStringRequest) -> Environment:
    values = OrderedDict()
    pending = {}
    to_request = []

    for key, value in request.requested.items():
        match = ENV_STRING_RE.match(value)
        if match:
            env_key = match.groups()[0]
            to_request.append(env_key)
            pending[env_key] = key
        else:
            values[key] = value

    env = await Get(Environment, EnvironmentRequest(to_request, to_request))

    for key, value in env.items():
        target = pending[key]
        values[target] = value

    return Environment(values)


def rules():
    return [*collect_rules()]
