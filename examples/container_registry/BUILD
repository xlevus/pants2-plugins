container_registry(
    name="exmaple-registry",
    registry="example.com/docker/registry",
)

docker_image(
    name="image",
    sources=["Dockerfile"],
    image_name="hello",
    image_version="latest",
    repositories=[
        ":example-registry",
    ],
)