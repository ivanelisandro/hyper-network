import docker
from hstest import StageTest, dynamic_test, CheckResult

test_network = "hyper-network"
test_volume = "hyper-volume"
project_images = ["postgres:15.3"]

test_mongo_envs = [
    'POSTGRES_PASSWORD=hyper2023',
    'POSTGRES_USER=hyper',
    'POSTGRES_DB=hyper-db',
]


class DockerTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None
        self.client = docker.from_env()

    @dynamic_test()
    def test1(self):
        """Tests that network exists in the system"""
        network_names = "".join(network.attrs.get("Name") for network in self.client.networks.list())
        if test_network not in network_names:
            return CheckResult.wrong(f"'{test_network}' not found in the system networks!")

        return CheckResult.correct()

    @dynamic_test()
    def test2(self):
        """Tests that volume exists in the system"""
        volume_names = "".join(volume.attrs.get("Name") for volume in self.client.volumes.list())
        if test_volume not in volume_names:
            return CheckResult.wrong(f"'{test_volume}' not found in the system volumes!")

        return CheckResult.correct()

    @dynamic_test()
    def test3(self):
        """Tests if images exist in the system"""
        images_text = " ".join([str(image) for image in self.client.images.list()])
        for image in project_images:
            if image not in images_text:
                return CheckResult.wrong(f"'{image}' not found in the system images!")

        return CheckResult.correct()

    @dynamic_test()
    def test4(self):
        """Tests image of container, state,exposed port, and host port"""
        all_containers = self.client.containers.list(all=True)
        container_name = "hyper-postgres"
        image_name = "postgres:15.3"
        exposed_port = "5432/tcp"
        host_port = "5432"
        status = "running"
        selected_container = None

        for container in all_containers:
            # Finds the container object to test
            if container_name in container.name:
                selected_container = container

        if not selected_container:
            # Fails if the expected container is not found
            return CheckResult.wrong(f"Couldn't find a container with the name '{container_name}'!")

        if image_name not in selected_container.attrs.get("Config").get("Image"):
            return CheckResult.wrong(f"Couldn't find a container from the '{image_name}' image!")

        if status not in selected_container.status:
            # Fails if the container is not running
            return CheckResult.wrong(f"The container should be {status}!")

        host_ports = selected_container.ports.get(exposed_port)

        if not host_ports:
            # Fails if the exposed port is wrong and returns None
            return CheckResult.wrong(
                f"The exposed port should be {exposed_port} and need to be mapped to a host port!")

        host_ports_str = "_".join(item.get("HostPort", "_") for item in host_ports)

        if host_port not in host_ports_str:
            # Fails if the host port is wrong
            return CheckResult.wrong(f"You should map {exposed_port} to {host_port}!")

        if not selected_container.attrs or \
                not selected_container.attrs.get("Config") or \
                not selected_container.attrs.get("Config").get("Env"):
            # Tests if environments exists
            return CheckResult.wrong(f"Environments are not defined!")

        container_envs = selected_container.attrs.get("Config").get("Env")

        for env in test_mongo_envs:
            # Tests if environments are defined
            if env not in container_envs:
                return CheckResult.wrong(f"Environment `{env}` not found!")

        if not selected_container.attrs.get("NetworkSettings") or \
                not selected_container.attrs.get("NetworkSettings").get("Networks"):
            # Tests if container network mode exists
            return CheckResult.wrong("Could not read networks from container!")

        container_networks = "*".join(selected_container.attrs.get("NetworkSettings").get("Networks").keys())
        if test_network not in container_networks:
            # Tests if container network is correct
            return CheckResult.wrong(f"The container network is wrong for {container_name}!")

        if not selected_container.attrs.get("Mounts") or \
                not selected_container.attrs.get("Mounts")[0].get("Name"):
            # Tests if container volume exists
            return CheckResult.wrong(
                "Could not read volume from container!")

        # Tests if container volume is correct
        mounts = selected_container.attrs.get("Mounts", [])
        is_volume_found = False
        for mount in mounts:
            if test_volume in mount.get("Name"):
                is_volume_found = True

        if not is_volume_found:
            return CheckResult.wrong(f"The container volume is wrong for {container_name}!")

        return CheckResult.correct()


if __name__ == '__main__':
    DockerTest().run_tests()
