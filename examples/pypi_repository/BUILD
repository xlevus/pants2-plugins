
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
    repository_url="https://foo:bar@example.com/",
    username="${PRIVATE_TWINE_USERNAME}",
    password="${PRIVATE_TWINE_PASSWORD}",
)

python_library(name="lib", sources=[])

python_distribution(
    name="example_package",
    provides=setup_py(
        name="xlvs-pants2-pypi-example",
        version="0.0.1",
    ),
    repositories=[
        ":testpypi",
        ":privatepypi",
    ]
)

