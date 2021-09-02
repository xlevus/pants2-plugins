python_library(
    name="lib",
)

pex_binary(
    name="hello-world",
    dependencies=[":lib"],
    entry_point="hello.py:main",
)

docker_image(
    name="image",
    sources=["Dockerfile"],
    image_name="hello-world",
    image_version="latest",
    dependencies=[
        ":hello-world",
    ],
)