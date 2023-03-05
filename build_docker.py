import os
import subprocess

from src.constants import Docker


def build_docker(docker_name, path):
    os.chdir(path)

    subprocess.call(
        f"docker build -t {docker_name} .".split(" ")
    )


if __name__ == "__main__":
    dockers = [Docker.OPENMM, Docker.BLENDER_GEN]

    pwd = os.getcwd()

    for docker in dockers:
        build_docker(
            docker,
            os.path.join(pwd, docker)
        )
