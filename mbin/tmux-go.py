#!/usr/bin/env python3

import argparse
import os
import os.path
import subprocess
import sys

clp = argparse.ArgumentParser(prog='tmux-go',
                              description='Create a preconfigured tmux session')

clp.add_argument('--dev', action='store_true', help='create a programming session')
clp.add_argument('--dir', help='set as current working directory')
clp.add_argument('--kill', dest='kill_session_id', help='kill the specified tmux session')

args = clp.parse_args()

if args.kill_session_id is not None:
   result = subprocess.run(["tmux", "has-session", "-t", args.kill_session_id], stderr=subprocess.DEVNULL)
   if result.returncode == 0:
      subprocess.run(["tmux", "kill-session", "-t", args.kill_session_id])
   else:
      print(f'ERROR Session {args.kill_session_id} does not exist')
   sys.exit(1)

session_name = 'futz'
working_dir = '~'

if args.dev:
   session_name = 'dev'

if args.dir is not None:
   working_dir = args.dir
else:
   if args.dev:
      working_dir = '~/src/github.com/enigmata'

working_dir = os.path.expanduser(working_dir)

if not os.path.isdir(working_dir):
   print(f'"{working_dir}" is not a directory!')
   sys.exit(1)

print(f'INFO Creating a tmux session "{session_name}" in directory "{working_dir}"')

result = subprocess.run(["tmux", "has-session", "-t", session_name], stderr=subprocess.DEVNULL)

if result.returncode != 0:
   print(f'INFO Session "{session_name}" does not exist, creating ...')
   subprocess.run(["tmux", "new-session", "-s", session_name, "-n", "home", "-d"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "split-window", "-h", "-t", session_name], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "send-keys", "-t", f'{session_name}:1.1', f'cd {working_dir}', "C-m"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "send-keys", "-t", f'{session_name}:1.1', "clear", "C-m"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "send-keys", "-t", f'{session_name}:1.2', f'cd {working_dir}', "C-m"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "send-keys", "-t", f'{session_name}:1.2', "clear", "C-m"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "new-window", "-t", f'{session_name}', "-n",  "alternate"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "send-keys", "-t", f'{session_name}:2', f'cd {working_dir}', "C-m"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "send-keys", "-t", f'{session_name}:2', "clear", "C-m"], stderr=subprocess.DEVNULL)
   subprocess.run(["tmux", "select-window", "-t", f'{session_name}:1'], stderr=subprocess.DEVNULL)
   print(f'INFO Session "{session_name}" created')
else:
   print(f'INFO Session "{session_name}" already exists')

if os.getenv('TMUX') is None:
   subprocess.run(["tmux", "attach", "-t", session_name], stderr=subprocess.DEVNULL)
else:
   print('WARN Did not attach to session because aleady in a session')
