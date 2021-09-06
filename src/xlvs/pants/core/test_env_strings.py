import pytest
from pants.engine.environment import Environment, EnvironmentRequest
from pants.testutil.rule_runner import MockGet, run_rule_with_mocks

from xlvs.pants.core.env_strings import EnvironmentStringRequest, environment_string


@pytest.mark.parametrize(
    "input,environment,expected",
    [
        ({"foo": "FOO"}, {}, {"foo": "FOO"}),
        ({"foo": "$FOO"}, {}, {"foo": "$FOO"}),
        ({"foo": "${FOO}"}, {}, {}),
        ({"foo": "${FOO}"}, {"FOO": "bar"}, {"foo": "bar"}),
        ({"foo": "${FOO}", "bar": "BAR"}, {"FOO": "bar"}, {"foo": "bar", "bar": "BAR"}),
    ],
)
def test_environment_string(input, environment, expected):
    request = EnvironmentStringRequest(input)

    def mock_get_environment(request: EnvironmentRequest) -> Environment:
        return Environment(environment)

    result = run_rule_with_mocks(
        environment_string,
        rule_args=[request],
        mock_gets=[
            MockGet(
                output_type=Environment,
                input_type=EnvironmentRequest,
                mock=mock_get_environment,
            )
        ],
    )

    assert dict(result) == expected
