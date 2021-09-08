
pypi_repository(
    name="pypi",
    repository="pypi",
)

pypi_repository(
    name="testpypi",
    repository="testpypi",
)

pypi_repository(
    name="privatepypi",
    repository_url="https://gitlab.inflo.ai/api/v4/projects/175/packages/pypi",
    username="${PRIVATE_TWINE_USERNAME}",
    password="${PRIVATE_TWINE_PASSWORD}",
)

aws_s3_bucket(
    name="s3_bucket",
)

python_library(name="lib", sources=[])

python_distribution(
    name="example_package",
    provides=setup_py(
        name="xlvs-pants2-pypi-example",
        version="0.0.1",
    ),
    setup_py_commands=["bdist_wheel", "sdist"],
    publish_targets=[
        ":privatepypi",
        ":s3_bucket",
    ]
)

