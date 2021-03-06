#!/usr/bin/env python3

import os
from pathlib import Path
import subprocess
import sys

home_dir=os.getenv('HOME')
tmp_dir=home_dir+'/tmp/hack'
starting_dir=os.getcwd()

subprocess.run(["mkdir","-p",tmp_dir])
os.chdir(tmp_dir)

result=subprocess.run(['wget','https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hack.zip'])
if result.returncode!=0:
    print(f'ERROR:  Hack font download failed with rc={result.returncode}. Exiting.')
    sys.exit(1)

result=subprocess.run(['unzip','Hack.zip'])
if result.returncode!=0:
    print(f'ERROR:  Hack font unpack failed with rc={result.returncode}. Exiting.')
    sys.exit(1)

subprocess.run(['rm','-f','Hack.zip'])

result=subprocess.run(['sudo','mkdir','-p','/usr/share/fonts/ttf/hack-nerd'])
if result.returncode!=0:
    print(f'ERROR:  Fonts dir creation failed with rc={result.returncode}. Exiting.')
    sys.exit(1)

result=subprocess.run("sudo cp * /usr/share/fonts/ttf/hack-nerd",shell=True)
if result.returncode!=0:
    print(f'ERROR:  Copy to fonts dir failed with rc={result.returncode}. Exiting.')
    sys.exit(1)

result=subprocess.run(['fc-cache','-f','-v'])
result=subprocess.run("fc-list|grep Hack",shell=True)

os.chdir(starting_dir)

sys.exit(0)
