"""
Simple Docker manager using docker-py (docker SDK for Python).
Requires the `docker` package and a running Docker daemon.
"""
import logging
from typing import Optional

try:
    import docker # type: ignore
except Exception:
    docker = None

logger = logging.getLogger(__name__)


class DockerManager:
    def __init__(self):
        if docker is None:
            raise RuntimeError('docker SDK is not installed')
        self.client = docker.from_env()

    def create_container(self, image: str, name: str, ram: int = 1024, cpu: float = 1.0, host_port: int = None, container_port: int = None) -> Optional[str]:
        """Create and start a container. Returns container id or None on failure."""
        try:
            mem_limit = f"{ram}m"
            # cpu_quota and cpu_period could be used; keep it simple here
            ports = None
            if host_port and container_port:
                ports = {f"{container_port}/tcp": int(host_port)}

            # Some images (e.g. Minecraft images) require environment vars like EULA=TRUE
            env = None
            if 'minecraft' in image or 'itzg' in image:
                env = {'EULA': 'TRUE'}

            # If a container exits due to a transient error (network, download, etc.),
            # it's often useful for Docker to try restarting it. Add a conservative
            # restart policy here; adjust as needed for your use-case.
            container = self.client.containers.run(
                image,
                name=name,
                detach=True,
                tty=True,
                mem_limit=mem_limit,
                ports=ports,
                environment=env,
                restart_policy={"Name": "unless-stopped"},
            )
            return container.id
        except Exception as e:
            logger.exception('Failed to create container: %s', e)
            return None

    def start_container(self, container_id: str) -> bool:
        try:
            c = self.client.containers.get(container_id)
            c.start()
            return True
        except Exception:
            logger.exception('Failed to start container')
            return False

    def stop_container(self, container_id: str) -> bool:
        try:
            c = self.client.containers.get(container_id)
            c.stop()
            return True
        except Exception:
            logger.exception('Failed to stop container')
            return False

    def remove_container(self, container_id: str) -> bool:
        try:
            c = self.client.containers.get(container_id)
            c.remove(force=True)
            return True
        except Exception:
            logger.exception('Failed to remove container')
            return False
