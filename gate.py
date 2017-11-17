#!/usr/bin/env python3
from plumbum.cmd import docker
from plumbum import FG
from plumbum import cli
import os
import sys

image = "test_image:latest"

class Action(object):
    def __init__(self, func, args=[]):
        self.func = func
        self.args = args

    def __call__(self):
        self.func(*self.args)


class MyApp(cli.Application):

    _action_list = []

    @cli.switch("--build", excludes=["--gcbuild"])
    def build(self):
        """Build the jupyter docker image"""
        action = Action(self.build_image)
        self._action_list.insert(0, action)

    @cli.switch("--jupyter")
    def jupyter(self):
        """Run the jupyter docker image"""
        action = Action(self.run_image)
        self._action_list.append(action)

    def _check_docker_daemon(self):
        try:
            docker["ps"]()
        except:
            print("Failed to connect to the docker daemon. Do you have the daemon running?")
            sys.exit(1)

    def build_image(self, build_type):
        self._check_docker_daemon()
        (docker["build", "-t", "test_image", "."]) & FG

    def run_image(self):
        self._check_docker_daemon()
        home_folder = os.getenv("HOME")

        try:
            print(f"Starting container with image {image}")
            (docker["run",
                    "-v", "/:/local",
                    "-v", "/var/run/docker.sock:/var/run/docker.sock",
                    "-v", f"{home_folder}/.config/gcloud:/root/.config/gcloud",
                    "--net=host",
                    image,
                    "jupyter",
                    "notebook",
                    "--allow-root"]) & FG
        except KeyboardInterrupt:
            print(f"Turning off container {image}")
            sys.exit(1)

    def main(self):
        for action in self._action_list:
            action()

if __name__ == "__main__":
    MyApp.run()
