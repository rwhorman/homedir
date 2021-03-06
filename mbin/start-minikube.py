#!/usr/bin/env python3

# TODO: accommodate diff platforms (MacOS only now)
# TODO: automatically set default based on available resources (cores, mem)
#       and available vm driver
# TODO: provide optional cmd-line args to set cores, mem explicitly

import subprocess

try:
    subprocess.run(["minikube", "start", "--vm-driver=xhyve", "--cpus=4", "--memory=8192"])
except FileNotFoundError:
    print("ERROR: minikube not installed or not in path")
