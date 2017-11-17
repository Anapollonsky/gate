#!/usr/bin/env python3
from plumbum.cmd import docker
from plumbum import FG
from plumbum import cli
import os
import sys

DOCKER_IMAGE_NAME = "gate"

class Action(object):
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def __call__(self):
        self.func(*self.args)


class MyApp(cli.Application):

    _action_list = []

    @cli.switch("--build")
    def build(self):
        """Build the docker image"""
        action = Action(self.build_image)
        self._action_list.insert(0, action)

    @cli.switch("--jupyter", str)
    def jupyter(self, place):
        """Run the jupyter docker image"""
        place = os.path.abspath(place) if place else os.getcwd
        action = Action(self.run_image, place)
        self._action_list.append(action)

    def _check_docker_daemon(self):
        try:
            docker["ps"]()
        except:
            print("Failed to connect to the docker daemon. Do you have the daemon running?")
            sys.exit(1)

    def build_image(self):
        self._check_docker_daemon()
        (docker["build", "-t", DOCKER_IMAGE_NAME, "."]) & FG

    def run_image(self, place):
        self._check_docker_daemon()
        home_folder = os.getenv("HOME")
        docker_image_full_name = DOCKER_IMAGE_NAME + ":latest"

        try:
            print(f"Starting container with image {docker_image_full_name}")
            (docker["run",
                    "-v", "/:/local",  # map the entire host machine to /local
                    "-v", "/var/run/docker.sock:/var/run/docker.sock",
                    "-v", f"{home_folder}/.config/gcloud:/root/.config/gcloud",  # map gcloud
                    "-w", f"/local/{place}",  # working directory
                    "--net=host",  # share network with host
                    docker_image_full_name,
                    "jupyter", "notebook",
                    "--allow-root"]) & FG
        except KeyboardInterrupt:
            print(f"Turning off container {docker_image_full_name}")
            sys.exit(1)

    def main(self):
        # Handle no argument case
        if (len(sys.argv) == 1): 
            self.help()
        for action in self._action_list:
            action()

if __name__ == "__main__":
    MyApp.run()
