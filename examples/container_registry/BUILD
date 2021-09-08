container_registry(
    name="container-store",
    registry="docker-registry.example.com:443",
)

docker_image(
    name="image",
    sources=["Dockerfile"],
    image_name="hello",
    image_version="latest",
    publish_targets=[
        ":container-store",
    ],
)