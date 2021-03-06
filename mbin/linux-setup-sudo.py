#!/usr/bin/env python3

import os
import subprocess
import sys

print('Objective: Set up passwordless sudo\n')
print('INSTRUCTIONS:')
print('1. Copy this line:')
print(f'     {os.getenv("USER")} ALL=(ALL) NOPASSWD: ALL')
print('2. visudo will be started to edit the file /etc/sudoers')
print('   enter root password at the prompt')
print('3. Add the above line to the bottom of the file and save+exit')
print('\nStart? ("y" to begin, "n" to abort)')

response=input()
if response.upper()!="Y":
    print('Aborting')
    sys.exit(1)

subprocess.run(["sudo", "visudo"])

sys.exit(0)
